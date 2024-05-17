# Copyright (c) 2008 Princeton University
# Copyright (c) 2009 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: Tushar Krishna
#

from m5.params import *
from m5.proxy import *
from m5.objects.Network import RubyNetwork
from m5.objects.BasicRouter import BasicRouter
from m5.objects.ClockedObject import ClockedObject

class GarnetNetwork(RubyNetwork):
    type = 'GarnetNetwork'
    cxx_header = "mem/ruby/network/garnet/GarnetNetwork.hh"
    cxx_class = 'gem5::ruby::garnet::GarnetNetwork'

    num_rows = Param.Int(0, "number of rows if 2D (mesh/torus/..) topology");
    ni_flit_size = Param.UInt32(16, "network interface flit size in bytes")
    vcs_per_vnet = Param.UInt32(4, "virtual channels per virtual network");
    buffers_per_data_vc = Param.UInt32(5, "buffers per data virtual channel");
    buffers_per_ctrl_vc = Param.UInt32(1, "buffers per ctrl virtual channel");
    routing_algorithm = Param.Int(0,
        "0: Weight-based Table, 1: XY, 2: Custom");
    enable_fault_model = Param.Bool(False, "enable network fault model");
    fault_model = Param.FaultModel(NULL, "network fault model");
    garnet_deadlock_threshold = Param.UInt32(50000,
                              "network-level deadlock threshold")

    # auto_top
    # for escape vns
    use_escape_vns = Param.Bool(False, "Whether to use escape VNs")
    n_deadlock_free = Param.Int32(1, "Number of deadlock free VNs per VN class")
    evn_deadlock_partition = Param.Int32(2, "Number of free/no guarantee VNs. Value is equal to first escape VN")
    min_n_deadlock_free = Param.Int32(2, "Minimum number of deadlock free VNs required. Used for assertion")
    # synth_traffic = Param.Bool(Parent.synth_traffic,"Whether this netowrk is serving synthetic traffic. (changes address translation)")

    # same across all routers
    # hardcoded
    # flat_src_dest_to_evn = VectorParam.Int32([0]*400, "2D src, dest indexed => flattened 400 20*src+dest indexed")
    flat_src_dest_to_evn = VectorParam.Int32( [],"2D src, dest indexed => flattened 400 20*src+dest indexed")


class GarnetNetworkInterface(ClockedObject):
    type = 'GarnetNetworkInterface'
    cxx_class = 'gem5::ruby::garnet::NetworkInterface'
    cxx_header = "mem/ruby/network/garnet/NetworkInterface.hh"

    id = Param.UInt32("ID in relation to other network interfaces")
    vcs_per_vnet = Param.UInt32(Parent.vcs_per_vnet,
                             "virtual channels per virtual network")
    virt_nets = Param.UInt32(Parent.number_of_virtual_networks,
                          "number of virtual networks")
    garnet_deadlock_threshold = Param.UInt32(Parent.garnet_deadlock_threshold,
                                      "network-level deadlock threshold")

    use_escape_vns = Param.Bool(Parent.use_escape_vns, "Whether to use escape VNs")
    n_deadlock_free = Param.Int32(Parent.n_deadlock_free, "Number of deadlock free VNs per VN class")
    evn_deadlock_partition = Param.Int32(Parent.evn_deadlock_partition, "Number of free/no guarantee VNs")
    min_n_deadlock_free = Param.Int32(Parent.min_n_deadlock_free, "Minimum number of deadlock free VNs required. Used for assertion")
    synth_traffic = Param.Bool(Parent.synth_traffic,"Whether this netowrk is serving synthetic traffic. Changes address translation")

class GarnetRouter(BasicRouter):
    type = 'GarnetRouter'
    cxx_class = 'gem5::ruby::garnet::Router'
    cxx_header = "mem/ruby/network/garnet/Router.hh"
    vcs_per_vnet = Param.UInt32(Parent.vcs_per_vnet,
                              "virtual channels per virtual network")
    virt_nets = Param.UInt32(Parent.number_of_virtual_networks,
                          "number of virtual networks")
    width = Param.UInt32(Parent.ni_flit_size,
                          "bit width supported by the router")

    # auto_top
    # for escape vns
    use_escape_vns = Param.Bool(Parent.use_escape_vns, "Whether to use escape VNs")
    n_deadlock_free = Param.Int32(Parent.n_deadlock_free, "Number of deadlock free VNs per VN class")
    evn_deadlock_partition = Param.Int32(Parent.evn_deadlock_partition, "Number of free/no guarantee VNs")
    min_n_deadlock_free = Param.Int32(Parent.min_n_deadlock_free, "Minimum number of deadlock free VNs required. Used for assertion")
    synth_traffic = Param.Bool(Parent.synth_traffic,"Whether this netowrk is serving synthetic traffic. Changes address translation")

    # no default size/values
    flat_next_router_map = VectorParam.Int32([],"2D src, dest indexed => flattened 400 20*src+dest indexed")
    flat_src_dest_to_evn = VectorParam.Int32(Parent.flat_src_dest_to_evn, "2D src, dest indexed => flattened 400 20*src+dest indexed")