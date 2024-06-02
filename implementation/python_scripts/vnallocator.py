# Copyright (c) 2024 Purdue University
# All rights reserved.

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

# Authors: Conor Green


'''

Description:
    Allocates virtual networks to a given topology and routing scheme
'''

# std
import argparse
import random
import math
import os
import ast

# venv
import networkx as nx

class VNAllocator:

    verbose = False
    slow  = False

    def __init__(self):

        # # topology vars
        # -------------
        self.filename = None
        self.r_map = None
        self.n_routers = -1
        self.n_links = -1

        # vc params
        # ---------
        # max allowed VCs
        self.vc_thresh = 10
        # min allowed VCs (to make equal amongst topologies)
        self.vc_min = 0
        # max # iterations to get under vc_thresh
        self.max_retries = 5

        # CDG vars
        # --------
        self.channel_to_node_map = {}
        self.node_to_channel_map = {}

        self.cdg_list = None

        # VN vars
        # -------
        self.vn_map = None
        self.allocated_path_list = None

        # path vars
        # ---------
        self.twod_path_list = None
        self.flat_path_list = None
        self.nrl = None

        # file I/O
        # --------
        self.out_vn_map_path_prefix = None


    # instance var stuff
    # ------------------
    def set_path_lists_from_twod(self, pl):
        self.path_list = pl.copy()
        self.flat_path_list = []
        for src, paths_to_dests in enumerate(pl):
            for p in paths_to_dests:
                self.flat_path_list.append(p)

    def set_path_lists_from_flat(self, pl):
        self.flat_path_list = pl.copy()

        nr = math.sqrt(len(pl))
        self.path_list = [[[] for _ in range(nr)] for __ in range(nr)]

        for p in pl:
            src = p[0]
            dest = p[-1]
            self.path_list[src][dest] = p.copy()

    ###################################################################
    # topology stuff

    def ingest_a_map(self, path_name):
        file_name = path_name.split('/')[-1]

        if True:#self.verbose:
            print(f'Ingesting filename = {file_name} ({path_name})')

        this_map = []

        with open(path_name, 'r') as inf:
            for row in inf:
                r_conns = row.split(' ')
                if '\n' in r_conns:
                    r_conns.remove('\n')

                # deal with approximate values (from MIP)
                try:
                    r_conns = [int(elem) for elem in r_conns]

                except:
                    r_conns = [int(float(elem)) for elem in r_conns]

                this_map.append(r_conns)

        # TODO: move to separate seciton?

        # quick sanitization
        n_routers = len(this_map)
        for i in range(n_routers):
            this_map[i][i] = 0


        # assert binary
        for src_map in this_map:
            for conn in src_map:
                # print(f'src map {i} : conn {conn}')
                # assert(conn == 1 or conn == 0)

                # instead make it binary
                if conn > 0.5:
                    conn = 1

        return this_map

    def setup(self, map_path, path_list_path, nrl_path):
        rm = self.ingest_a_map(map_path)
        self.init_topo_vars(rm)
        self.ingest_path_list(path_list_path)


        self.ingest_nrl(nrl_path, self.n_routers)

        print(f'n_routers={self.n_routers}. n_links={self.n_links}')

        # self.assert_path_list_vs_nrl()

    def assert_path_list_vs_nrl(self):

        nrl = self.nrl
        fpl = self.flat_path_list
        nr = self.n_routers

        print(f'nr={nr}')
        print(f'nrl ({len(nrl)})')
        print(f'fpl ({len(fpl)})')

        alternate_twod_paths = self.nrl_to_twodpath(nrl, nr)
        print(f'created alternate 2d paths')
        alternate_flat_paths = self.twod_to_flat(alternate_twod_paths)

        # assert(set(fpl) == set(alternate_flat_paths))
        iter = 0
        for p in fpl:
            if iter % 100 == 0:
                print(f'iter {iter}')
            assert(p in alternate_flat_paths)
            iter += 1

        print(f'path matches nrl')

    def twod_to_flat(self, twod):
        flat = []
        for row in twod:
            for path in row:
                flat.append(path)
        return flat

    def nrl_to_twodpath(self, nrl, n_routers):
        twod_paths = [[[] for _ in range(n_routers)] for __ in range(n_routers)]
        for osrc in range(n_routers):
            for odest in range(n_routers):
                # print(f'constructing path for {osrc}->...->{odest}')

                cur = osrc

                twod_paths[osrc][odest].append(cur)

                while cur != odest:
                    nex = nrl[cur][osrc][odest]
                    twod_paths[osrc][odest].append(nex)
                    cur = nex    

        return twod_paths

    def init_topo_vars(self, r_map):
        self.r_map = r_map.copy()
        nr = len(r_map)
        self.n_routers = nr

        nl = 0
        for p in range(nr):
            for q in range(nr):
                if p==q:
                    continue
                if r_map[p][q] >= 1:
                    nl += 1

        self.n_links = nl

    def ingest_path_list(self, path_name):

        if True:#self.verbose:
            print(f'Ingesting path list {path_name}')

        path_list = []

        with open(path_name, 'r') as inf:
            name = inf.readline()

            for line in inf.readlines():

                # print(f'line (type {type(line)}) = {line}')

                as_list = ast.literal_eval(line)
                clean_as_list = [e for e in as_list]


                # TODO remove 
                # this is hack for bs mesh stuff
                # if int(clean_as_list[-1]) >= 64:
                #     # print(f'bad {clean_as_list}')
                #     continue

                path_list.append(clean_as_list)


        # its flat
        self.flat_path_list = path_list.copy()

    def ingest_nrl(self, nrl_name, n_routers):
        if True:#self.verbose:
            print(f'Ingesting nrl {nrl_name}')
        
        nrl = []
        with open(nrl_name,'r') as inf:

            cur = 0
            i = 0
            nrl.append([])

            for line in inf:
                
                if '_' in line:
                    continue

                line = line.strip('\n')
                line = line.replace('[','')
                line = line.replace(']','')
                # print(f'line = {line}')
                line_split = line.split(' ')
                line_split = [l for l in line_split if '\n' not in l]

                # print(f'nrl={nrl}')

                nrl[cur].append([])
                
                for e in line_split:
                    e = e.strip(',')
                    nrl[cur][-1].append(int(e))

                # print(f'i={i}')

                i += 1
                if i == n_routers:
                    i = 0
                    cur += 1
                    nrl.append([])

        if [] in nrl:
            nrl.remove([])

        # shallow acceptable. local var will not be modified
        self.nrl = nrl.copy()

    ###################################################################
    # CDG stuff

    # IMPORTANT: path_list is flat.
    #           determine src/dest by indexing w/ [0]/[-1]
    def create_a_cdg_from_paths(self, path_list):
        assert(self.n_links != -1)
        assert(self.channel_to_node_map is not None)
        assert(self.node_to_channel_map is not None)

        n_links = self.n_links

        self.channel_number = 0
        cnum1 = 0
        cnum2 = 0

        cdg_adj_list = [[] for _ in range(n_links)]

        # print(f'n_links = {n_links}')e
        # quit()


        for path in path_list:

            # 1/2 node paths cannot have turns
            # theres only one edge

            for i in range(len(path) - 2):
                # print(f'====================\npath={path}')
                # print(f'self.node_to_channel_map={self.node_to_channel_map}')
                src = path[i]
                mid = path[i+1]
                dest = path[i+2]



                channel_name1 = str(src)+":"+str(mid)
                if channel_name1 in self.channel_to_node_map:
                    cnum1 = self.channel_to_node_map[channel_name1]
                else:
                    cnum1 = self.channel_number
                    try:
                        self.node_to_channel_map[cnum1]
                        input(f'overwriting channel number {cnum1} w/ old contents {self.node_to_channel_map[cnum1]}')
                    except:
                        pass
                        # print(f'new channel number {cnum1}')
                    self.channel_to_node_map[channel_name1] = cnum1
                    self.node_to_channel_map[cnum1] = channel_name1
                    self.channel_number += 1
                # print (channel_name1 + "--->" + str(cnum1))
                    # edge_name_dict[src].update({mid:cnum1})

                channel_name2 = str(mid)+":"+str(dest)
                if channel_name2 in self.channel_to_node_map:
                    cnum2 = self.channel_to_node_map[channel_name2]
                else:
                    cnum2 = self.channel_number

                    try:
                        self.node_to_channel_map[cnum2]
                        input(f'overwriting channel number {cnum2} w/ old contents {self.node_to_channel_map[cnum2]}')
                    except:
                        pass
                        # print(f'new channel number {cnum2}')

                    self.channel_to_node_map[channel_name2] = cnum2
                    self.node_to_channel_map[cnum2] = channel_name2
                    self.channel_number += 1
                # print (channel_name2 + "--->" + str(cnum2))
                    # edge_name_dict[mid].update({dest:cnum2})

                if cnum2 in cdg_adj_list[cnum1]:
                    pass                                 # turn already exists in CDG; ignore
                else:
                    cdg_adj_list[cnum1].append(cnum2)    # add turn to CDG

                # input(f'good?')

        if self.verbose:
            print(f'completed creation of cdg from path set')
            self.print_cdg_list([cdg_adj_list])

        # quit()

        return cdg_adj_list.copy()

    # IMPORTANT: path_list is flat.
    #           determine src/dest by indexing w/ [0]/[-1]
    def create_a_cdg_from_paths2(self, path_list, n_links):

        channel_to_node_map = {}
        node_to_channel_map = {}

        channel_number = 0
        cnum1 = 0
        cnum2 = 0

        cdg_adj_list = [[] for _ in range(n_links)]

        for path in path_list:

            # 1/2 node paths cannot have turns
            # theres only one edge

            for i in range(len(path) - 2):
                # print(f'====================\npath={path}')
                src = path[i]
                mid = path[i+1]
                dest = path[i+2]

                channel_name1 = str(src)+":"+str(mid)
                if channel_name1 in channel_to_node_map:
                    cnum1 = channel_to_node_map[channel_name1]
                else:
                    cnum1 = channel_number
                    channel_to_node_map[channel_name1] = cnum1
                    node_to_channel_map[cnum1] = channel_name1
                    channel_number += 1
                # print (channel_name1 + "--->" + str(cnum1))
                    # edge_name_dict[src].update({mid:cnum1})

                channel_name2 = str(mid)+":"+str(dest)
                if channel_name2 in channel_to_node_map:
                    cnum2 = channel_to_node_map[channel_name2]
                else:
                    cnum2 = channel_number
                    channel_to_node_map[channel_name2] = cnum2
                    node_to_channel_map[cnum2] = channel_name2
                    channel_number += 1
                # print (channel_name2 + "--->" + str(cnum2))
                    # edge_name_dict[mid].update({dest:cnum2})

                if cnum2 in cdg_adj_list[cnum1]:
                    pass                                 # turn already exists in CDG; ignore
                else:
                    cdg_adj_list[cnum1].append(cnum2)    # add turn to CDG

        if verbose:
            print(f'completed creation of cdg from path set')
            print_cdg_list([cdg_adj_list])

        # quit()

        return cdg_adj_list.copy()

    def networkx_get_cycle(self, cdg):

        cycle = []

        G = nx.DiGraph()

        for src, depens in enumerate(cdg):
            for dest in depens:
                G.add_edge(src, dest)

        try:
            cycle = list(nx.find_cycle(G))

            if self.verbose:
                print(f'networkx found cycle: {cycle}')
            return cycle

        except:
            return []

    def get_back_edge(self, cdg):

        if self.verbose:
            print(f'checking networkx get_cycle')
        cycle = self.networkx_get_cycle(cdg)
        if self.verbose:
            print(f'cycle={cycle}')
        try:
            # get random edge

            half = len(cycle) // 2
            latter_half = cycle[half:]
            one_turn = random.choice(latter_half)
            # one_turn = random.choice(cycle)

            be = [one_turn[0], one_turn[1]]
        except:
            be = []

        if self.verbose:
            print(f'be={be}')

        return be

    def get_paths_using_be(self, potential_paths, this_be):

        bad_paths = []

        for this_path in potential_paths:

            # cant have cycles
            if len(this_path) <= 2:
                continue

            # list of edges for path
            # e.g. path = [0,1,2,3] => edges [x,y,z] where x=channel_to_node_map['0:1'], y=...
            this_path_edges = []
            for i in range(len(this_path) - 1):
                src = this_path[i]
                dest = this_path[i + 1]
                str_rep = f'{src}:{dest}'
                # print(f'str_rep')
                try:
                    this_edge = self.channel_to_node_map[str_rep]
                    this_path_edges.append(this_edge)

                # unlisted channel
                except Exception as e:

                    # break
                    pass

            # if self.verbose:
            #     print(f'now, this_path_edges={this_path_edges}')

            # determine if path contains the bad back edge
            related_path = False

            for i in range(len(this_path_edges) - 1):
                window = this_path_edges[i:i+2]

                if this_be == window:
                    if self.verbose:
                        print(f'FLAG this_be={this_be} in this paths edges {this_path_edges}')
                    related_path = True

            if related_path:
                if self.verbose:
                    print(f'appending {this_path} (edges {this_path_edges}) to bad_paths={bad_paths}')
                bad_paths.append(this_path)

        return bad_paths

    ###################################################################

    # big worker
    def assign_static_vcs(self):

        print(f'assigning static vcs...')

        # instance vars used
        assert(self.n_links != -1)

        deadlock_free_paths = []
        deadlock_free_paths.append(self.flat_path_list.copy())

        n_deadlock_free_cdgs = 0

        cdg_list = []

        cdg_list.append(
            self.create_a_cdg_from_paths(
                deadlock_free_paths[0] ) )

        while (n_deadlock_free_cdgs < len(cdg_list)):
            # 1) find a back edge from current cdg
            #   no back edge (thus no cycle) => move to next cdg
            # 2) find all paths of this cdg that utilize that back edge/turn
            # 3) remove these paths from this path_list and add to next path list
            # 4) regenerate this cdg and next cdg from this and next path list
            # 5) repeat

            # 1) get back edge from current cdg

            this_cdg = []
            for e in cdg_list[n_deadlock_free_cdgs]:
                this_cdg.append(e)

            # tests all three/four cycle functions
            be = self.get_back_edge(this_cdg)

            # for prints

            in_loop_iter = 0

            completed = []

            while ( len(be) > 0):
                if self.verbose:
                    print(f'# deadlock free {n_deadlock_free_cdgs} :: inner loop iter {in_loop_iter}')
                in_loop_iter += 1

                if in_loop_iter % 100 == 0:
                    print(f'# deadlock free {n_deadlock_free_cdgs} :: inner loop iter {in_loop_iter}')

                # 2) get all paths of this cdg that utilize that be

                # get all paths that correspond to this vc/cdg
                these_paths = []
                for e in deadlock_free_paths[n_deadlock_free_cdgs]:
                    these_paths.append(e)

                # get all other paths in this set that use that back edge
                bad_paths = self.get_paths_using_be(these_paths, be)

                # if n_deadlock_free_cdgs >= 6:
                #     print(f'be={be}')
                #     print(f'bad_paths={bad_paths}')


                # 3) add bad paths to next path list
                # init
                try:
                    _ = deadlock_free_paths[n_deadlock_free_cdgs + 1]
                except:
                    deadlock_free_paths.append([])

                for bp in bad_paths:
                    deadlock_free_paths[n_deadlock_free_cdgs + 1].append(bp)

                # and remove bad paths from current path list
                for bp in bad_paths:
                    if self.verbose:
                        print(f'removing bp={bp}')
                    deadlock_free_paths[n_deadlock_free_cdgs].remove(bp)


                # 4) regenerate this cdg and next cdg from this and next path list

                if self.verbose:
                    print(f'recalculating cdgs {n_deadlock_free_cdgs} and {n_deadlock_free_cdgs + 1}')

                cdg_list[n_deadlock_free_cdgs] = \
                    self.create_a_cdg_from_paths(
                        deadlock_free_paths[n_deadlock_free_cdgs])

                try:
                    cdg_list[n_deadlock_free_cdgs + 1] =\
                        self.create_a_cdg_from_paths(
                            deadlock_free_paths[n_deadlock_free_cdgs + 1])
                except:
                    cdg_list.append(
                        self.create_a_cdg_from_paths(
                            deadlock_free_paths[n_deadlock_free_cdgs + 1])
                        )


                # 5) repeat. recalculate if back edge
                this_cdg = cdg_list[n_deadlock_free_cdgs]

                # tests all three/four cycle functions
                be = self.get_back_edge(this_cdg)

                # if n_deadlock_free_cdgs >= 6:
                #     print(f'be={be}')




            n_deadlock_free_cdgs += 1

            print(f'Completed another cycle. # deadlock free cdgs = {n_deadlock_free_cdgs}')
            print(f'n dl paths = {len(deadlock_free_paths)}')
            print(f'n cdgs = {len(cdg_list)}')

            if self.verbose:
                try:
                    print(f'paths({len(deadlock_free_paths)})=\n\t{deadlock_free_paths}')
                    self.print_cdg_list(cdg_list)

                    for path in deadlock_free_paths[n_deadlock_free_cdgs]:
                        s = path[0]
                        d = path[1]
                        completed.append((s,d))

                    print(f'completed this cycle')
                    for i,pair in enumerate(completed):
                        print(f'{i:02} : {pair}')
                except:
                    pass

            if self.slow:
                input('cont?')

        while len(deadlock_free_paths) < self.vc_min:
            deadlock_free_paths.append([])
            cdg_list.append([])

        # if True:#self.verbose:
        #     # print(f'Completed another cycle. # deadlock free cdgs = {n_deadlock_free_cdgs}')
        #     # print(f'paths({len(deadlock_free_paths)})=\n\t{deadlock_free_paths}')
        #     # self.print_cdg_list(cdg_list)
            # print(f'n dl paths = {len(deadlock_free_paths)}')
            # print(f'n cdgs = {len(cdg_list)}')

        # quit()


        # set other stuff

        self.n_vns = len(deadlock_free_paths)
        self.allocated_path_list = deadlock_free_paths.copy()
        self.set_vn_map_from_path_list()


        # last check
        print(f'Done with vn alloc')
        cdg_list = []
        for pl in self.allocated_path_list:
            cdg_list.append(self.create_a_cdg_from_paths(pl))
        self.assert_deadlock_free(cdg_list)

    def set_vn_map_from_path_list(self):

        all_weights = [self.calc_path_set_weight(pset, 'hops')\
                        for pset in self.allocated_path_list]
        print(f'all_weights={all_weights}')

        assert(self.allocated_path_list is not None)
        assert(self.n_routers != -1)

        nr = self.n_routers
        vm = [[-1 for _ in range(nr)]for __ in range(nr)]

        completed = [[0 for _ in range(nr)]for __ in range(nr)]

        for vn, this_path_list in enumerate(self.allocated_path_list):

            self.assert_pathlist_deadlock_free(this_path_list)

            for path in this_path_list:
                src = path[0]
                dest = path[-1]
                # print(f'{src}->...->{dest}')
                assert(vm[src][dest] == -1)
                vm[src][dest] = vn

                completed[src][dest] = 1
        # for i,row in enumerate(completed):
        #     print(f'{i:02} : {row}')
                
        for i in range(nr):
            vm[i][i] = 0

        # quit()

        self.vn_map = vm

    def output_vn_to_file(self, op):

        with open(op,'w+') as of:
            for row in self.vn_map:
                for e in row:
                    l = f'{e} '
                    of.write(l)
                of.write('\n')
        print(f'Wrote {op}')

        print(f'vn_map ({len(self.vn_map)})=...')
        for i in range(self.n_routers):
            print(f'\t{i} : {self.vn_map[i]}')
        # quit()

        # extra checking lol

        # TODO uncomment

        self.chase_nrl()

    def prune_pathlist(self, oned_pl, vn_map, vn_interest):
        new_pl = []
        for p in oned_pl:
            s = p[0]
            d = p[-1]

            if vn_map[s][d] == vn_interest:
                new_pl.append(p)
        return new_pl

    def translate_cycle(self,cycle):
        for a,b in cycle:
            print(f'{node_to_channel_map[a].split(":")[0]}->',end='')
        print('')

    def chase_nrl(self):
        assert(self.vn_map)
        assert(self.nrl)

        twod_pl = self.nrl_to_twodpath(self.nrl, self.n_routers)
        flat_pl = self.twod_to_flat(twod_pl)

        for vn in range(self.n_vns):
            vnet_pl = self.prune_pathlist(flat_pl, self.vn_map, vn)
            my_cdg = self.create_a_cdg_from_paths2(vnet_pl, self.n_links)


            cycle = self.networkx_get_cycle(my_cdg)

            self.translate_cycle(cycle)

            assert(len(cycle) == 0)

    ###################################################################
    # load balancing

    def calc_path_set_path_weight(self, sp_set):
        return len(sp_set)

    def calc_path_set_hop_weight(self,sp_set):
        w = 0
        for path in sp_set:
            w += self.calc_path_hop_weight(path)
        return w

    def calc_path_hop_weight(self,path):
        w = len(path) - 1
        return w

    # use this
    def calc_path_set_weight(self, sp_set, metric):

        if metric == 'hops':
            return self.calc_path_set_hop_weight(sp_set)
        # elif metric == 'paths':
        return self.calc_path_set_path_weight(sp_set)

    # use this
    def calc_path_weight(self, path, metric):

        if metric == 'hops':
            return self.calc_path_hop_weight(path)
        elif metric == 'paths':
            return 1

    def load_balance(self, metric):

        assert(self.n_vns != -1)
        assert(self.vn_map is not None)
        assert(self.allocated_path_list is not None)

        # exit early
        if metric == 'none':
            return

        # input('about to load balance')
        # self.verbose = True

        # local handles
        n_vns = self.n_vns
        old_path_list = self.allocated_path_list

        paths_per_vn = [len(s) for s in old_path_list]


        # completely local var
        new_allocated_path_list = [[] for _ in range(n_vns)]
        for vn, sp_set in enumerate(old_path_list):
            for p in sp_set:
                new_allocated_path_list[vn].append(p)

        # get weight info before balancing

        all_weights = [self.calc_path_set_weight(pset, metric)\
                        for pset in old_path_list]

        avg_weight = 0
        for w in all_weights:
            avg_weight += w
        avg_weight = avg_weight / n_vns

        if True:#self.verbose:
            print('-'*72)
            print(f'Before load balancing of metric {metric}')
            print(f'\tweights={all_weights} avg={avg_weight}')
            print(f'\tfor {paths_per_vn} paths per vn')

        # input('begin?')

        # donate from 0, 1, 2, 3...
        for donor_vn in range(n_vns):

            donor_path_list = []

            # for all paths in current path list
            for path in new_allocated_path_list[donor_vn]:
                donor_path_list.append(path.copy())

            # increment to not retry known immobile paths
            donor_path_idx = 0

            cur_weight = self.calc_path_set_weight(
                            new_allocated_path_list[donor_vn],
                            metric)

            # while this path set is heavy
            while(cur_weight > avg_weight \
                    and donor_path_idx < len(donor_path_list) ):

                if True:#self.verbose:
                    if donor_path_idx % 100 == 0:
                        print(f'{donor_path_idx}th iteration and ' +\
                                f'donor ({donor_vn}) ' + \
                                f'weight={cur_weight}' + \
                                f' (all = {[self.calc_path_set_weight(pset, metric) for pset in new_allocated_path_list]})')

                donor_path = donor_path_list[donor_path_idx]

                # target of this path. default to self
                target_vn = donor_vn

                # search others
                # look at end of list
                #   since it is most empty and thus least likely to have collision
                #   this works as this alg is exhaustive so might as well take free lunch when we can
                for other_vn in reversed(range(n_vns)):
                    # not self
                    if donor_vn == other_vn:
                        continue

                    # skip if potential target is heavy (do not overburden)
                    if self.calc_path_set_weight(new_allocated_path_list[other_vn], metric) > avg_weight:
                        # print(f'now recipient {other_vc} is heavy ({calc_link_weight(this_path_list[other_vc])})')
                        continue


                    # completely new local obj
                    new_path_set = []
                    for p in new_allocated_path_list[other_vn]:
                        new_path_set.append(p)

                    new_path_set.append(donor_path)

                    # if we add that donor path, is this new set DL free?

                    # new local obj
                    new_cdg = self.create_a_cdg_from_paths(new_path_set)
                    bes = self.get_back_edge(new_cdg)
                    if len(bes) == 0:
                        # print(f'moving path {donor_path} from {donor_vc}->{other_vc}')

                        target_vn = other_vn

                        # found. might as well exit early?
                        break

                        # else, loop to next possible vn

                # recalc weight
                cur_weight = self.calc_path_set_weight(
                            new_allocated_path_list[donor_vn],
                            metric)

                # found alternative
                if target_vn != donor_vn:
                    # donor_path_list.remove(donor_path)
                    new_allocated_path_list[donor_vn].remove(donor_path)
                    new_allocated_path_list[target_vn].append(donor_path)
                    # print(f'after removal/addition,')
                    # print(f'this_path_list[donor_vc]={this_path_list[donor_vc]}')
                    # print(f'this_path_list[target_vc]={this_path_list[target_vc]}')
                else:
                    pass
                    # print(f'cannot move {donor_path} from {donor_vn}')
                    # input('wait')
                donor_path_idx += 1

            # done with a vn
            print(f'load balanced vn {donor_vn}')
            # last check
            my_cdg_list = []
            for pl in new_allocated_path_list:
                my_cdg_list.append(self.create_a_cdg_from_paths(pl))
            self.assert_deadlock_free(my_cdg_list)


        paths_per_vn = [len(s) for s in new_allocated_path_list]

        all_weights = [self.calc_path_set_weight(pset, metric) for pset in new_allocated_path_list]

        avg_weight = 0
        for w in all_weights:
            avg_weight += w
        avg_weight = avg_weight / n_vns

        if True:#self.verbose:
            print('-'*72)
            print(f'After load balancing')
            print(f'\tweights={all_weights} avg={avg_weight}')
            print(f'\tfor {paths_per_vn} paths and per node per vn')

        # input('continue?')

        # set obj vars
        # self.allocated_path_list = new_allocated_path_list.copy(deep=True)
        self.allocated_path_list = []
        for new_path_list in new_allocated_path_list:
            self.allocated_path_list.append(new_path_list.copy())

        self.n_vns = len(self.allocated_path_list)
        self.set_vn_map_from_path_list()


        # last check
        cdg_list = []
        for pl in self.allocated_path_list:
            cdg_list.append(self.create_a_cdg_from_paths(pl))
        self.assert_deadlock_free(cdg_list)

        return

    # old heuristic. might be useful
    # def reduce_path_list(path_list):

    #     return

    #     n_noi_routers = n_routers - 64
    #     if n_noi_routers == 20:
    #         e = [0,4,5,9,10,14,15,19]

    #     elif n_noi_routers == 24:
    #         e = [0,5,6,11,12,17,18,23]
    #     noi_never_dest = [i for i in range(n_noi_routers) if i not in e]

    #     new_path_list = []

    #     for path in path_list:
    #         # skip ones with the noi as true source
    #         true_src = path[0]
    #         if true_src < n_noi_routers:
    #             continue
    #         # skip ones that terminate in center (not edge) of noi
    #         true_dest = path[-1]
    #         if true_dest in noi_never_dest:
    #             continue

    #         # else
    #         new_path_list.append(path)

    #     return new_path_list

    def assert_deadlock_free(self, list_of_cdgs):
        for cdg in list_of_cdgs:
            bes = self.get_back_edge(cdg)
            assert(len(bes) == 0)

    def assert_pathlist_deadlock_free(self, pathlist):
        cdg = self.create_a_cdg_from_paths(pathlist)
        bes = self.get_back_edge(cdg)
        assert(len(bes) == 0)

    ###################################################################
    # prints

    def print_cdg_list(self, l):
        for i, c in enumerate(l):
            print(f'cdg #{i}')
            for j in range(0,len(c),5):
                try:
                    print(f'[{j}:{j+5}) = {c[j:j+5]}')
                except:
                    print(f'[{j}:) = {c[j:]}')

    def print_path(self, p):

        print(f'path {p[0]} to {p[-1]} (len {len(p)-1}): ',end='')

        l = len(p)
        for i in range(l-1):
            e = p[i]
            print(f'{e}->',end='')
        print(f'{p[-1]}')

    def print_paths_2dmat(self, pmat):

        for src_paths in pmat:
            for p in src_paths:
                if len(p) == 0:
                    continue
                self.print_path(p)

    def print_path_list(self, pl):
        for p in pl:
            self.print_path(p)

