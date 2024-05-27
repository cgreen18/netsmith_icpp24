/*
 * Copyright (c) 2020 Advanced Micro Devices, Inc.
 * Copyright (c) 2020 Inria
 * Copyright (c) 2016 Georgia Institute of Technology
 * Copyright (c) 2008 Princeton University
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */


#include "mem/ruby/network/garnet/NetworkInterface.hh"

#include <cassert>
#include <cmath>

#include "base/cast.hh"
#include "debug/RubyNetwork.hh"
#include "mem/ruby/network/MessageBuffer.hh"
#include "mem/ruby/network/garnet/Credit.hh"
#include "mem/ruby/network/garnet/flitBuffer.hh"
#include "mem/ruby/slicc_interface/Message.hh"

namespace gem5
{

namespace ruby
{

namespace garnet
{

NetworkInterface::NetworkInterface(const Params &p)
  : ClockedObject(p), Consumer(this), m_id(p.id),
    m_virtual_networks(p.virt_nets), m_vc_per_vnet(0),
    m_vc_allocator(m_virtual_networks, 0),
    m_deadlock_threshold(p.garnet_deadlock_threshold),
    m_use_escape_vns(p.use_escape_vns),
    vc_busy_counter(m_virtual_networks, 0)
{
    m_stall_count.resize(m_virtual_networks);
    niOutVcs.resize(0);

    // for sankey
    m_post_dlock=false;
}

void
NetworkInterface::addInPort(NetworkLink *in_link,
                              CreditLink *credit_link)
{
    InputPort *newInPort = new InputPort(in_link, credit_link);
    inPorts.push_back(newInPort);
    // DPRINTF(RubyNetwork, "Adding input port:%s with vnets %s\n",
    // in_link->name(), newInPort->printVnets());

    in_link->setLinkConsumer(this);
    credit_link->setSourceQueue(newInPort->outCreditQueue(), this);
    if (m_vc_per_vnet != 0) {
        in_link->setVcsPerVnet(m_vc_per_vnet);
        credit_link->setVcsPerVnet(m_vc_per_vnet);
    }

}

void
NetworkInterface::addOutPort(NetworkLink *out_link,
                             CreditLink *credit_link,
                             SwitchID router_id, uint32_t consumerVcs)
{
    OutputPort *newOutPort = new OutputPort(out_link, credit_link, router_id);
    outPorts.push_back(newOutPort);

    assert(consumerVcs > 0);
    // We are not allowing different physical links to have different vcs
    // If it is required that the Network Interface support different VCs
    // for every physical link connected to it. Then they need to change
    // the logic within outport and inport.
    if (niOutVcs.size() == 0) {
        m_vc_per_vnet = consumerVcs;
        int m_num_vcs = consumerVcs * m_virtual_networks;
        niOutVcs.resize(m_num_vcs);
        outVcState.reserve(m_num_vcs);
        m_ni_out_vcs_enqueue_time.resize(m_num_vcs);
        // instantiating the NI flit buffers
        for (int i = 0; i < m_num_vcs; i++) {
            m_ni_out_vcs_enqueue_time[i] = Tick(INFINITE_);
            outVcState.emplace_back(i, m_net_ptr, consumerVcs);
        }

        // Reset VC Per VNET for input links already instantiated
        for (auto &iPort: inPorts) {
            NetworkLink *inNetLink = iPort->inNetLink();
            inNetLink->setVcsPerVnet(m_vc_per_vnet);
            credit_link->setVcsPerVnet(m_vc_per_vnet);
        }
    } else {
        fatal_if(consumerVcs != m_vc_per_vnet,
        "%s: Connected Physical links have different vc requests: %d and %d\n",
        name(), consumerVcs, m_vc_per_vnet);
    }

    // DPRINTF(RubyNetwork, "OutputPort:%s Vnet: %s\n",
    // out_link->name(), newOutPort->printVnets());

    out_link->setSourceQueue(newOutPort->outFlitQueue(), this);
    out_link->setVcsPerVnet(m_vc_per_vnet);
    credit_link->setLinkConsumer(this);
    credit_link->setVcsPerVnet(m_vc_per_vnet);
}

void
NetworkInterface::addNode(std::vector<MessageBuffer *>& in,
                          std::vector<MessageBuffer *>& out)
{
    inNode_ptr = in;
    outNode_ptr = out;

    for (auto& it : in) {
        if (it != nullptr) {
            it->setConsumer(this);
        }
    }
}

void
NetworkInterface::dequeueCallback()
{
    // An output MessageBuffer has dequeued something this cycle and there
    // is now space to enqueue a stalled message. However, we cannot wake
    // on the same cycle as the dequeue. Schedule a wake at the soonest
    // possible time (next cycle).
    scheduleEventAbsolute(clockEdge(Cycles(1)));
}

void
NetworkInterface::incrementStats(flit *t_flit)
{
    int vnet = t_flit->get_vnet();

    // Latency
    m_net_ptr->increment_received_flits(vnet);
    Tick network_delay =
        t_flit->get_dequeue_time() -
        t_flit->get_enqueue_time() - cyclesToTicks(Cycles(1));
    Tick src_queueing_delay = t_flit->get_src_delay();
    Tick dest_queueing_delay = (curTick() - t_flit->get_dequeue_time());
    Tick queueing_delay = src_queueing_delay + dest_queueing_delay;

    m_net_ptr->increment_flit_network_latency(network_delay, vnet);
    m_net_ptr->increment_flit_queueing_latency(queueing_delay, vnet);

    if (t_flit->get_type() == TAIL_ || t_flit->get_type() == HEAD_TAIL_) {
        m_net_ptr->increment_received_packets(vnet);
        m_net_ptr->increment_packet_network_latency(network_delay, vnet);
        m_net_ptr->increment_packet_queueing_latency(queueing_delay, vnet);
    }

    // Hops
    m_net_ptr->increment_total_hops(t_flit->get_route().hops_traversed);

    // for Sankey tracking

    // get src/first and dest/last VNs
    int src_vn = t_flit->get_first_vnvc();
    int dest_vn = t_flit->get_last_vnvc();

    // track in 2d matrix the src, dest VC/VNs
    m_net_ptr->increment_sankey(src_vn, dest_vn);

    int r_id = get_router_id(vnet);
    bool after_dlock = m_net_ptr->get_post_dlock_of_router(r_id);
    if(after_dlock){
        m_net_ptr->increment_dlock_sankey(src_vn, dest_vn);
        RouteInfo this_route = t_flit->get_route();
        int src_r = this_route.src_router;
        int dest_r = this_route.dest_router;
        m_net_ptr->increment_dlock_srcdest(src_r, dest_r);
    }
}

/*
 * The NI wakeup checks whether there are any ready messages in the protocol
 * buffer. If yes, it picks that up, flitisizes it into a number of flits and
 * puts it into an output buffer and schedules the output link. On a wakeup
 * it also checks whether there are flits in the input link. If yes, it picks
 * them up and if the flit is a tail, the NI inserts the corresponding message
 * into the protocol buffer. It also checks for credits being sent by the
 * downstream router.
 */

void
NetworkInterface::wakeup()
{
    std::ostringstream oss;
    for (auto &oPort: outPorts) {
        oss << oPort->routerID() << "[" << oPort->printVnets() << "] ";
    }
    DPRINTF(RubyNetwork, "Network Interface %d connected to router:%s "
            "woke up. Period: %ld\n", m_id, oss.str(), clockPeriod());

    // printf("Woke up in NI %d\n",m_id);

    assert(curTick() == clockEdge());
    MsgPtr msg_ptr;
    Tick curTime = clockEdge();

    // Checking for messages coming from the protocol
    // can pick up a message/cycle for each virtual net
    for (int vnet = 0; vnet < inNode_ptr.size(); ++vnet) {
        MessageBuffer *b = inNode_ptr[vnet];
        if (b == nullptr) {
            continue;
        }

        if (b->isReady(curTime)) { // Is there a message waiting
            msg_ptr = b->peekMsgPtr();
            if (flitisizeMessage(msg_ptr, vnet)) {
                b->dequeue(curTime);
            }
        }
    }

    scheduleOutputLink();

    // Check if there are flits stalling a virtual channel. Track if a
    // message is enqueued to restrict ejection to one message per cycle.
    checkStallQueue();

    /*********** Check the incoming flit link **********/
    DPRINTF(RubyNetwork, "Number of input ports: %d\n", inPorts.size());
    for (auto &iPort: inPorts) {
        NetworkLink *inNetLink = iPort->inNetLink();
        if (inNetLink->isReady(curTick())) {
            flit *t_flit = inNetLink->consumeLink();
            DPRINTF(RubyNetwork, "NI Recieved flit:%s\n", *t_flit);
            assert(t_flit->m_width == iPort->bitWidth());

            int vnet = t_flit->get_vnet();
            t_flit->set_dequeue_time(curTick());

            MessageBuffer * temp = outNode_ptr[vnet];

            bool slots_avail = temp->areNSlotsAvailable(1, curTime);



            // If a tail flit is received, enqueue into the protocol buffers
            // if space is available. Otherwise, exchange non-tail flits for
            // credits.
            if (t_flit->get_type() == TAIL_ ||
                t_flit->get_type() == HEAD_TAIL_) {
                if (!iPort->messageEnqueuedThisCycle &&
                    outNode_ptr[vnet]->areNSlotsAvailable(1, curTime)) {

                    // outNode_ptr[vnet]->areNSlotsAvailable(1, curTime) causing seg fault

                    // Space is available. Enqueue to protocol buffer.
                    outNode_ptr[vnet]->enqueue(t_flit->get_msg_ptr(), curTime,
                                               cyclesToTicks(Cycles(1)));

                    // Simply send a credit back since we are not buffering
                    // this flit in the NI
                    Credit *cFlit = new Credit(t_flit->get_vc(),
                                               true, curTick());
                    iPort->sendCredit(cFlit);
                    // Update stats and delete flit pointer
                    incrementStats(t_flit);
                    delete t_flit;
                } else {
                    // No space available- Place tail flit in stall queue and
                    // set up a callback for when protocol buffer is dequeued.
                    // Stat update and flit pointer deletion will occur upon
                    // unstall.
                    iPort->m_stall_queue.push_back(t_flit);
                    m_stall_count[vnet]++;

                    outNode_ptr[vnet]->registerDequeueCallback([this]() {
                        dequeueCallback(); });
                }
            } else {
                // Non-tail flit. Send back a credit but not VC free signal.
                Credit *cFlit = new Credit(t_flit->get_vc(), false,
                                               curTick());
                // Simply send a credit back since we are not buffering
                // this flit in the NI
                iPort->sendCredit(cFlit);

                // Update stats and delete flit pointer.
                incrementStats(t_flit);
                delete t_flit;
            }
        }
    }

    DPRINTF(RubyNetwork, "Completed iteration of input ports\n");

    /****************** Check the incoming credit link *******/

    for (auto &oPort: outPorts) {
        CreditLink *inCreditLink = oPort->inCreditLink();
        if (inCreditLink->isReady(curTick())) {
            Credit *t_credit = (Credit*) inCreditLink->consumeLink();
            outVcState[t_credit->get_vc()].increment_credit();
            if (t_credit->is_free_signal()) {
                outVcState[t_credit->get_vc()].setState(IDLE_,
                    curTick());
            }
            delete t_credit;
        }
    }


    // It is possible to enqueue multiple outgoing credit flits if a message
    // was unstalled in the same cycle as a new message arrives. In this
    // case, we should schedule another wakeup to ensure the credit is sent
    // back.
    for (auto &iPort: inPorts) {
        if (iPort->outCreditQueue()->getSize() > 0) {
            DPRINTF(RubyNetwork, "Sending a credit %s via %s at %ld\n",
            *(iPort->outCreditQueue()->peekTopFlit()),
            iPort->outCreditLink()->name(), clockEdge(Cycles(1)));
            iPort->outCreditLink()->
                scheduleEventAbsolute(clockEdge(Cycles(1)));
        }
    }
    checkReschedule();
}

void
NetworkInterface::checkStallQueue()
{
    // Check all stall queues.
    // There is one stall queue for each input link
    for (auto &iPort: inPorts) {
        iPort->messageEnqueuedThisCycle = false;
        Tick curTime = clockEdge();

        if (!iPort->m_stall_queue.empty()) {
            for (auto stallIter = iPort->m_stall_queue.begin();
                 stallIter != iPort->m_stall_queue.end(); ) {
                flit *stallFlit = *stallIter;
                int vnet = stallFlit->get_vnet();

                // If we can now eject to the protocol buffer,
                // send back credits
                if (outNode_ptr[vnet]->areNSlotsAvailable(1,
                    curTime)) {
                    outNode_ptr[vnet]->enqueue(stallFlit->get_msg_ptr(),
                        curTime, cyclesToTicks(Cycles(1)));

                    // Send back a credit with free signal now that the
                    // VC is no longer stalled.
                    Credit *cFlit = new Credit(stallFlit->get_vc(), true,
                                                   curTick());
                    iPort->sendCredit(cFlit);

                    // Update Stats
                    incrementStats(stallFlit);

                    // Flit can now safely be deleted and removed from stall
                    // queue
                    delete stallFlit;
                    iPort->m_stall_queue.erase(stallIter);
                    m_stall_count[vnet]--;

                    // If there are no more stalled messages for this vnet, the
                    // callback on it's MessageBuffer is not needed.
                    if (m_stall_count[vnet] == 0)
                        outNode_ptr[vnet]->unregisterDequeueCallback();

                    iPort->messageEnqueuedThisCycle = true;
                    break;
                } else {
                    ++stallIter;
                }
            }
        }
    }
}

// Embed the protocol message into flits
bool
NetworkInterface::flitisizeMessage(MsgPtr msg_ptr, int vnet)
{
    Message *net_msg_ptr = msg_ptr.get();
    NetDest net_msg_dest = net_msg_ptr->getDestination();

    // gets all the destinations associated with this message.
    std::vector<NodeID> dest_nodes = net_msg_dest.getAllDest();

    // Number of flits is dependent on the link bandwidth available.
    // This is expressed in terms of bytes/cycle or the flit size
    OutputPort *oPort = getOutportForVnet(vnet);
    assert(oPort);
    int num_flits = (int)divCeil((float) m_net_ptr->MessageSizeType_to_int(
        net_msg_ptr->getMessageSize()), (float)oPort->bitWidth());

    DPRINTF(RubyNetwork, "Message Size:%d vnet:%d bitWidth:%d\n",
        m_net_ptr->MessageSizeType_to_int(net_msg_ptr->getMessageSize()),
        vnet, oPort->bitWidth());

    // loop to convert all multicast messages into unicast messages
    for (int ctr = 0; ctr < dest_nodes.size(); ctr++) {

        int src_r = 0;
        int dest_r = 0;

        // this will return a free output virtual channel
        int vc;
        if(m_use_escape_vns){

            // use src, dest routers to decide evn_class
    
            // get original source. Its the router attacked to this
            src_r = oPort->routerID();

            NodeID destID = dest_nodes[ctr];
            dest_r = m_net_ptr->get_router_id(destID, vnet);

            int evn_class = m_net_ptr->get_evn_for_src_dest(src_r, dest_r);


            vc = calculate_valid_evn(vnet, evn_class);
            DPRINTF(RubyNetwork, "NetworkInterface:: flitisizeMessage():: Calculated valid VC %d for evn_class %d (%d->...->%d)\n",
                vc,evn_class,src_r,dest_r);
        }   
        else{
            vc = calculateVC(vnet);
            DPRINTF(RubyNetwork, "NetworkInterface:: flitisizeMessage():: Calculated any VC %d\n",
                vc);
        }

        if (vc == -1) {
            m_net_ptr->increment_ni_rejected(src_r,dest_r);
            return false ;
        }
        MsgPtr new_msg_ptr = msg_ptr->clone();
        NodeID destID = dest_nodes[ctr];

        Message *new_net_msg_ptr = new_msg_ptr.get();
        if (dest_nodes.size() > 1) {
            NetDest personal_dest;
            for (int m = 0; m < (int) MachineType_NUM; m++) {
                if ((destID >= MachineType_base_number((MachineType) m)) &&
                    destID < MachineType_base_number((MachineType) (m+1))) {
                    // calculating the NetDest associated with this destID
                    personal_dest.clear();
                    personal_dest.add((MachineID) {(MachineType) m, (destID -
                        MachineType_base_number((MachineType) m))});
                    new_net_msg_ptr->getDestination() = personal_dest;
                    break;
                }
            }
            net_msg_dest.removeNetDest(personal_dest);
            // removing the destination from the original message to reflect
            // that a message with this particular destination has been
            // flitisized and an output vc is acquired
            net_msg_ptr->getDestination().removeNetDest(personal_dest);
        }

        // Embed Route into the flits
        // NetDest format is used by the routing table
        // Custom routing algorithms just need destID

        RouteInfo route;
        route.vnet = vnet;
        route.net_dest = new_net_msg_ptr->getDestination();
        route.src_ni = m_id;
        route.src_router = oPort->routerID();
        route.dest_ni = destID;
        route.dest_router = m_net_ptr->get_router_id(destID, vnet);

        // initialize hops_traversed to -1
        // so that the first router increments it to 0
        route.hops_traversed = -1;

        m_net_ptr->increment_injected_packets(vnet);
        m_net_ptr->update_traffic_distribution(route);
        int packet_id = m_net_ptr->getNextPacketID();
        for (int i = 0; i < num_flits; i++) {
            m_net_ptr->increment_injected_flits(vnet);
            flit *fl = new flit(packet_id,
                i, vc, vnet, route, num_flits, new_msg_ptr,
                m_net_ptr->MessageSizeType_to_int(
                net_msg_ptr->getMessageSize()),
                oPort->bitWidth(), curTick());

            DPRINTF(RubyNetwork,"fl is %s\n",*fl);

            fl->set_src_delay(curTick() - msg_ptr->getTime());
            niOutVcs[vc].insert(fl);

            // for Sankey
            fl->set_first_vnvc(vc);
            fl->set_last_vnvc(vc);
        }

        m_ni_out_vcs_enqueue_time[vc] = curTick();
        outVcState[vc].setState(ACTIVE_, curTick());
    }
    DPRINTF(RubyNetwork,"Completed flitisizing\n");
    return true ;
}

int 
NetworkInterface::calculate_valid_evn(int vnet, int evn_class)
{
    // absolute vc across all req/resp type VNs
    int abs_vc_base = vnet*m_vc_per_vnet;

    // rel vc val that is base of DL free
    // ie for evn_class, DL free vcs are [class_rel_vc_base,class_rel_vc_bound)
    int class_rel_vc_base = m_evn_deadlock_partition + evn_class*m_n_deadlock_free;
    int class_rel_vc_bound = class_rel_vc_base + m_n_deadlock_free;


    // update m_vc_allocator to point to the correct vc for evn_class
    // if in DL free section, point to first vc for class
    // removes need for complex rollover in loop

    if (m_vc_allocator[vnet] >= m_evn_deadlock_partition){
        m_vc_allocator[vnet] = class_rel_vc_base;
    }

    // save initial vc for breaking from loop
    int first_check = m_vc_allocator[vnet];

    bool is_idle = false;

    DPRINTF(RubyNetwork, "evn_class %d and dl_part %d\n",evn_class, m_evn_deadlock_partition);

    for (int i = 0; i < m_vc_per_vnet; i++) {
        
        // get delta
        int delta = m_vc_allocator[vnet];

        // simple update m_vc_allocator
        m_vc_allocator[vnet]++;
        if (m_vc_allocator[vnet] == m_vc_per_vnet){
            DPRINTF(RubyNetwork, "rollover %d->0\n",m_vc_allocator[vnet]);
            m_vc_allocator[vnet] = 0;
        }

        DPRINTF(RubyNetwork, "delta = %d and first = %d (abs %d)\n",delta,first_check, abs_vc_base + first_check);

        // if delta not valid (ie wrong DL free for this evn_class)
        //  then continue loop
        // wrong if dl_part <= delta (in DL free zone) and delta < class_rel_vc_base or delta >= class_rel_vc_bound
        if ( delta >= m_evn_deadlock_partition ){
            // if below or above valid range
            if((delta < class_rel_vc_base) || (delta >= class_rel_vc_bound)){
                continue;
            }
        }

        // check if idle
        DPRINTF(RubyNetwork, "Checking if vc %d (abs %d) available/idle\n",delta, abs_vc_base + delta);

        is_idle = outVcState[abs_vc_base + delta].isInState(IDLE_, curTick());
        DPRINTF(RubyNetwork, "idle? %d\n",is_idle);



        // complex rollover
        // if we will exit and vc_alloc is in DL free set
        //  then set up vc_allocator to point to first DL free
        // if((is_idle || m_vc_allocator[vnet] == first_check) 
        //     && (m_vc_allocator[vnet] >= m_evn_deadlock_partition)){
        //     m_vc_allocator[vnet] = m_evn_deadlock_partition;
        // }

        // break conditions
        //  if idle
        //      then found solution and exit early via return
        //  if m_vc_allocator == first
        //      then have checked everything and exit via break (so it increments busy counter)
        if (is_idle) {
            DPRINTF(RubyNetwork, "%d idle. returning\n",delta);
            // update busy counter
            vc_busy_counter[vnet] = 0;
            return (abs_vc_base + delta);
        }

        // technically not necessary. all loops should be valid
        if (m_vc_allocator[vnet] == first_check){
            DPRINTF(RubyNetwork, "vc_alloc %d returning to first_check %d. breaking\n",m_vc_allocator[vnet], first_check);
            break;
        }

    }



    vc_busy_counter[vnet] += 1;
    // panic_if(vc_busy_counter[vnet] > m_deadlock_threshold,
    //      "%s: Possible network deadlock in vnet: %d, evn_class %d, at time: %llu \n",
    //      name(), vnet,evn_class , curTick());
    if (vc_busy_counter[vnet] > m_deadlock_threshold){
        printf("Possible network deadlock in vnet: %d, evn_class %d, at time: %lu in NI %d and router %d \n",
            vnet,evn_class , curTick(), m_id, get_router_id(vnet));
        m_post_dlock = true;
        int r_id = get_router_id(vnet);
        m_net_ptr->set_post_dlock_of_router(r_id);

        m_deadlock_threshold = 2*m_deadlock_threshold;
        printf("post_dlock=%d and dlock thresh=%d in NI %d\n",m_post_dlock,m_deadlock_threshold,m_id);
    }

    // panic_if(2*vc_busy_counter[vnet] >= m_deadlock_threshold,
    //     "%s: Possible network deadlock in vnet: %d, evn_class %d, at time: %llu \n",
    //     name(), vnet,evn_class , curTick());

    return -1;

}


// int 
// NetworkInterface::calculate_valid_evn(int vnet, int evn_class)
// {
//     // absolute vc across all req/resp type VNs
//     int abs_vc_base = vnet*m_vc_per_vnet;

//     // check the no guarantee VCs
//     // [0,m_evn_deadlock_partition)
//     for (int i = 0; i < m_evn_deadlock_partition; i++) {
//         int delta = m_vc_allocator[vnet];
//         m_vc_allocator[vnet]++;

//         DPRINTF(RubyNetwork, "First no guarantee. Checking if vc %d (abs %d) available/idle\n",delta, abs_vc_base + delta);

//         // rollover
//         // m_vc_allocator[vnet] elem of [0,m_evn_deadlock_partition)
//         if (m_vc_allocator[vnet] == m_evn_deadlock_partition){
//             m_vc_allocator[vnet] = 0;
//             DPRINTF(RubyNetwork, "rollover\n",abs_vc_base + delta);
//         }


//         if (outVcState[abs_vc_base + delta].isInState(
//                     IDLE_, curTick())) {
//             vc_busy_counter[vnet] = 0;
//             return (abs_vc_base + delta);
//         }

//         // rollover break
//         // // 0 => just rolled over
//         if (m_vc_allocator[vnet] == 0){
//             DPRINTF(RubyNetwork, "rollover break\n",abs_vc_base + delta);
//             break;
//         }


//     }

//     // else, check DL-free escape VNs

//     // DL-free VNs are blocked
//     // class 0 : [m_evn_deadlock_partition, m_evn_deadlock_partition + m_n_deadlock_free)
//     // class 1 : [m_evn_deadlock_partition + m_n_deadlock_free, m_evn_deadlock_partition + 2*m_n_deadlock_free)
//     // ...

//     // this_class (arg) : [m_evn_deadlock_partition + evn_class*m_n_deadlock_free, m_evn_deadlock_partition + (evn_class + 1)*m_n_deadlock_free)

//     // iter through all avail
//     // will be m_n_deadlock_free for this class

//     int class_rel_vc_base = m_evn_deadlock_partition + evn_class*m_n_deadlock_free;

//     for(int i = 0; i < m_n_deadlock_free; i++){

//         // continue;

//         // dont do round-robin. it gets weird with the different eVNs
//         // just check through this class' options
//         int delta = class_rel_vc_base + i;

//         DPRINTF(RubyNetwork, "Checking if DL free vc %d (abs %d) available/idle\n",delta, abs_vc_base + delta);

//         // delta is relative vc
//         if (outVcState[abs_vc_base + delta].isInState(
//                     IDLE_, curTick())) {
//             vc_busy_counter[vnet] = 0;
//             return (abs_vc_base + delta);
//         }

//     }

//     // recheck no guarantees
//     // check the no guarantee VCs
//     // [0,m_evn_deadlock_partition)
//     for (int i = 0; i < m_evn_deadlock_partition; i++) {
//         int delta = m_vc_allocator[vnet];
//         m_vc_allocator[vnet]++;

//         DPRINTF(RubyNetwork, "Second no guarantee. Checking if vc %d (abs %d) available/idle\n",delta, abs_vc_base + delta);

//         // rollover
//         // m_vc_allocator[vnet] elem of [0,m_evn_deadlock_partition)
//         if (m_vc_allocator[vnet] == m_evn_deadlock_partition){
//             DPRINTF(RubyNetwork, "rollover\n",abs_vc_base + delta);
//             m_vc_allocator[vnet] = 0;
//         }

//         if (outVcState[abs_vc_base + delta].isInState(
//                     IDLE_, curTick())) {
//             vc_busy_counter[vnet] = 0;
//             return (abs_vc_base + delta);
//         }

//         // rollover break
//         // 0 => just rolled over
//         if (m_vc_allocator[vnet] == 0){
//             DPRINTF(RubyNetwork, "rollover break\n",abs_vc_base + delta);
//             break;
//         }

//     }



//     vc_busy_counter[vnet] += 1;
//     // panic_if(vc_busy_counter[vnet] > m_deadlock_threshold,
//     //     "%s: Possible network deadlock in vnet: %d, evn_class %d, at time: %llu \n",
//     //     name(), vnet,evn_class , curTick());
//     if (vc_busy_counter[vnet] > m_deadlock_threshold){
//         printf("Possible network deadlock in vnet: %d, evn_class %d, at time: %lu in NI %d and router %d \n",
//             vnet,evn_class , curTick(), m_id, get_router_id(vnet));
//         m_post_dlock = true;
//         int r_id = get_router_id(vnet);
//         m_net_ptr->set_post_dlock_of_router(r_id);

//         m_deadlock_threshold = 2*m_deadlock_threshold;
//         printf("post_dlock=%d and dlock thresh=%d in NI %d\n",m_post_dlock,m_deadlock_threshold,m_id);
//     }

//     return -1;

// }

// Looking for a free output vc
int
NetworkInterface::calculateVC(int vnet)
{
    for (int i = 0; i < m_vc_per_vnet; i++) {
        int delta = m_vc_allocator[vnet];
        m_vc_allocator[vnet]++;
        if (m_vc_allocator[vnet] == m_vc_per_vnet)
            m_vc_allocator[vnet] = 0;

        if (outVcState[(vnet*m_vc_per_vnet) + delta].isInState(
                    IDLE_, curTick())) {
            vc_busy_counter[vnet] = 0;
            return ((vnet*m_vc_per_vnet) + delta);
        }
    }

    vc_busy_counter[vnet] += 1;
    panic_if(vc_busy_counter[vnet] > m_deadlock_threshold,
        "%s: Possible network deadlock in vnet: %d at time: %llu \n",
        name(), vnet, curTick());

    return -1;
}

void
NetworkInterface::scheduleOutputPort(OutputPort *oPort)
{
   int vc = oPort->vcRoundRobin();

   for (int i = 0; i < niOutVcs.size(); i++) {
       vc++;
       if (vc == niOutVcs.size())
           vc = 0;

       int t_vnet = get_vnet(vc);
       if (oPort->isVnetSupported(t_vnet)) {
           // model buffer backpressure
           if (niOutVcs[vc].isReady(curTick()) &&
               outVcState[vc].has_credit()) {

               bool is_candidate_vc = true;
               int vc_base = t_vnet * m_vc_per_vnet;

               if (m_net_ptr->isVNetOrdered(t_vnet)) {
                   for (int vc_offset = 0; vc_offset < m_vc_per_vnet;
                        vc_offset++) {
                       int t_vc = vc_base + vc_offset;
                       if (niOutVcs[t_vc].isReady(curTick())) {
                           if (m_ni_out_vcs_enqueue_time[t_vc] <
                               m_ni_out_vcs_enqueue_time[vc]) {
                               is_candidate_vc = false;
                               break;
                           }
                       }
                   }
                }


                int rel_vc = vc - vc_base;

                bool restricted_to_escape = false;

                if(rel_vc >= m_evn_deadlock_partition) restricted_to_escape = true;

                bool has_top_flit = true;

                if (oPort->hasTopFlit()){
                    // DPRINTF(RubyNetwork,"\t\t\tNo top flit for VC %d\n",
                    //     vc);
                    has_top_flit = false;
                }

                if (restricted_to_escape && m_use_escape_vns && has_top_flit){



                    // TODO: possibly here check if VC and flit valid?
                    flit* peeked_flit = niOutVcs[vc].peekTopFlit();

                    // check if valid...
                    RouteInfo ri = peeked_flit->get_route();
                    int src_r = ri.src_router;
                    int dest_r = ri.dest_router;

                    int evn_class = m_net_ptr->get_evn_for_src_dest(src_r, dest_r);


                    // allowed if rel_vc elem of [partition + class*n_per_class,partition + (class+1)*n_per_class)
                    int valid_low_bound = m_evn_deadlock_partition + evn_class*m_n_deadlock_free;
                    int valid_high_bound = valid_low_bound + m_n_deadlock_free;

                    if(rel_vc < valid_low_bound || rel_vc >= valid_high_bound){
                        DPRINTF(RubyNetwork, "scheduleOutputPort():: Trying to schedule an invalid VC %d when class=%d for %d->...->%d\n",
                            vc, evn_class, src_r, dest_r);
                    }
                    else{
                        DPRINTF(RubyNetwork, "scheduleOutputPort():: Trying to schedule a valid VC %d when class=%d for %d->...->%d\n",
                            vc, evn_class, src_r, dest_r);
                    }
                }
                else{
                    DPRINTF(RubyNetwork, "scheduleOutputPort():: Trying to schedule a NOT escape VC %d\n",vc);
                }

                DPRINTF(RubyNetwork,"scheduleOutputPort():: Trying to schedule VC %d\n",vc);


                if (!is_candidate_vc)
                    continue;

                // Update the round robin arbiter
                oPort->vcRoundRobin(vc);

                outVcState[vc].decrement_credit();

                // Just removing the top flit
                flit *t_flit = niOutVcs[vc].getTopFlit();
                t_flit->set_time(clockEdge(Cycles(1)));

                // Scheduling the flit
                scheduleFlit(t_flit);

                if (t_flit->get_type() == TAIL_ ||
                    t_flit->get_type() == HEAD_TAIL_) {
                    m_ni_out_vcs_enqueue_time[vc] = Tick(INFINITE_);
                }

                // Done with this port, continue to schedule
                // other ports
                return;
            }
        }
    }
}



/** This function looks at the NI buffers
 *  if some buffer has flits which are ready to traverse the link in the next
 *  cycle, and the downstream output vc associated with this flit has buffers
 *  left, the link is scheduled for the next cycle
 */

void
NetworkInterface::scheduleOutputLink()
{
    // Schedule each output link
    for (auto &oPort: outPorts) {
        scheduleOutputPort(oPort);
    }
}

NetworkInterface::InputPort *
NetworkInterface::getInportForVnet(int vnet)
{
    for (auto &iPort : inPorts) {
        if (iPort->isVnetSupported(vnet)) {
            return iPort;
        }
    }

    return nullptr;
}

/*
 * This function returns the outport which supports the given vnet.
 * Currently, HeteroGarnet does not support multiple outports to
 * support same vnet. Thus, this function returns the first-and
 * only outport which supports the vnet.
 */
NetworkInterface::OutputPort *
NetworkInterface::getOutportForVnet(int vnet)
{
    for (auto &oPort : outPorts) {
        if (oPort->isVnetSupported(vnet)) {
            return oPort;
        }
    }

    return nullptr;
}
void
NetworkInterface::scheduleFlit(flit *t_flit)
{
    OutputPort *oPort = getOutportForVnet(t_flit->get_vnet());

    if (oPort) {
        DPRINTF(RubyNetwork, "Scheduling at %s time:%ld flit:%s Message:%s\n",
        oPort->outNetLink()->name(), clockEdge(Cycles(1)),
        *t_flit, *(t_flit->get_msg_ptr()));
        oPort->outFlitQueue()->insert(t_flit);
        oPort->outNetLink()->scheduleEventAbsolute(clockEdge(Cycles(1)));
        return;
    }

    panic("No output port found for vnet:%d\n", t_flit->get_vnet());
    return;
}

int
NetworkInterface::get_vnet(int vc)
{
    for (int i = 0; i < m_virtual_networks; i++) {
        if (vc >= (i*m_vc_per_vnet) && vc < ((i+1)*m_vc_per_vnet)) {
            return i;
        }
    }
    fatal("Could not determine vc");
}


// Wakeup the NI in the next cycle if there are waiting
// messages in the protocol buffer, or waiting flits in the
// output VC buffer.
// Also check if we have to reschedule because of a clock period
// difference.
void
NetworkInterface::checkReschedule()
{
    for (const auto& it : inNode_ptr) {
        if (it == nullptr) {
            continue;
        }

        while (it->isReady(clockEdge())) { // Is there a message waiting
            scheduleEvent(Cycles(1));
            return;
        }
    }

    for (auto& ni_out_vc : niOutVcs) {
        if (ni_out_vc.isReady(clockEdge(Cycles(1)))) {
            scheduleEvent(Cycles(1));
            return;
        }
    }

    // Check if any input links have flits to be popped.
    // This can happen if the links are operating at
    // a higher frequency.
    for (auto &iPort : inPorts) {
        NetworkLink *inNetLink = iPort->inNetLink();
        if (inNetLink->isReady(curTick())) {
            scheduleEvent(Cycles(1));
            return;
        }
    }

    for (auto &oPort : outPorts) {
        CreditLink *inCreditLink = oPort->inCreditLink();
        if (inCreditLink->isReady(curTick())) {
            scheduleEvent(Cycles(1));
            return;
        }
    }
}

void
NetworkInterface::print(std::ostream& out) const
{
    out << "[Network Interface]";
}

uint32_t
NetworkInterface::functionalWrite(Packet *pkt)
{
    uint32_t num_functional_writes = 0;
    for (auto& ni_out_vc : niOutVcs) {
        num_functional_writes += ni_out_vc.functionalWrite(pkt);
    }

    for (auto &oPort: outPorts) {
        num_functional_writes += oPort->outFlitQueue()->functionalWrite(pkt);
    }
    return num_functional_writes;
}


// void
// NetworkInterface::regStats(){

//     n_routers = m_net_ptr->getNumRouters();

//     for(int s=0; s<n_routers; s++){
//         m_rejected.push_back(
//             std::vector<statistics::Scalar* >() );

//         for(int d=0; d<n_routers; n++){
//             statistics::Scalar* waits = new statistics::Scalar();

//             waits->name(name() + ".nirejected." + "s" +
//                     std::to_string(s) + "." + "d" + std::to_string(d));
//             m_rejected[s].push_back(waits);
//         }

//     }
     
// }

// void
// NetworkInterface::collateStats()
// {
//     //blank
// }

// void
// NetworkInterface::resetStats()
// {
//     //blank
// }


} // namespace garnet
} // namespace ruby
} // namespace gem5
