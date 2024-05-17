/*
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


#include "mem/ruby/network/garnet/OutputUnit.hh"

#include "debug/RubyNetwork.hh"
#include "mem/ruby/network/garnet/Credit.hh"
#include "mem/ruby/network/garnet/CreditLink.hh"
#include "mem/ruby/network/garnet/Router.hh"
#include "mem/ruby/network/garnet/flitBuffer.hh"

namespace gem5
{

namespace ruby
{

namespace garnet
{

OutputUnit::OutputUnit(int id, PortDirection direction, Router *router,
  uint32_t consumerVcs)
  : Consumer(router), m_router(router), m_id(id), m_direction(direction),
    m_vc_per_vnet(consumerVcs)
{
    const int m_num_vcs = consumerVcs * m_router->get_num_vnets();
    outVcState.reserve(m_num_vcs);
    for (int i = 0; i < m_num_vcs; i++) {
        outVcState.emplace_back(i, m_router->get_net_ptr(), consumerVcs);
    }

    // borrow params from router
    m_evn_deadlock_partition = m_router->get_deadlock_partition();
    m_n_deadlock_free = m_router->get_n_deadlock_free();
}

void
OutputUnit::decrement_credit(int out_vc)
{
    DPRINTF(RubyNetwork, "Router %d OutputUnit %s decrementing credit:%d for "
            "outvc %d at time: %lld for %s\n", m_router->get_id(),
            m_router->getPortDirectionName(get_direction()),
            outVcState[out_vc].get_credit_count(),
            out_vc, m_router->curCycle(), m_credit_link->name());

    outVcState[out_vc].decrement_credit();
}

void
OutputUnit::increment_credit(int out_vc)
{
    DPRINTF(RubyNetwork, "Router %d OutputUnit %s incrementing credit:%d for "
            "outvc %d at time: %lld from:%s\n", m_router->get_id(),
            m_router->getPortDirectionName(get_direction()),
            outVcState[out_vc].get_credit_count(),
            out_vc, m_router->curCycle(), m_credit_link->name());

    outVcState[out_vc].increment_credit();
}

// Check if the output VC (i.e., input VC at next router)
// has free credits (i..e, buffer slots).
// This is tracked by OutVcState
bool
OutputUnit::has_credit(int out_vc)
{
    assert(outVcState[out_vc].isInState(ACTIVE_, curTick()));
    return outVcState[out_vc].has_credit();
}


// Check if the output port (i.e., input port at next router) has free VCs.
bool
OutputUnit::has_free_vc(int vnet)
{

    DPRINTF(RubyNetwork, "OutputUnit:: has_free_VC():: in function??\n");

    int vc_base = vnet*m_vc_per_vnet;
    for (int vc = vc_base; vc < vc_base + m_vc_per_vnet; vc++) {
        if (is_vc_idle(vc, curTick()))
            return true;
    }



    return false;
}

// Check if the output port (i.e., input port at next router) has free VCs.
bool
OutputUnit::has_free_valid_evn(int vnet, int evn_class, int current_vc)
{
    // absolute vc across all req/resp type VNs
    int abs_vc_base = vnet*m_vc_per_vnet;


    bool restricted_to_escape = false;

    // assume current_vc is relative

    if (current_vc >= m_evn_deadlock_partition){
        restricted_to_escape = true;
        DPRINTF(RubyNetwork, "OutputUnit:: has_free_valid_evn():: current_vc = %d (abs %d) is in escape VNs ( >= %d)\n", current_vc, current_vc + abs_vc_base, m_evn_deadlock_partition);
    }
    else{
        DPRINTF(RubyNetwork, "OutputUnit:: has_free_valid_evn():: current_vc = %d (abs %d) is NOT in escape VNs ( < %d)\n", current_vc, current_vc + abs_vc_base, m_evn_deadlock_partition);
    }

    // if not currently in an escape VN then
    if (!restricted_to_escape){
        // check the no guarantee VCs
        // [0,m_evn_deadlock_partition)
        for (int i = 0; i < m_evn_deadlock_partition; i++) {
            int vc = abs_vc_base + i;
            DPRINTF(RubyNetwork, "OutputUnit:: has_free_valid_evn():: checking vc = %d\n", vc);
            if (is_vc_idle(vc, curTick()))
                return true;
        }
    }

    // else, check DL-free escape VNs

    // DL-free VNs are blocked
    // class 0 : [m_evn_deadlock_partition, m_evn_deadlock_partition + m_n_deadlock_free)
    // class 1 : [m_evn_deadlock_partition + m_n_deadlock_free, m_evn_deadlock_partition + 2*m_n_deadlock_free)
    // ...

    // this_class (arg) : [m_evn_deadlock_partition + evn_class*m_n_deadlock_free, m_evn_deadlock_partition + (evn_class + 1)*m_n_deadlock_free)

    // iter through all avail
    // will be m_n_deadlock_free for this class

    int class_rel_vc_base = m_evn_deadlock_partition + evn_class*m_n_deadlock_free;

    for(int i = 0; i < m_n_deadlock_free; i++){
        int vc = abs_vc_base + class_rel_vc_base + i;
        DPRINTF(RubyNetwork, "OutputUnit:: has_free_valid_evn():: checking vc = %d\n", vc);
        if (is_vc_idle(vc, curTick()))
            return true;
    }

    return false;
}

// Assign a free output VC to the winner of Switch Allocation
int
OutputUnit::select_free_vc(int vnet)
{
    int vc_base = vnet*m_vc_per_vnet;
    for (int vc = vc_base; vc < vc_base + m_vc_per_vnet; vc++) {
        if (is_vc_idle(vc, curTick())) {
            outVcState[vc].setState(ACTIVE_, curTick());
            return vc;
        }
    }

    return -1;
}

// Check if the output port (i.e., input port at next router) has free VCs.
int
OutputUnit::select_free_valid_evn(int vnet, int evn_class, int current_vc)
{
    // absolute vc across all req/resp type VNs
    int abs_vc_base = vnet*m_vc_per_vnet;


    bool restricted_to_escape = false;

    // assume current_vc is relative

    if (current_vc >= m_evn_deadlock_partition){
        restricted_to_escape = true;
        DPRINTF(RubyNetwork, "OutputUnit:: select_free_valid_evn():: current_vc = %d (abs %d) is in escape VNs ( >= %d)\n", current_vc, current_vc + abs_vc_base, m_evn_deadlock_partition);
    }
    else{
        DPRINTF(RubyNetwork, "OutputUnit:: select_free_valid_evn():: current_vc = %d (abs %d) is NOT in escape VNs ( < %d)\n", current_vc, current_vc + abs_vc_base, m_evn_deadlock_partition);
    }

    // if not currently in an escape VN then
    if (!restricted_to_escape){
        // check the no guarantee VCs
        // [0,m_evn_deadlock_partition)
        for (int i = 0; i < m_evn_deadlock_partition; i++) {
            int vc = abs_vc_base + i;
            if (is_vc_idle(vc, curTick())) {
                outVcState[vc].setState(ACTIVE_, curTick());
                return vc;
            }
        }
    }

    // else, check DL-free escape VNs

    // DL-free VNs are blocked
    // class 0 : [m_evn_deadlock_partition, m_evn_deadlock_partition + m_n_deadlock_free)
    // class 1 : [m_evn_deadlock_partition + m_n_deadlock_free, m_evn_deadlock_partition + 2*m_n_deadlock_free)
    // ...

    // this_class (arg) : [m_evn_deadlock_partition + evn_class*m_n_deadlock_free, m_evn_deadlock_partition + (evn_class + 1)*m_n_deadlock_free)

    // iter through all avail
    // will be m_n_deadlock_free for this class

    int class_rel_vc_base = m_evn_deadlock_partition + evn_class*m_n_deadlock_free;

    DPRINTF(RubyNetwork, "OutputUnit:: select_free_valid_evn():: evn_class %d is restricted to vcs [%d,%d) (abs [%d,%d))", evn_class, class_rel_vc_base, class_rel_vc_base + m_n_deadlock_free, abs_vc_base + class_rel_vc_base, abs_vc_base + class_rel_vc_base + m_n_deadlock_free );

    for(int i = 0; i < m_n_deadlock_free; i++){
        int vc = abs_vc_base + class_rel_vc_base + i;

        if (is_vc_idle(vc, curTick())) {
            outVcState[vc].setState(ACTIVE_, curTick());
            return vc;
        }

    }

    return -1;
}
/*
 * The wakeup function of the OutputUnit reads the credit signal from the
 * downstream router for the output VC (i.e., input VC at downstream router).
 * It increments the credit count in the appropriate output VC state.
 * If the credit carries is_free_signal as true,
 * the output VC is marked IDLE.
 */

void
OutputUnit::wakeup()
{
    if (m_credit_link->isReady(curTick())) {
        Credit *t_credit = (Credit*) m_credit_link->consumeLink();
        increment_credit(t_credit->get_vc());

        if (t_credit->is_free_signal())
            set_vc_state(IDLE_, t_credit->get_vc(), curTick());

        delete t_credit;

        if (m_credit_link->isReady(curTick())) {
            scheduleEvent(Cycles(1));
        }
    }
}

flitBuffer*
OutputUnit::getOutQueue()
{
    return &outBuffer;
}

void
OutputUnit::set_out_link(NetworkLink *link)
{
    m_out_link = link;
}

void
OutputUnit::set_credit_link(CreditLink *credit_link)
{
    m_credit_link = credit_link;
}

void
OutputUnit::insert_flit(flit *t_flit)
{
    outBuffer.insert(t_flit);
    m_out_link->scheduleEventAbsolute(m_router->clockEdge(Cycles(1)));
}

uint32_t
OutputUnit::functionalWrite(Packet *pkt)
{
    return outBuffer.functionalWrite(pkt);
}

Router*
OutputUnit::get_router(){
    return m_router;
}

} // namespace garnet
} // namespace ruby
} // namespace gem5