#######################################################################
# for running as main


def networkx_get_cycle(cdg):

    cycle = []

    G = nx.DiGraph()

    for src, depens in enumerate(cdg):
        for dest in depens:
            G.add_edge(src, dest)

    try:
        cycle = list(nx.find_cycle(G))

        if verbose:
            print(f'networkx found cycle: {cycle}')
        return cycle

    except:
        return []

def translate_cycle(cycle,node_to_channel_map):
    for a,b in cycle:
        print(f'{node_to_channel_map[a].split(":")[0]}->',end='')
    print('')

# IMPORTANT: path_list is flat.
#           determine src/dest by indexing w/ [0]/[-1]
def create_a_cdg_from_paths( path_list, n_links):

    channel_to_node_map = {}
    node_to_channel_map = {}

    channel_number = 0
    cnum1 = 0
    cnum2 = 0

    cdg_adj_list = [[] for _ in range(n_links)]

    for path in path_list:

        # 1/2 node paths cannot have turns
        # theres only one edge

        for i in range(len(path) - 2):
            # print(f'====================\npath={path}')
            src = path[i]
            mid = path[i+1]
            dest = path[i+2]

            channel_name1 = str(src)+":"+str(mid)
            if channel_name1 in channel_to_node_map:
                cnum1 = channel_to_node_map[channel_name1]
            else:
                cnum1 = channel_number
                channel_to_node_map[channel_name1] = cnum1
                node_to_channel_map[cnum1] = channel_name1
                channel_number += 1
            # print (channel_name1 + "--->" + str(cnum1))
                # edge_name_dict[src].update({mid:cnum1})

            channel_name2 = str(mid)+":"+str(dest)
            if channel_name2 in channel_to_node_map:
                cnum2 = channel_to_node_map[channel_name2]
            else:
                cnum2 = channel_number
                channel_to_node_map[channel_name2] = cnum2
                node_to_channel_map[cnum2] = channel_name2
                channel_number += 1
            # print (channel_name2 + "--->" + str(cnum2))
                # edge_name_dict[mid].update({dest:cnum2})

            if cnum2 in cdg_adj_list[cnum1]:
                pass                                 # turn already exists in CDG; ignore
            else:
                cdg_adj_list[cnum1].append(cnum2)    # add turn to CDG

    if verbose:
        print(f'completed creation of cdg from path set')
        print_cdg_list([cdg_adj_list])

    # quit()

    return cdg_adj_list.copy(), node_to_channel_map, channel_to_node_map

