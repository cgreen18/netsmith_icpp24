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
    Class version of floyd warshall algorithm to find all-pairs minimum distances
        for a given topology/file. Includes modified BFS to find all
        paths of minimum &/ desired hop distances

'''

from collections import deque


class Floyd:

    # class variables
    verbose = False

    # for floyd
    INF = 999

    hop_dist_key = 'hop_dist'
    sp_list_key = 'sp_list'

    def __init__(self):

        # topology variables
        # ------------------
        self.r_map = None

        # for bsorm
        # ---------
        self.residual_capacities = None
        self.demands_map = None

        self.n_routers = -1
        self.n_ulinks = -1
        self.n_cols = -1

        self.is_mesh = False

        # path variables
        # --------------
        self.hop_dist = None

        # eg { 0 : {1 : {'hop_len':1, 'sp_list':[[0,1]]}, // end dest = 1
        #        : 2 : {'hop_len':2, 'sp_list':[[0,1,2],[0,6,2]]}, // end dest = 2
        #          ... } //end src = 0
        #   1 : ...} // end all
        self.all_paths = {}

        # 4D (n_routers X n_routers X *varies X *path_len)
        self.all_min_hop_paths = []

        self.all_nonmin_hop_paths = []

        self.all_min_hop_picky_paths = []

        self.all_min_hop_injej_paths = []

        self.all_min_hop_laxinjej_paths = []

        self.all_min_hop_odnoi_paths = []

        self.all_nonmin_hop_ndbt_paths = []

        self.all_nonmin_hop_ndbt_picky_paths = []

        self.all_nonmin_hop_ndbt_injej_paths = []


        # 3D (n_routers X n_routers X *path_len)
        self.shortest_paths = []

        # 2D (n_routers^2 X *varies)
        self.flat_shortest_paths = []

    # class instance functions
    # ------------------------

    def init_uniform_residual_capacities(self, init_cap):

        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        if self.residual_capacities is None:
            self.residual_capacities = self.r_map.copy()

        n_routers = self.n_routers

        for src in range(n_routers):
            for dest in range(n_routers):
                if self.r_map[src][dest] == 1:
                    self.residual_capacities[src][dest] = init_cap


    def init_demands(self):
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        n_routers = self.n_routers

        self.demands_map = [[0.0 for _ in range(n_routers)] for __ in range(n_routers)]

    # class attribute functions
    # -------------------------

    # used lol
    def set_verbose(self, v):
        self.verbose = v

    # hop dist stuff
    # --------------

    def floyd(self):
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        if self.verbose:
            print(f'begin floyd. n_rotuers={self.n_routers}')

        # for brevity
        n_routers = self.n_routers

        graph = [[item if item==1 else self.INF for item in row] for row in self.r_map]

        for i in range(0,n_routers):
            graph[i][i]=0

        dist = list(map(lambda p: list(map(lambda q: q, p)), graph))

        for r in range(n_routers):
            for p in range(n_routers):
                for q in range(n_routers):
                    # shorter path through r
                    if (dist[p][r]+ dist[r][q]) < dist[p][q]:
                        dist[p][q] = dist[p][r] + dist[r][q]
                
            #         print(f'q={q}')
                
            #     print(f'p={p}')

            # print(f'r={r}')

        self.hop_dist = dist.copy()


    # path stuff
    # ----------

    # TODO move all paths for a given length to a separate function
    # modified from
    #   https://www.geeksforgeeks.org/print-paths-given-source-destination-using-bfs/
    def calculate_min_hop_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # for brevity
        n_routers = self.n_routers

        short_paths = []

        for src in range(n_routers):

            short_paths.append([])

            # print(f'Min hop paths for src {src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                this_path_list = []

                if src == dest:
                    # path is nonexistent
                    this_path_list.append(src)
                    short_paths[src][dest].append(this_path_list)
                    continue


                # perform psuedo-BFS

                shortest_dist = self.hop_dist[src][dest]

                # print(f'Searching for path {src}->{dest} of dist {shortest_dist}')


                queue = deque()

                path = []
                path.append(src)
                queue.append(path.copy())

                while queue:
                    path = queue.popleft()
                    last = path[-1]

                    # only consider the minimal paths
                    if len(path) - 1 > shortest_dist:
                        # print(f'path {path} (len {len(path)}) > shortest {shortest_dist}')
                        continue

                    if last == dest:
                        this_path_list.append(path)
                        if self.verbose:
                            self.print_path(path)

                    for i in range(n_routers):

                        # only consider neighbors
                        if self.r_map[last][i] == 0:
                            continue

                        # if self.is_not_visited(i, path):
                        if not i in path:
                            new_path = path.copy()
                            new_path.append(i)
                            queue.append(new_path)


                short_paths[src][dest] = this_path_list.copy()

                # print(f'Found {src}->{dest}={this_path_list}')

                # end dest loop


        self.all_min_hop_paths = short_paths.copy()

        print(f'done with min hop paths')


    # TODO move all paths for a given length to a separate function
    # modified from
    #   https://www.geeksforgeeks.org/print-paths-given-source-destination-using-bfs/
    def calculate_nonmin_hop_paths(self, nonmin_allowance):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # for brevity
        n_routers = self.n_routers

        short_paths = []

        for src in range(n_routers):

            short_paths.append([])

            print(f'\nNon min hop paths for src {src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                this_path_list = []

                if src == dest:
                    # path is nonexistent
                    # this_path_list.append(src)
                    # short_paths[src][dest].append(this_path_list)
                    continue


                # perform psuedo-BFS

                shortest_dist = self.hop_dist[src][dest]

                # print(f'\tMin hop paths for dest {dest}. shortest_dist={shortest_dist}. nonmin_allowance={nonmin_allowance}')


                # print(f'Searching for path {src}->{dest} of dist {shortest_dist}')


                queue = deque()

                path = []
                path.append(src)
                queue.append(path.copy())

                while queue:
                    path = queue.popleft()
                    last = path[-1]

                    # print(f'\t\tpath {path} (len {len(path)})')

                    # only consider the minimal paths
                    if len(path) - 1 > shortest_dist + nonmin_allowance :
                        # print(f'\t\t\tpath - 1 => shortest + nonmin_allowance ')
                        continue

                    # else:
                    #     print(f'\t\t\tpath {path} (len {len(path)}) is nonminimal')

                    if last == dest and len(path)  - 1 > shortest_dist:
                        # print(f'\t\t\tpath  - 1 > shortest_dist')
                        # print(f'\t\t\tpath {path} (len {len(path)}) is not visited')

                        this_path_list.append(path)
                        if self.verbose:
                            self.print_path(path)

                    for i in range(n_routers):

                        # only consider neighbors
                        if self.r_map[last][i] == 0:
                            continue

                        # if self.is_not_visited(i, path):
                        if not i in path:
                            new_path = path.copy()
                            new_path.append(i)
                            queue.append(new_path)


                short_paths[src][dest] = this_path_list.copy()

                # print(f'Found {src}->{dest}={this_path_list}')
                # print('')

                # end dest loop


        self.all_nonmin_hop_paths = short_paths.copy()

        print(f'done with min hop paths')

        return short_paths.copy()

# TODO move all paths for a given length to a separate function
    # modified from
    #   https://www.geeksforgeeks.org/print-paths-given-source-destination-using-bfs/
    def calculate_min_hop_picky_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # for brevity
        n_routers = self.n_routers

        short_paths = []
        print(f'Selecting min hop picky paths')

        for src in range(n_routers):

            short_paths.append([])

            # print(f'{src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                this_path_list = []

                if src == dest:
                    # path is nonexistent
                    this_path_list.append(src)
                    short_paths[src][dest].append(this_path_list)
                    continue


                # perform psuedo-BFS

                # relax this constraint
                # shortest_dist = self.hop_dist[src][dest]

                # set it as first dist found
                shortest_dist = n_routers

                # print(f'Searching for path {src}->{dest} of dist {shortest_dist}')



                queue = deque()

                path = []
                path.append(src)
                queue.append(path.copy())

                while queue:
                    path = queue.popleft()
                    last = path[-1]

                    # only consider the minimal paths
                    if len(path) - 1 > shortest_dist:
                        # print(f'path {path} (len {len(path)}) > shortest {shortest_dist}')
                        continue



                    if last == dest:
                        if self.is_valid_picky_path(path):
                            this_path_list.append(path)

                            # sets the bar
                            # since BFs this should also be minimum
                            if len(path) < shortest_dist:
                                shortest_dist = len(path) -1

                            # print(f'valid path {path} and valid picky path. new shortest dist = {shortest_dist}')


                        # else:
                        #     print(f'valid path {path} but invalid picky path')

                        if self.verbose:
                            self.print_path(path)

                    for i in range(n_routers):

                        # only consider neighbors
                        if self.r_map[last][i] == 0:
                            continue

                        # if self.is_not_visited(i, path):
                        if not i in path:
                            new_path = path.copy()
                            new_path.append(i)
                            queue.append(new_path)

                short_paths[src][dest] = this_path_list.copy()

                # print(f'Found {src}->{dest}={this_path_list}')

                # end dest loop


        self.all_min_hop_picky_paths = short_paths.copy()

    def calculate_min_hop_injej_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # for brevity
        n_routers = self.n_routers

        short_paths = []

        for src in range(n_routers):

            short_paths.append([])

            # print()
            print(f'injej paths src {src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                # if src < 20:
                #     continue

                # print(f'-'*72)
                #print(f'\t->...{dest}')

                this_path_list = []

                if src == dest:
                    # path is nonexistent
                    this_path_list.append(src)
                    short_paths[src][dest].append(this_path_list)
                    continue


                # perform psuedo-BFS

                # relax this constraint
                # shortest_dist = self.hop_dist[src][dest]

                # set it as first dist found
                shortest_dist = n_routers

                # print(f'\t\tSearching for path {src}->{dest} of dist {shortest_dist}')



                queue = deque()

                path = []
                path.append(src)
                queue.append(path.copy())


                while queue:

                    #if dest == 47:
                    #    input(f'cont? path={path}')

                    path = queue.popleft()
                    last = path[-1]

                    # only consider the minimal paths
                    if len(path) - 1 > shortest_dist:
                        # print(f'\t\tpath {path} (len {len(path)}) > shortest {shortest_dist}')
                        continue



                    if last == dest:
                        # print(f'\t\tpossible path {path}')
                        if self.is_valid_injej_path(path):
                            this_path_list.append(path)

                            # sets the bar
                            # since BFs this should also be minimum
                            if len(path) < shortest_dist:
                                shortest_dist = len(path) -1

                            # print(f'valid injej path {path}. new shortest dist = {shortest_dist}')


                        # else:
                        #     print(f'valid path {path} but invalid picky path')

                        if self.verbose:
                            self.print_path(path)

                    for i in range(n_routers):

                        # only consider neighbors
                        if self.r_map[last][i] == 0:
                            continue

                        # if self.is_not_visited(i, path):
                        if not i in path:
                            new_path = path.copy()
                            new_path.append(i)
                            queue.append(new_path)

                short_paths[src][dest] = this_path_list.copy()

                # if src >= 21:
                #     print(f'Found {src}->{dest}={this_path_list}')
                #     input('cont?')
                # end dest loop


        self.all_min_hop_injej_paths = short_paths.copy()

        print(f'done with injej paths')

    def calculate_min_hop_laxinjej_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # for brevity
        n_routers = self.n_routers

        short_paths = []

        for src in range(n_routers):

            short_paths.append([])

            # print()
            # print(f'injej paths src {src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                # if src < 20:
                #     continue

                # print(f'-'*72)
                # print(f'injej {src}->...{dest}')

                this_path_list = []

                if src == dest:
                    # path is nonexistent
                    this_path_list.append(src)
                    short_paths[src][dest].append(this_path_list)
                    continue


                # perform psuedo-BFS

                # relax this constraint
                # shortest_dist = self.hop_dist[src][dest]

                # set it as first dist found
                shortest_dist = n_routers

                # print(f'Searching for path {src}->{dest} of dist {shortest_dist}')



                queue = deque()

                path = []
                path.append(src)
                queue.append(path.copy())

                while queue:
                    path = queue.popleft()
                    last = path[-1]

                    # only consider the minimal paths
                    if len(path) - 1 > shortest_dist:
                        # print(f'path {path} (len {len(path)}) > shortest {shortest_dist}')
                        continue



                    if last == dest:
                        if self.is_valid_laxinjej_path(path):
                            this_path_list.append(path)

                            # sets the bar
                            # since BFs this should also be minimum
                            if len(path) < shortest_dist:
                                shortest_dist = len(path) -1

                            # print(f'valid injej path {path}. new shortest dist = {shortest_dist}')


                        # else:
                        #     print(f'valid path {path} but invalid picky path')

                        if self.verbose:
                            self.print_path(path)

                    for i in range(n_routers):

                        # only consider neighbors
                        if self.r_map[last][i] == 0:
                            continue

                        # if self.is_not_visited(i, path):
                        if not i in path:
                            new_path = path.copy()
                            new_path.append(i)
                            queue.append(new_path)

                short_paths[src][dest] = this_path_list.copy()

                # if src >= 21:
                #     print(f'Found {src}->{dest}={this_path_list}')
                #     input('cont?')
                # end dest loop


        self.all_min_hop_laxinjej_paths = short_paths.copy()

        print(f'done with lax injej paths')

    def calculate_min_hop_odnoi_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # for brevity
        n_routers = self.n_routers

        short_paths = []

        for src in range(n_routers):

            short_paths.append([])

            # print()
            # print(f'injej paths src {src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                # if src < 20:
                #     continue

                # print(f'-'*72)
                # print(f'injej {src}->...{dest}')

                this_path_list = []

                if src == dest:
                    # path is nonexistent
                    this_path_list.append(src)
                    short_paths[src][dest].append(this_path_list)
                    continue


                # perform psuedo-BFS

                # relax this constraint
                # shortest_dist = self.hop_dist[src][dest]

                # set it as first dist found
                shortest_dist = n_routers

                # print(f'Searching for path {src}->{dest} of dist {shortest_dist}')



                queue = deque()

                path = []
                path.append(src)
                queue.append(path.copy())

                while queue:
                    path = queue.popleft()
                    last = path[-1]
                    first = path[0]

                    # only consider the minimal paths
                    if len(path) - 1 > shortest_dist:
                        # print(f'path {path} (len {len(path)}) > shortest {shortest_dist}')
                        continue



                    if last == dest:
                        if self.is_valid_odnoi_path(path):
                            this_path_list.append(path)

                            # sets the bar
                            # since BFs this should also be minimum
                            if len(path) < shortest_dist:
                                shortest_dist = len(path) -1

                            # if first >= 20 and last >= 20:

                            #     print(f'valid odnoi path {path}. new shortest dist = {shortest_dist}')
                            #     input('cont?')


                        # else:
                        #     print(f'valid path {path} but invalid picky path')

                        if self.verbose:
                            self.print_path(path)

                    for i in range(n_routers):

                        # only consider neighbors
                        if self.r_map[last][i] == 0:
                            continue

                        # if self.is_not_visited(i, path):
                        if not i in path:
                            new_path = path.copy()
                            new_path.append(i)
                            queue.append(new_path)

                short_paths[src][dest] = this_path_list.copy()

                # if src >= 21:
                #     print(f'Found {src}->{dest}={this_path_list}')
                #     input('cont?')
                # end dest loop


        self.all_min_hop_odnoi_paths = short_paths.copy()

        print(f'done with odnoi paths')

    def calculate_nonmin_hop_ndbt_picky_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # return

        # for brevity
        n_routers = self.n_routers


        short_paths = []

        for src in range(n_routers):

            short_paths.append([])

            # print(f'\nMin hop paths for src {src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                if src == dest:
                    # path is nonexistent
                    # this_path_list.append(src)
                    # short_paths[src][dest].append(this_path_list)
                    continue

                # perform psuedo-BFS

                shortest_dist = self.hop_dist[src][dest]

                nonmin_allowance = 0
                at_least_one_path = False
                while not at_least_one_path:

                    this_path_list = []


                    # print('-'*80)
                    # print(f'\tMin hop paths for src {src}, dest {dest}. shortest_dist={shortest_dist}. nonmin_allowance={nonmin_allowance}')
                    # input(f'Searching for path {src}->{dest} of dist {shortest_dist}')

                    # if src==21:
                    #     self.verbose = True

                    queue = deque()

                    path = []
                    path.append(src)
                    queue.append(path.copy())

                    while queue:
                        path = queue.popleft()
                        last = path[-1]

                        # print(f'\t\tpath {path} (len {len(path)})')

                        # only consider the minimal paths
                        if len(path) - 1 > shortest_dist + nonmin_allowance :
                            # print(f'\t\t\tpath - 1 => shortest + nonmin_allowance ')
                            continue
                        
                        # else:
                        #     print(f'\t\t\tpath {path} (len {len(path)}) is nonminimal')



                        if last == dest:
                            # print(f'\t\t\tfound destination {dest}')
                            if self.verbose:
                                print(f'\t\t\tpath {path} (len {len(path)}) reaches destination')

                            # theres probably a cool list comprehension
                            noi_portion = []
                            for p in path:
                                if not self.r_is_noc(p):
                                    noi_portion.append(p)

                            # only consider no double backs
                            if self.path_has_double_back(noi_portion):
                                if self.verbose:
                                    print(f'path {path} (w/ noi_portion {noi_portion}) has double back turn')
                                continue

                            if not self.is_valid_picky_path(path):
                                if self.verbose:
                                    print(f'path {path} is not picky')
                                continue

                            # found path
                            this_path_list.append(path)
                            at_least_one_path = True
                            if self.verbose:
                                self.print_path(path)

                        for i in range(n_routers):

                            # only consider neighbors
                            if self.r_map[last][i] == 0:
                                continue

                            # if self.is_not_visited(i, path):
                            if not i in path:
                                new_path = path.copy()
                                new_path.append(i)
                                queue.append(new_path)

                    nonmin_allowance += 1

                    # if src == 3 and dest == 14:
                    # input(f'continuing nonmin_allowance to {nonmin_allowance}')



                nonmin_allowance -= 1


                short_paths[src][dest] = this_path_list.copy()

                # print(f'Found {src}->{dest}={this_path_list}')

                if nonmin_allowance != 0:
                    # input(f'FLAG : nonmin {src}->{dest} by {nonmin_allowance} for list {short_paths[src][dest]}')
                    # print(f'FLAG : nonmin {src}->{dest} by {nonmin_allowance}')
                    pass
                # else:
                #     input(f'FLAG : min {src}->{dest} for list {short_paths[src][dest]}')



                # print('')

                # input(f'completed pathset {nonmin_allowance}')


                # end dest loop




        self.all_nonmin_hop_ndbt_picky_paths = short_paths.copy()

        print(f'done with nonmin hop no double back picky paths')


    def calculate_nonmin_hop_ndbt_injej_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # return

        # for brevity
        n_routers = self.n_routers


        short_paths = []

        for src in range(n_routers):

            short_paths.append([])

            # print(f'\nMin hop paths for src {src}')

            for dest in range(n_routers):
                short_paths[src].append([])

                if src == dest:
                    # path is nonexistent
                    # this_path_list.append(src)
                    # short_paths[src][dest].append(this_path_list)
                    continue

                # perform psuedo-BFS

                shortest_dist = self.hop_dist[src][dest]

                nonmin_allowance = 0
                at_least_one_path = False
                while not at_least_one_path:

                    this_path_list = []

                    # print('-'*80)
                    # print(f'\tMin hop paths for src {src}, dest {dest}. shortest_dist={shortest_dist}. nonmin_allowance={nonmin_allowance}')
                    # print(f'Searching for path {src}->{dest} of dist {shortest_dist}')

                    # if src==21:
                    #     self.verbose = True

                    queue = deque()

                    path = []
                    path.append(src)
                    queue.append(path.copy())

                    while queue:
                        path = queue.popleft()
                        last = path[-1]

                        # print(f'\t\tpath {path} (len {len(path)})')

                        # only consider the minimal paths
                        if len(path) - 1 > shortest_dist + nonmin_allowance :
                            # print(f'\t\t\tpath - 1 => shortest + nonmin_allowance ')
                            continue
                        
                        # else:
                        #     print(f'\t\t\tpath {path} (len {len(path)}) is nonminimal')



                        if last == dest:
                            # print(f'\t\t\tfound destination {dest}')
                            if self.verbose:
                                print(f'\t\t\tpath {path} (len {len(path)}) reaches destination')

                            # theres probably a cool list comprehension
                            noi_portion = []
                            for p in path:
                                if not self.r_is_noc(p):
                                    noi_portion.append(p)

                            # only consider no double backs
                            if self.path_has_double_back(noi_portion):
                                if self.verbose:
                                    print(f'path {path} (w/ noi_portion {noi_portion}) has double back turn')
                                continue

                            if not self.is_valid_injej_path(path):
                                if self.verbose:
                                    print(f'path {path} is not injej')
                                continue

                            # found path
                            this_path_list.append(path)
                            at_least_one_path = True
                            if self.verbose:
                                self.print_path(path)

                        for i in range(n_routers):

                            # only consider neighbors
                            if self.r_map[last][i] == 0:
                                continue

                            # if self.is_not_visited(i, path):
                            if not i in path:
                                new_path = path.copy()
                                new_path.append(i)
                                queue.append(new_path)

                    nonmin_allowance += 1

                    # if src == 3 and dest == 14:
                    # input(f'continuing nonmin_allowance to {nonmin_allowance}')



                nonmin_allowance -= 1


                short_paths[src][dest] = this_path_list.copy()

                # print(f'Found {src}->{dest}={this_path_list}')

                if nonmin_allowance != 0:
                    # input(f'FLAG : nonmin {src}->{dest} by {nonmin_allowance} for list {short_paths[src][dest]}')
                    # print(f'FLAG : nonmin {src}->{dest} by {nonmin_allowance}')
                    pass
                # else:
                #     input(f'FLAG : min {src}->{dest} for list {short_paths[src][dest]}')



                # print('')

                # input(f'completed pathset {nonmin_allowance}')


                # end dest loop




        self.all_nonmin_hop_ndbt_injej_paths = short_paths.copy()

        print(f'done with nonmin hop no double back injej paths')


    def calculate_nonmin_hop_ndbt_paths(self):

        assert(self.hop_dist is not None)
        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        # for brevity
        n_routers = self.n_routers

        local_verbose =  False

        short_paths = []
        for src in range(n_routers):
            short_paths.append([])

            
            for dest in range(n_routers):
                if local_verbose:
                    print(f'\nMin hop paths for src {src}, dest {dest}')
                short_paths[src].append([])

                # if src == 0 and dest == 7  :
                # if True:
                if False:
                    # local_verbose = True
                    pass

                if src == dest:
                    # path is nonexistent
                    # this_path_list.append(src)
                    # short_paths[src][dest].append(this_path_list)
                    continue

                # perform psuedo-BFS

                shortest_dist = self.hop_dist[src][dest]

                # now find a path
                nonmin_allowance = 0
                at_least_one_path = False
                while not at_least_one_path:

                    this_path_list = []

                    if local_verbose:
                        print('-'*80)
                        print(f'\tMin hop paths for src {src}, dest {dest}. shortest_dist={shortest_dist}. nonmin_allowance={nonmin_allowance}')
                        print(f'Searching for path {src}->{dest} of dist {shortest_dist}')
                        # input('cont?')


                    queue = deque()

                    path = []
                    path.append(src)
                    queue.append(path.copy())

                    while queue:

                        # print(f'expected continue')

                        path = queue.popleft()
                        last = path[-1]

                        if local_verbose:
                            input(f'\t\tpath {path} (len {len(path) - 1})')

                        # only consider the minimal paths
                        if len(path) - 1 > shortest_dist + nonmin_allowance :
                            if local_verbose:
                                print(f'\t\t\tpath - 1 => shortest + nonmin_allowance ')
                            continue
                        
                        else:
                            if local_verbose:
                                print(f'\t\t\tpath {path} (len {len(path)}) is nonminimal')
                            pass


                        if last == dest:
                            if local_verbose:
                                print(f'\t\t\tfound destination {dest}')
                                input(f'\t\t\tpath {path} (len {len(path)}) is not visited')


                            # only consider no double backs
                            if self.path_has_double_back(path, vb=local_verbose):
                                if self.verbose or local_verbose:
                                    print(f'path {path} has double back turn')

                            else:
                                if self.verbose or local_verbose:
                                    print(f'path {path} does NOT have double back turn')
                                # found path
                                # print(f'at_least_one_path={at_least_one_path}')
                                this_path_list.append(path)
                                at_least_one_path = True
                                if local_verbose:
                                    self.print_path(path)
                                    input(f'\tnew path : {path}')

                        for i in range(n_routers):

                            # only consider neighbors
                            if self.r_map[last][i] == 0:
                                continue

                            # if self.is_not_visited(i, path):
                            if not i in path:
                                new_path = path.copy()
                                new_path.append(i)
                                queue.append(new_path)

                    # print(f'exhaused queue')
                    # print(f'at_least_one_path={at_least_one_path}')

                    nonmin_allowance += 1

                    if nonmin_allowance < 1:
                        local_verbose = False
                    else:
                        local_verbose = False# True

                    # if src == 3 and dest == 14:
                    #     input(f'continuing nonmin_allowance to {nonmin_allowance}')



                nonmin_allowance -= 1


                short_paths[src][dest] = this_path_list.copy()

                # print(f'Found {src}->{dest}={this_path_list}')

                if nonmin_allowance != 0:
                    # input(f'FLAG : nonmin {src}->{dest} by {nonmin_allowance} for list {short_paths[src][dest]}')
                    # print(f'FLAG : nonmin {src}->{dest} by {nonmin_allowance}')
                    pass


                # print('')

                # input(f'completed pathset {nonmin_allowance}')


                # end dest loop




        self.all_nonmin_hop_ndbt_paths = short_paths.copy()

        print(f'done with nonmin hop no double back paths')

    # routes that double-back (head E-W and then W-E on other links) are not possible due to disintegration
    def path_has_double_back(self, path, vb=False):

        if vb:
            print(f'checking double back for {path}')

        has_gone_east_west = False
        has_gone_west_east = False

        double_back_EWWE = False
        double_back_WEEW = False

        path_len = len(path)
        for i in range(path_len - 1):
            s = path[i]
            d = path[i+1]

            if self.node_a_to_b_is_east_west(s,d):
                has_gone_east_west = True
                if vb:
                    print(f'\tturn {s}->{d} in path {path} goes E-W')

            if self.node_a_to_b_is_west_east(s,d):
                has_gone_west_east = True
                if vb:
                    print(f'\tturn {s}->{d} in path {path} goes W-E')
 
            this_is_west_east = self.node_a_to_b_is_west_east(s,d)
            this_is_east_west = self.node_a_to_b_is_east_west(s,d)

            # if this_is_west_east:
            #     print(f'\tturn {s}->{d} in path {path} goes W-E')

            # if this_is_east_west:
            #     print(f'\tturn {s}->{d} in path {path} goes E-W')

            if has_gone_east_west and this_is_west_east:
                if vb:
                    print(f'\tdouble back turn {s}->{d} in path {path} found')
                double_back_EWWE = True

            if has_gone_west_east and this_is_east_west:
                if vb:
                    print(f'\tdouble back turn {s}->{d} in path {path} found')
                double_back_WEEW = True

        if double_back_EWWE and double_back_WEEW:
        # if double_back_EWWE or double_back_WEEW:

            if vb:
                input(f'has double both back for {path}')
            return True

        return False

    def node_a_to_b_is_west_east(self, a, b):

        n_cols = self.n_cols
        col_a = a % n_cols
        col_b = b % n_cols

        # west to east => lower col to higher col
        if col_a < col_b:
            return True
        if col_a == col_b:
            # return True
            if a < b:
                return True

        return False

    def node_a_to_b_is_east_west(self, a, b):

        n_cols = self.n_cols
        col_a = a % n_cols
        col_b = b % n_cols

        # east to west => higher col to lower col
        if col_a > col_b:
            return True
        if col_a == col_b:
            # return False
            if a > b:
                return True

        return False

    def get_lowest_weight_path(self, src, dest, demand):

        min_path_set = self.all_min_hop_paths[src][dest]

        if self.verbose:
            print(f'Considering min_path_set[{src}][{dest}]={min_path_set}')

        # dummy max
        # TODO: what's the theoretical max?
        lowest_weight = self.INF
        lowest_weight_path = None

        for path_num, path in enumerate(min_path_set):

            path_len = len(path)
            path_weight = 0
            for i in range(path_len - 1):
                node_a = path[i]
                node_b = path[i+1]
                path_weight += self.weight_of_edge(node_a, node_b, demand)

            if path_weight < lowest_weight:
                if path_num != 0:
                    print(f'\tFLAG choosing not first path {path}')
                lowest_weight = path_weight
                lowest_weight_path = path.copy()

        if self.verbose:
            print(f'Found lowest weight path between {src} -> {dest}')
            print(f'\tpath (len={len(lowest_weight_path)}) (weight={lowest_weight}) = {lowest_weight_path}')

        return lowest_weight_path.copy()

    def weight_of_edge(self, src, dest, demand):
        res_cap = self.residual_capacities[src][dest]

        if res_cap < demand:
            return self.INF

        w = 1.0 / (res_cap - demand)
        return w

    def update_capacities_on_path(self, path, demand):

        path_len = len(path)

        for i in range(path_len - 1):
            src = path[i]
            dest = path[i+1]

            assert(self.residual_capacities[src][dest] >= demand)

            self.residual_capacities[src][dest] -= demand

    def r_is_noc(self, r_num):
        n_noi = 20
        if self.is_mesh:
            n_noi = 64
        if r_num >= n_noi:
            return True
        return False

    def same_chiplet(self, a,b):

        if a < 20 or b < 20:
            return False

        a = a - 20
        b = b - 20

        chiplet_a = (a % 8 >= 4) + 2*(a / 8 >= 4)

        chiplet_b = (b % 8 >= 4) + 2*(b / 8 >= 4)

        # print(f'a={a} on {chiplet_a}, b={b} on {chiplet_b}')

        if chiplet_a == chiplet_b:
            return True
        return False

    def only_traverses_noc(self, p):
        for n in p:
            if not self.r_is_noc(n):
                return False
        return True

    def is_valid_odnoi_path(self, path):

        src_r = path[0]
        dest_r = path[-1]

        # if same chiplet, must traverse only NoC
        # else, must inject/eject immediately/lastly

        if self.same_chiplet(src_r, dest_r):
            return self.only_traverses_noc(path)

        return self.is_valid_injej_path(path)

    def is_valid_injej_path(self, path):

        # valid if 1) directly connected or ( 2) inj/ej immediately AND 3) is valid picky path )

        src_r = path[0]
        dest_r = path[-1]

        is_src_noc = self.r_is_noc(src_r)
        is_dest_noc = self.r_is_noc(dest_r)

        # print(f'valid_injej():: considering path {path}. src_noc={is_src_noc}, dest_noc={is_dest_noc}')

        # 1)
        # if len(path) == 2:
        #     # print(f'\t\tdirect connection')
        #     return True

        # 2)

        # a) noc->noc => must inj and ej
        # b) noc->noi => must inj
        # c) noi->noc => must ej
        # d) noi->noi => none

        if not self.is_valid_picky_path(path):
            # print(f'\t\t not valid picky')
            return False

        #   a) inj and ej
        if is_src_noc and is_dest_noc:
            s2 = path[1]
            d2 = path[-2]
            # inj. must go noc->noi = not noc => is noc ret False
            if self.r_is_noc(s2):
                # print(f'\t\t not inj {src_r}->{s2}')
                return False

            # ej. must go noi->noc = not noc => is noc ret False
            if self.r_is_noc(d2):
                # print(f'\t\t not ej {d2}->{dest_r}')
                return False

        # b) inj
        elif is_src_noc and not is_dest_noc:
            s2 = path[1]
            # inj. must go noc->noi = not noc => is noc ret False
            if self.r_is_noc(s2):
                # print(f'\t\t not inj {src_r}->{s2}')
                return False

        # c) ej
        elif not is_src_noc and is_dest_noc:
            d2 = path[-2]
            # inj. must go noc->noi = not noc => is noc ret False
            if self.r_is_noc(d2):
                # print(f'\t\t not ej {d2}->{dest_r}')
                return False

        # print(f'\t\t path {path} must be valid')

        return True

    def is_valid_laxinjej_path(self, path):

        # valid if 1) directly connected or ( 2) inj/ej immediately AND 3) is valid picky path )

        src_r = path[0]
        dest_r = path[-1]

        is_src_noc = self.r_is_noc(src_r)
        is_dest_noc = self.r_is_noc(dest_r)

        # print(f'valid_injej():: considering path {path}. src_noc={is_src_noc}, dest_noc={is_dest_noc}')

        # 1)
        if len(path) == 2:
            # print(f'\t\tdirect connection')
            return True

        # 2)

        # a) noc->noc => must inj and ej
        # b) noc->noi => must inj
        # c) noi->noc => must ej
        # d) noi->noi => none

        if not self.is_valid_picky_path(path):
            # print(f'\t\t not valid picky')
            return False

        #   a) inj and ej
        if is_src_noc and is_dest_noc:
            s2 = path[1]
            d2 = path[-2]
            # inj. must go noc->noi = not noc => is noc ret False
            if self.r_is_noc(s2):
                # print(f'\t\t not inj {src_r}->{s2}')
                return False

            # ej. must go noi->noc = not noc => is noc ret False
            if self.r_is_noc(d2):
                # print(f'\t\t not ej {d2}->{dest_r}')
                return False

        # b) inj
        elif is_src_noc and not is_dest_noc:
            s2 = path[1]
            # inj. must go noc->noi = not noc => is noc ret False
            if self.r_is_noc(s2):
                # print(f'\t\t not inj {src_r}->{s2}')
                return False

        # c) ej
        elif not is_src_noc and is_dest_noc:
            d2 = path[-2]
            # inj. must go noc->noi = not noc => is noc ret False
            if self.r_is_noc(d2):
                # print(f'\t\t not ej {d2}->{dest_r}')
                return False

        # print(f'\t\t path {path} must be valid')

        return True

    def is_valid_picky_path(self, path):

        crossed_into_noi = False
        crossed_into_noc = False

        into_noi_crossings = 0
        into_noc_crossings = 0

        inject_hop = None
        eject_hop = None

        last_was_noc = None

        flagged_path = False

        # print(f'picky_path():: path={path}')


        src_r = path[0]
        dest_r = path[-1]

        is_src_noc = self.r_is_noc(src_r)
        is_dest_noc = self.r_is_noc(dest_r)

        # given src, dest
        should_never_cross = False
        if (not is_src_noc) and (not is_dest_noc):
            should_never_cross = True

        for i, r in enumerate(path):

            is_this_noc = self.r_is_noc(r)

            if self.verbose:
                print(f'r={r} is_noc? {is_this_noc}. is_last_noc? {last_was_noc}')

            if last_was_noc is None:
                last_was_noc = is_this_noc
                continue

            if last_was_noc and not is_this_noc:
                crossed_into_noi = True
                inject_hop = i
                into_noi_crossings += 1

            if not last_was_noc and is_this_noc:
                crossed_into_noc = True
                eject_hop = i
                into_noc_crossings += 1



            last_was_noc = is_this_noc

        if self.verbose:
            print(f'path {src_r}->{dest_r} : injects at {inject_hop}and ejects at {eject_hop}')
            print(f'\t\t: noc crossings = {into_noc_crossings} and into noi crossings = {into_noi_crossings}')


        if into_noc_crossings > 1:
            return False
        if into_noi_crossings > 1:
            return False

        # allowed to surf noc
        if not crossed_into_noi:
            return True

        if should_never_cross and (crossed_into_noi or crossed_into_noc):
            if self.verbose:
                print(f'not picky should never cross')
            return False

        if crossed_into_noi and inject_hop != 1:
            if self.verbose:
                print(f'injected at wrong time')
            return False
        if crossed_into_noc and eject_hop != len(path) - 1:
            if self.verbose:
                print(f'ejected at wrong time')
            return False



        return True


    # general stuff
    # -------------

    def max_of_mat(self, mat):
        max_val = max([max(row) for row in mat])
        return max_val

    def calc_n_ulinks(self):
        sum = 0

        for p in range(self.n_routers):
            for q in range(self.n_routers):
                if p==q:
                    continue
                sum += self.r_map[p][q]

        return sum

    # input/output stuff
    # ------------------

    def ingest_map(self, path_name):
        self.r_map = self.ingest_a_map(path_name)
        self.n_routers = len(self.r_map)
        self.n_ulinks = self.calc_n_ulinks()


        self.n_cols = 5
        if self.n_routers == 48:
            self.n_cols = 8
        if self.n_routers == 30:
            self.n_cols = 5
        if self.n_routers == 64:
            self.n_cols = 8

        # input(f'Number of cols very important. Must be set. Currently, n_cols = {self.n_cols}')


    def ingest_a_map(self, path_name):
        file_name = path_name.split('/')[-1]

        if self.verbose:
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
                # instead, make binary
                if conn >= 0.5:
                    conn = 1
                # assert(conn == 1 or conn == 0)

        # if self.verbose:
        #     print(f'read {this_map}')

        return this_map

    # prints
    # ------

    def print_path(self, p):

        print(f'path {p[0]} to {p[-1]} (len {len(p)-1}): ',end='')

        l = len(p)
        for i in range(l-1):
            e = p[i]
            print(f'{e}->',end='')
        print(f'{p[-1]}')

    def print_all_shortest_paths(self):
        for spl in self.all_shortest_paths:
            for dpl in spl:
                for pl in dpl:
                    for p in pl:
                        self.print_path(p)

    # launcher
    # --------

    def setup(self, fname):
        self.ingest_map(fname)
        self.floyd()


def main():
    f = Floyd()

    fname = './files/paper_solutions/20r/kite_medium.map'

    f.ingest_map(fname)

    f.floyd()

    f.calculate_shortest_paths()

    f.calculate_all_paths()

if __name__ == '__main__':
    main()