def ingest_vn_local(vn_path):
    vn_map = []

    with open(vn_path,'r') as inf:
        for line in inf:
            line.strip('\n')
            line_split = line.split(' ')
            line_split = [l for l in line_split if '\n' not in l]

            vn_map.append([])
            for e in line_split:
                vn_map[-1].append(int(e))
    return vn_map

def ingest_nrl_local( nrl_name, n_routers):
    if True:#self.verbose:
        print(f'Ingesting nrl {nrl_name}')
    
    nrl = []
    with open(nrl_name,'r') as inf:

        cur = 0
        i = 0
        nrl.append([])

        for line in inf:
            
            if '_' in line:
                continue

            line = line.strip('\n')
            line = line.replace('[','')
            line = line.replace(']','')
            # print(f'line = {line}')
            line_split = line.split(' ')
            line_split = [l for l in line_split if '\n' not in l]

            # print(f'nrl={nrl}')

            nrl[cur].append([])
            
            for e in line_split:
                e = e.strip(',')
                nrl[cur][-1].append(int(e))

            # print(f'i={i}')

            i += 1
            if i == n_routers:
                i = 0
                cur += 1
                nrl.append([])

    return nrl

def flatten_pathlist(twod_pl):
    oned_pl = []
    for src, row in enumerate(twod_pl):
        for dest, path in enumerate(row):
            oned_pl.append(path)
    return oned_pl

def prune_pathlist(oned_pl, vn_map, vn_interest):
    new_pl = []
    for p in oned_pl:
        s = p[0]
        d = p[-1]

        if vn_map[s][d] == vn_interest:
            new_pl.append(p)
    return new_pl

# only local vars
def verify_nrl_vn_files( nrl_path, vn_path):

    vm = ingest_vn_local(vn_path)
    n_routers = len(vm)
    nrl = ingest_nrl_local(nrl_path, n_routers)

    twod_paths = [[[] for __ in range(n_routers)] for _ in range(n_routers)]

    for osrc in range(n_routers):
        for odest in range(n_routers):
            # print(f'constructing path for {osrc}->...->{odest}')

            iter = 0

            cur = osrc

            twod_paths[osrc][odest].append(cur)

            while cur != odest:
                nex = nrl[cur][osrc][odest]
                twod_paths[osrc][odest].append(nex)

                # print(f'cur={cur}, nex={nex}')

                cur = nex

                

                iter += 1

                # if iter >= 8:
                #     quit()

    flat_pl = flatten_pathlist(twod_paths)

    n_vns = 1
    for row in vm:
        # print(f'vm row={row}')
        n_vns = max(n_vns, max(row))

    n_links = n_routers*10
    
    for vn in range(n_vns + 1):

        vnet_pl = prune_pathlist(flat_pl, vm, vn)
        my_cdg, ntc_map, ctn_map = create_a_cdg_from_paths(vnet_pl, n_links)

        cycle = networkx_get_cycle(my_cdg)

        print(f'printing cycle for vn {vn}')
        translate_cycle(cycle, ntc_map)

        if len(cycle) > 0:
            print(f'ERROR: possible deadlock')
            quit()

    print(f'SUCCESS: no deadlock')


def alloc_vns_map_file(fpath,
    route_file_path,
    nrl_file_path,
    out_vn_name=None,
    load_balancing_type='hops',
    alg_type='mclb',
    min_n_vns=None,
    max_n_vns=None,
    max_retries=None,
    vn_file_path_prefix='./topologies_and_routing/vn_maps/'):

    successful = False
    iters = 0

    topo_name = fpath.split('/')[-1].replace('.paths','')
    topo_name = topo_name.replace('.map','')

    while(not successful):

        v = VNAllocator()
        v.verbose = verbose

        if min_n_vns is not None:
            v.vc_min = min_n_vns

        v.setup(fpath, route_file_path, nrl_file_path)

        print(f'completed setup')
        # quit()

        # v.set_path_lists_from_flat(name_to_look_for)


        v.assign_static_vcs()

        # if stringent on # vns
        successful = True
        n_vns = v.n_vns


        if max_n_vns is not None:
            if n_vns > max_n_vns:
                successful = False
                print(f'Failure to reach under {max_n_vns} VNs. Got {n_vns}')
        if max_retries is not None:
            if iters > max_retries:
                successful = True
                print(f'Reached max iterations {iters}')
        else:
            successful = True

        iters += 1


    # dont waste time
    v.load_balance(load_balancing_type)

    if out_vn_name is None:
        outname = f'{topo_name}_{alg_type}_{load_balancing_type}_{n_vns}vns.vn'
        outpath = os.path.join(vn_file_path_prefix, outname)
    else:
        outpath = out_vn_name

    v.output_vn_to_file(outpath)

    vn_file_path = outpath

    print(f'topo {topo_name}\n\titer {iters} successful? {successful}')

    del(v)

    # local var check
    verify_nrl_vn_files(nrl_file_path, vn_file_path)





def alloc_vns_map_file_driver(fpath,
    route_file_path_prefix='./topologies_and_routing/routepath_lists',
    nrl_file_path_prefix='./topologies_and_routing/nr_lists',
    vn_file_path_prefix='./topologies_and_routing/vn_maps',
    min_n_vns=None,
    max_n_vns=None,
    max_retries=None,
    alg_type=None,
    lb_type=None):

    global verbose

    vn_file_path = None
    nrl_file_path = None

    load_balancing_types = ['paths','hops','none']
    alg_types = ['naive','naive_picky','bsorm','bsorm_picky','cload','cload_picky',
                'bsorm_zindexed','cload_zindexed','mclb','augmclb','noci_mclb', 'newnoi_mclb',
                'lpbt']

    if alg_type is not None:
        alg_types = [a for a in alg_types if a==alg_type]
    if len(alg_types) == 0:
        print(f'alg type unfound')
        quit()
    if lb_type is not None:
        load_balancing_types = [l for l in load_balancing_types if l==lb_type]

    for l_b_t in load_balancing_types:
        for a_t in alg_types:


            map_file_path_prefix, map_file_name = \
            os.path.split(fpath)

            # remove ".map"
            topo_name = map_file_name.replace('.map','')



            fullname = f'{topo_name}_{a_t}_{l_b_t}'

            print(f'Working on {fullname}...\n\ti.e. {topo_name} generated by {a_t} balanced by {l_b_t}')


            # name + alg_type + '.paths'

            if alg_type != 'noci_mclb':
                route_file_name = f'{topo_name}_{a_t}.paths'
            else:
                route_file_name = f'mclb_noci_{topo_name}_{a_t}.paths'

            route_file_path = os.path.join(route_file_path_prefix,
                    route_file_name)

            if alg_type != 'noci_mclb':
                nrl_file_name = f'{topo_name}_{a_t}.nrl'
            else:
                nrl_file_name = f'mclb_noci_{topo_name}_{a_t}.nrl'

            nrl_file_path = os.path.join(nrl_file_path_prefix,
                    nrl_file_name)



            alloc_vns_map_file(fpath, route_file_path, nrl_file_path, vn_file_path, min_n_vns=min_n_vns,max_n_vns=max_n_vns,max_retries=max_retries)

    # verify_nrl_vn_files(nrl_file_path, vn_file_path)

def alloc_vns_all_in_dir(dir, mask,
                        route_file_path_prefix='./topologies_and_routing/routepath_lists',
                        nrl_file_path_prefix='./topologies_and_routing//nr_lists',
                        vn_file_path_prefix='./topologies_and_routing//vn_maps',
                        min_n_vns=None,
                        max_n_vns=None,
                        max_retries=None,
                        alg_type=None,
                        lb_type=None):

    global verbose

    negmask = 'asym'

    for root, dirs, files  in os.walk(dir):
        for file in files:
            if mask is not None:
                if mask not in file:
                    continue
            if negmask is not None:
                if negmask in file:
                    continue

            file_path = os.path.join(root,file)

            print('\n' + '='*2*72 )
            print(f'Beginning file:\n\t{file} ({file_path})\n')
            alloc_vns_map_file_driver(file_path,
                            route_file_path_prefix=route_file_path_prefix,
                            nrl_file_path_prefix=nrl_file_path_prefix,
                            vn_file_path_prefix=vn_file_path_prefix,
                            alg_type=alg_type,
                            lb_type=lb_type,
                            min_n_vns=min_n_vns,
                            max_n_vns=max_n_vns,
                            max_retries=max_retries)
            print(f'\nCompleted file:\n\t{file} ({file_path})')
            print('='*2*72 +'\n')

def main():

    _lbt = ['paths','hops','none']


    parser = argparse.ArgumentParser(description='Verify topology values')
    parser.add_argument('--filename',type=str,help='.map file to evaluate')

    parser.add_argument('--all_in_dir', type=str, help='directory to list for all files')
    parser.add_argument('--all_mask', type=str, help='only do for files with this str in filename')
    parser.add_argument('--verbose',action='store_true',help='debug prints')

    parser.add_argument('--min_n_vns',type=int,help='Minimum # of virtual networks')
    parser.add_argument('--max_n_vns',type=int)
    parser.add_argument('--max_retries',type=int,default=15)

    parser.add_argument('--alg_type',type=str)
    parser.add_argument('--lb_type',type=str,choices=_lbt)
    parser.add_argument('--weighted_mclb',action='store_true',help='routing type')

    parser.add_argument('--nr_list',type=str)
    parser.add_argument('--vn_map',type=str)
    parser.add_argument('--path_list',type=str)
    parser.add_argument('--out_vn_name',type=str)

    # for quick testing
    parser.add_argument('--qt',action='store_true')

    args = parser.parse_args()

    if args.qt:
        args.filename = './files/paper_solutions/20r/kite_large.map'
        args.verbose = True

    global verbose
    verbose = args.verbose

    print(f'args={args}')

    fname = None
    if args.filename is not None:
        fname = args.filename
    elif args.all_in_dir is None:
        print('No file list provided. Exiting...')

    if args.nr_list is not None and args.vn_map is not None:
        verify_nrl_vn_files(args.nr_list, args.vn_map )
        print(f'Deadlock free')
        quit()

    load_type = 'hops'
    if args.lb_type:
        load_type=args.lb_type
    alg_type = 'mclb'
    if args.alg_type:
        alg_type=args.alg_type



    if args.nr_list is not None and args.path_list is not None:
        alloc_vns_map_file(fname,
                            args.path_list,
                            args.nr_list,
                            out_vn_name=args.out_vn_name,
                            min_n_vns=args.min_n_vns,
                            max_n_vns=args.max_n_vns,
                            max_retries=args.max_retries)

    elif args.all_in_dir is not None:
        alloc_vns_all_in_dir(args.all_in_dir,
                            args.all_mask,
                            # route_file_path_prefix=rfp,
                            # nrl_file_path_prefix=nrlp,
                            # vn_file_path_prefix=vnfp,
                            alg_type=args.alg_type,
                            lb_type=args.lb_type,
                            min_n_vns=args.min_n_vns,
                            max_n_vns=args.max_n_vns,
                            max_retries=args.max_retries)
    else:
        alloc_vns_map_file_driver(fname,
                            # route_file_path_prefix=rfp,
                            # nrl_file_path_prefix=nrlp,
                            # vn_file_path_prefix=vnfp,
                            alg_type=args.alg_type,
                            lb_type=args.lb_type,
                            min_n_vns=args.min_n_vns,
                            max_n_vns=args.max_n_vns,
                            max_retries=args.max_retries)

if __name__ == '__main__':
    main()
