'''

Description:
    Gives naive (zero and random-indexed), bsorm bw-aware, and
        cload bw-aware routing functions given a topology.

'''

# default python libraries
import argparse
import random
import os
from itertools import chain
from copy import deepcopy
import ast
import math

# local libraries/modules
from floyd2 import Floyd

class Routing:

    # class vars
    verbose = False
    light_verbose = True

    paths_output_path_prefix = './topologies_and_routing/routepath_lists'
    all_paths_output_path_prefix = './topologies_and_routing/allpath_lists'
    nr_list_output_path_prefix = './topologies_and_routing/nr_lists'

    # arbitrary definition of infinity
    INF = Floyd.INF

    def __init__(self):

        # topo stuff
        self.filename = None
        self.r_map = None
        self.n_routers = -1
        self.n_ulinks = -1

        self.myfloyd = None
        self.hop_dists = None

        # for routing
        self.bsorm_residual_capacities = None
        self.cload_loads = None

        self.all_short_paths = None

        # # for outputs
        # self.naive_path_list = None
        # self.bsorm_bwaware_path_list = None
        # self.bsorm_bwaware_zindexed_path_list = None
        # self.cload_bwaware_path_list = None
        # self.cload_bwaware_zindexed_path_list = None

        self.path_list_dict = {}
        self.nr_map_dict = {}

    def setup(self, infile):
        # sets r_map, n_routers, and n_ulinks
        self.ingest_map(infile)

        self.filename = infile

    ###################################################################
    # helper

    def print_twodmat(self, mat):
        for i, row in enumerate(mat):
            print(f'{i} : {row}')

    def print_dist_mat(self):
        print(f'printing dist mat')
        self.print_twodmat( self.myfloyd.hop_dist)

    ###################################################################
    # setup

    def ingest_map(self, path_name):
        self.r_map = self.ingest_a_map(path_name)
        self.n_routers = len(self.r_map)
        self.n_cols = 5
        if self.n_routers == 48:
            self.n_cols = 8
        self.n_ulinks = self.calc_n_ulinks()

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

        return this_map

    def ingest_pathlist(self, path_name):

        if self.verbose:
            print(f'Ingesting path list {path_name}')

        path_list = []


        with open(path_name, 'r') as inf:
            name = inf.readline()

            for line in inf.readlines():

                # print(f'line (type {type(line)}) = {line}')

                as_list = ast.literal_eval(line)
                clean_as_list = [e for e in as_list]


                path_list.append(clean_as_list)

        n_routers = int(math.sqrt(len(path_list))) #+ 1

        if n_routers % 2 != 0:
            n_routers += 1

        if self.verbose:
            print(f'n_routers={n_routers}')
            for path in path_list:
                s = path[0]
                d = path[-1]
                print(f'{s}->{d} : {path}')

        return path_list.copy(), n_routers

    def calc_n_ulinks(self):
        mysum = 0

        for p in range(self.n_routers):
            for q in range(self.n_routers):
                if p==q:
                    continue
                mysum += self.r_map[p][q]

        return mysum

    def init_uniform_residual_capacities(self, init_cap):

        assert(self.r_map is not None)
        assert(self.n_routers != -1)

        nr = self.n_routers

        self.bsorm_residual_capacities = [[0.0 for _ in range(nr)]  for __ in range(nr)]

        for src in range(nr):
            for dest in range(nr):
                if self.r_map[src][dest] >= 1:
                    self.bsorm_residual_capacities[src][dest] = init_cap

    def init_demands(self):
        assert(self.n_routers != -1)

        nr = self.n_routers

        self.cload_loads = \
            [[0.0 for _ in range(nr)] for __ in range(nr)]

    ###################################################################
    # big worker
    def route(self, filename, alg_type=None, nonmin=None):
        # 0) setup
        #   0a) init (self): r_map, n_routers, n_links
        #      (0a completed outside this class)
        #   0b) init (floyd): r_map, n_routers, n_links, residual \
        #       capacities, demands
        #   0c) calc (floyd): hop_dist, min_hop_path_list

        # 1) naive
        # 2) bsorm bwaware: zero and random indexed
        # 3) cload bwaware: zero and random indexed
        # 4) injej

        # 5) output to .paths files
        #   5a) <topo>_naive.paths
        #   5b) <topo>_bsorm_zindexed.paths
        #   5c) <topo>_bsorm.paths
        #   5d) <topo>_cload_zindexed.paths
        #   5e) <topo>_cload.paths

        # 0) setup
        self.filename = filename
        self.setup(filename)

        base_file_name = filename.split('/')[-1]
        base_file_name = base_file_name.split('.')[0]


        #   0a) init (self): r_map, n_routers, n_links
        assert(self.r_map is not None)
        assert(self.n_routers != -1)
        assert(self.n_routers is not None)
        assert(self.n_ulinks != -1)

        init_cap = 1.0
        self.init_uniform_residual_capacities(init_cap)
        self.init_demands()

        if self.light_verbose:
            print(f'Ingested. Beginning floyd warshall...')
            print(f'-------------------------')

        #   0b) init (floyd): r_map, n_routers, n_links, residual \
        self.myfloyd = Floyd()
        # self.myfloyd.set_verbose(True)
        self.myfloyd.setup(filename)

        if 'mesh' in filename:
            self.myfloyd.is_mesh = True


        #   0c) calc (floyd): hop_dist, min_hop_path_list
        # (n_routers X n_routers X *n_paths X *path_len) * => varies



        if 'ndbt_picky' in alg_type:
            self.myfloyd.calculate_nonmin_hop_ndbt_picky_paths()

            self.all_short_ndbt_picky_paths = self.myfloyd.all_nonmin_hop_ndbt_picky_paths

            if self.light_verbose:
                print(f'Completed picky FW')
            self.output_allpathslist_ndbt_picky_raw(base_file_name)



        if 'ndbt_injej' in alg_type:
            self.myfloyd.calculate_nonmin_hop_ndbt_injej_paths()

            self.all_short_ndbt_injej_paths = self.myfloyd.all_nonmin_hop_ndbt_injej_paths

            if self.light_verbose:
                print(f'Completed picky FW')
            self.output_allpathslist_ndbt_injej_raw(base_file_name)

        elif 'picky' in alg_type:
            self.myfloyd.calculate_min_hop_picky_paths()

            self.all_short_picky_paths = self.myfloyd.all_min_hop_picky_paths

            if self.light_verbose:
                print(f'Completed picky FW')
            self.output_allpathslist_picky_raw(base_file_name)

        elif 'ndbt' in alg_type:
            self.myfloyd.calculate_nonmin_hop_ndbt_paths()

            self.all_short_ndbt_paths = self.myfloyd.all_nonmin_hop_ndbt_paths

            if self.light_verbose:
                print(f'Completed ndbt FW')
                print(f'need to output all paths list')
            self.output_allpathslist_ndbt_raw(base_file_name)

        # quit()

        # TODO end uncomment

        if 'injej' in alg_type:
            self.myfloyd.calculate_min_hop_injej_paths()

            self.all_short_injej_paths = self.myfloyd.all_min_hop_injej_paths

            if self.light_verbose:
                print(f'Completed injej FW')
            self.output_allpathslist_injej_raw(base_file_name)

        if 'odnoi' in alg_type:

            self.myfloyd.calculate_min_hop_odnoi_paths()

            self.all_short_odnoi_paths = self.myfloyd.all_min_hop_odnoi_paths

            if self.light_verbose:
                print(f'Completed odnoi FW')

            self.output_allpathslist_odnoi_raw(base_file_name)

        if 'laxinjej' in alg_type:
            self.myfloyd.calculate_min_hop_laxinjej_paths()

            self.all_short_laxinjej_paths = self.myfloyd.all_min_hop_laxinjej_paths

            if self.light_verbose:
                print(f'Completed lax injej FW')
            self.output_allpathslist_laxinjej_raw(base_file_name)     




        # quit()
        
        # TODO uncomment
        ######################################################33
        self.myfloyd.calculate_min_hop_paths()

        # shallow but wont matter
        all_paths = self.myfloyd.all_min_hop_paths
        self.all_short_paths = all_paths

        self.output_allpathslist_raw(base_file_name)

        ######################################################

        # if nonmin is not None:
        #     self.myfloyd.calculate_nonmin_hop_paths(nonmin)

        #     for s, dest_paths in enumerate(self.myfloyd.all_nonmin_hop_paths):
        #         for d, path_list in enumerate(dest_paths):
        #             for p in path_list:
        #                 all_paths[s][d].append(p)
        #     # all_paths += self.myfloyd.all_nonmin_hop_paths

        #     print(f'found {len(self.myfloyd.all_nonmin_hop_paths)} nonminimal paths {self.myfloyd.all_nonmin_hop_paths}')





        # return




        # total_hops = 0
        # i = 0

        # for src, src_map in enumerate( self.all_short_picky_paths):
        #     for dest, path_list in enumerate(src_map):
        #         if src==dest:
        #             continue
        #         a_min_path = path_list[0]

        #         print(f'picky {src}->{dest} in {len(a_min_path)} hops')

        #         total_hops += len(a_min_path)
        #         i += 1

        # print(f'total_hops = {total_hops} for {i} pairs')
        # quit()

        # 0.5) all paths
        if 'all' in alg_type:
            return

        # 1) naive
        if alg_type is None or alg_type == 'naive':
            npl = self.naive()
            key = 'naive'
            self.path_list_dict.update({key:npl})

            if self.light_verbose:
                print(f'Completed naive path list')
                print(f'-------------------------')
            if self.verbose:
                self.print_path_list(npl)
                print('-'*72)

        # 1.1) naive + picky paths
        if alg_type is None or alg_type == 'naive_picky':

            nppl = self.naive(picky=True)
            key = 'naive_picky'
            self.path_list_dict.update({key:nppl})


            if self.light_verbose:
                print(f'Completed naive picky path list')
                print(f'-------------------------')
            if self.verbose:
                self.print_path_list(pbba)
                print('-'*72)

        # 1.2) naive + injej paths
        if alg_type is None or alg_type == 'naive_injej':

            nppl = self.naive(injej=True)
            key = 'naive_injej'
            self.path_list_dict.update({key:nppl})


            if self.light_verbose:
                print(f'Completed naive injej path list')
                print(f'-------------------------')
            if verbose:
                self.print_path_list(pbba)
                print('-'*72)

        # 1.2) naive + (nonmin) ndbt paths
        if alg_type is None or alg_type == 'naive_ndbt':

            ndbta = self.naive(ndbt=True)
            key = 'nndbt'
            self.path_list_dict.update({key:ndbta})

            if self.light_verbose:
                print(f'Completed no double back turns path list')
                print(f'-------------------------')
            if verbose:
                self.print_path_list(ndbta)
                print('-'*72)

        # 1.2) naive + (nonmin) ndbt paths
        if alg_type is None or alg_type == 'naive_ndbt_picky':

            ndbtap = self.naive(ndbt_picky=True)
            key = 'nndbt_picky'
            self.path_list_dict.update({key:ndbtap})

            if self.light_verbose:
                print(f'Completed no double back turns path list')
                print(f'-------------------------')
            if verbose:
                self.print_path_list(ndbtap)
                print('-'*72)

        if alg_type is None or alg_type == 'naive_ndbt_injej':

            ndbtaie = self.naive(ndbt_injej=True)
            key = 'nndbt_injej'
            self.path_list_dict.update({key:ndbtaie})

            if self.light_verbose:
                print(f'Completed no double back turns path list')
                print(f'-------------------------')
            if verbose:
                self.print_path_list(ndbtap)
                print('-'*72)

        # return

        # return


            # self.types_of_crossings(npl)

            # name = f'{base_file_name}_naive'
            # self.output_pathlist(npl, name)
            # self.print_path_list()

        # 2) bsorm bwaware

        # self.init_uniform_residual_capacities(init_cap)
        # self.init_demands()


        # # zero indexed
        # bba_zi = self.bsorm(use_rand_idx=False)
        # self.bsorm_bwaware_zindexed_path_list = bba_zi

        # key = 'bsorm_zindexed'
        # self.path_list_dict.update({key:bba_zi})

        # if self.light_verbose:
        #     print(f'Completed bsorm zindexed path list')
        #     print(f'-------------------------')
        # if verbose:
        #     self.print_path_list(bba_zi)
        #     print('-'*72)

        # name = f'{base_file_name}_bsorm_zindexed'
        # # self.output_pathlist(bba_zi, name)

        # self.init_uniform_residual_capacities(init_cap)
        # self.init_demands()

        # # rand indexed
        # ##############
        if alg_type is None or alg_type == 'bsorm':
            self.init_uniform_residual_capacities(init_cap)
            self.init_demands()
            bba = self.bsorm()
            self.bsorm_bwaware_path_list = bba

            key = 'bsorm'
            self.path_list_dict.update({key:bba})

            if self.light_verbose:
                print(f'Completed bsorm path list')
                print(f'-------------------------')
            if verbose:
                self.print_path_list(bba)
                print('-'*72)



        # self.init_uniform_residual_capacities(init_cap)
        # self.init_demands()
        # 3.5) bsorm + picky


        # rand indexed
        # pbba = self.bsorm(picky=True)
        # self.bsorm_bwaware_path_list = pbba

        # key = 'bsorm_picky'
        # self.path_list_dict.update({key:pbba})

        # if self.light_verbose:
        #     print(f'Completed bsorm picky path list')
        #     print(f'-------------------------')
        # if verbose:
        #     self.print_path_list(pbba)
        #     print('-'*72)

        # name = f'{base_file_name}_bsorm'
        # self.output_pathlist(bba, name)

        # 3) channel load bwaware
        self.init_uniform_residual_capacities(init_cap)
        self.init_demands()

        # # zero indexed
        # clba_zi = self.cload(use_rand_idx=False)
        # self.cload_bwaware_zindexed_path_list = clba_zi


        # key = 'cload_zindexed'
        # self.path_list_dict.update({key:clba_zi})

        # if self.light_verbose:
        #     print(f'Completed cload zindexed path list')
        #     print(f'-------------------------')
        # if verbose:
        #     self.print_path_list(clba_zi)
        #     print('-'*72)

        # name = f'{base_file_name}_cload_zindexed'
        # self.output_pathlist(clba_zi, name)

        if alg_type is None or alg_type == 'cload':

            self.init_uniform_residual_capacities(init_cap)
            self.init_demands()


            clba = self.cload()
            key = 'cload'
            self.path_list_dict.update({key:clba})

            if self.light_verbose:
                print(f'Completed cload path list')
                print(f'-------------------------')
            if verbose:
                self.print_path_list(clba)
                print('-'*72)

        if alg_type is None or alg_type == 'cload_ndbt':



            self.init_uniform_residual_capacities(init_cap)
            self.init_demands()


            clbandbt = self.cload(ndbt=True)
            key = 'cloadndbt'
            self.path_list_dict.update({key:clbandbt})


            if self.light_verbose:
                print(f'Completed cload no double back turns path list')
                print(f'-------------------------')
            if verbose:
                self.print_path_list(clbandbt)
                print('-'*72)


        # self.init_uniform_residual_capacities(init_cap)
        # self.init_demands()

        # pclba = self.cload(picky=True)
        # key = 'cload_picky'
        # self.path_list_dict.update({key:pclba})

        # if self.light_verbose:
        #     print(f'Completed cload picky path list')
        #     print(f'-------------------------')
        # if verbose:
        #     self.print_path_list(plba)
        #     print('-'*72)

        # name = f'{base_file_name}_cload'
        # self.output_pathlist(clba, name)

        # # # 4) injej

        # injej_under_algs = ['naive','bsorm','cload']
        # injej_under_algs = ['naive','bsorm','cload']

        # for a_t in injej_under_algs:
        #     injej = self.injej(a_t)
        #     self.injej_path_list = injej

        #     key = f'injej_{a_t}'
        #     self.path_list_dict.update({key:injej})

        #     if self.light_verbose:
        #         print(f'Completed injej {a_t} path list')
        #         print(f'-------------------------')
        #     if verbose:
        #         self.print_path_list(injej)
        #         print('-'*72)



        # 5) output

        # FLAG

        self.output_paths_all_types(base_file_name)


        self.construct_list_of_nr_maps_all_types()

        self.output_nr_maps_all_types(base_file_name)

        # self.output_allpathslist(base_file_name)
        # self.output_allpaths_all_types_humanreadable(base_file_name)
        # self.output_allpathslist_humanreadable(self.short_paths , base_file_name)
        # self.output_allpathslist_raw(base_file_name)
        # self.output_allpathslist_picky_raw(base_file_name)
        # self.output_allpathslist_injej_raw(base_file_name)

        # quick debug
        # self.print_dist_mat()

        return

    def pathlist_to_nrl(self, pathlist_path):

        pl, nrs = self.ingest_pathlist(pathlist_path)

        self.n_routers = nrs
        nrl = self.construct_list_of_nr_maps(pl)


        # print(f'nrl is...')
        # for i,r in enumerate(nrl):
        #     print(f'r {i} : {r}')

            # if i > 86:
            #     tc = input('cont?')
            #     if 'n' in tc:
            #         quit()
        # quit()

        pathlist_name = pathlist_path.split('/')[-1]
        raw_name = pathlist_name.split('.')[0]



        self.output_nr_map(raw_name, nrl)

    ###################################################################
    # outputs

    # call this
    def output_nr_maps_all_types(self, base_file_name):

        for r_type, plist in self.nr_map_dict.items():
            name = f'{base_file_name}_{r_type}'
            self.output_nr_map(name, plist)

    # helper
    def output_nr_map(self, base_file_name, nrl):
        full_name = f'{base_file_name}.nrl'

        full_out_path = os.path.join(self.nr_list_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:
            of.write(base_file_name + '\n')
            for i,path in enumerate(nrl):
                of.write(f'{path}\n')

        #         if i > 1699:
        #             print(f'path {i} = {path}')
                
        #         if i > 1704:
        #             quit()

        print(f'Wrote to {full_out_path}')

        # quit()

    def construct_list_of_nr_maps_all_types(self):

        for r_type, plist in self.path_list_dict.items():
            nr_map_list = self.construct_list_of_nr_maps(plist)
            self.nr_map_dict.update({r_type : nr_map_list})
        return

    def construct_list_of_nr_maps(self, path_list):

        n_r = self.n_routers

        print(f'constructing nr map for # routers {n_r}')

        # flatten first dimension
        # 400 x 20
        # default next router is -1 (illegal connection flag)
        nr_map_list = [ [-1 for col in range(n_r)] for row in range(n_r*n_r)]

        for path in path_list:
            path_src = path[0]
            path_dest = path[-1]

            n_hops = len(path) - 1

            # print(f'path {path_src}->..->{path_dest} = {path}')

            for i in range(n_hops):
                hop_src = path[i]
                hop_dest = path[i+1]

                # if you are the ith src of this hop,
                #   you are the ith block of 2D next router matrices
                #   blocks of size n_r (number routers)

                which_block = hop_src*n_r

                # you are looking at the entry of src and dest of the
                #   pkt
                #   the value is the next router or dest of this hop

                which_row = which_block + path_src
                which_col = path_dest

                next_router_val = hop_dest

                # print(f'row {which_row}, col {which_col} = {next_router_val}')

                nr_map_list[which_row][which_col] = next_router_val

        if self.verbose:
            thresh = 0
            print(f'for # routers {n_r}, pathlist {path_list}')
            print(f'completed nr_map_list!')
            # print(f'nr_map_list[1700]={nr_map_list[1700]}')
            # quit()
            for i, row in enumerate(nr_map_list):

                cur = i // n_r
                f_src = i % n_r


                

                print(f'\t{i}th line, cur {cur}, flow src {f_src} : (len {len(row)}) {row}')


                # if cur > 20:
                #     thresh += n_r
                #     inp = input('cont?')
                #     if 'n' in inp:
                #         quit(-1)
                

        # quit()

        return nr_map_list

    def output_paths_all_types(self, base_file_name):

        for r_type, plist in self.path_list_dict.items():
            name = f'{base_file_name}_{r_type}'
            self.output_pathlist(plist, name)

    # def output_allpaths_all_types_humanreadable(self, base_file_name):

    #     for r_type, plist in self.path_list_dict.items():
    #         name = f'{base_file_name}_{r_type}'
    #         self.output_allpathslist_humanreadable(plist, name)

    def output_pathlist(self, path_list, base_file_name):

        full_name = f'{base_file_name}.paths'

        full_out_path = os.path.join(self.paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:
            of.write(base_file_name + '\n')
            for path in path_list:
                of.write(f'{path}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist(self, base_file_name):
        full_name = f'{base_file_name}.allpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        of.write(f'{path}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist_raw(self, base_file_name):
        full_name = f'{base_file_name}.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist_picky_raw(self, base_file_name):
        full_name = f'{base_file_name}_picky.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_picky_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist_ndbt_picky_raw(self, base_file_name):
        full_name = f'{base_file_name}_ndbt_picky.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_ndbt_picky_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist_ndbt_injej_raw(self, base_file_name):
        full_name = f'{base_file_name}_ndbt_injej.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_ndbt_injej_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist_injej_raw(self, base_file_name):
        full_name = f'{base_file_name}_injej.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_injej_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist_laxinjej_raw(self, base_file_name):
        full_name = f'{base_file_name}_laxinjej.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_laxinjej_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')


    def output_allpathslist_ndbt_raw(self, base_file_name):
        full_name = f'{base_file_name}_ndbt.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_ndbt_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')

    def output_allpathslist_odnoi_raw(self, base_file_name):
        full_name = f'{base_file_name}_odnoi.rallpaths'

        full_out_path = os.path.join(self.all_paths_output_path_prefix, \
                full_name)

        with open(full_out_path, 'w+') as of:

            for src, src_paths in enumerate(self.all_short_odnoi_paths):
                for dest, paths in enumerate(src_paths):
                    for path in paths:
                        line = ''
                        for n in path[:-1]:
                            line += f'{n} '
                        line += f'{path[-1]}'
                        of.write(f'{line}\n')

        print(f'Wrote to {full_out_path}')

    def r_is_noc(self, r_num):
        if r_num > 20:
            return True
        return False

    def types_of_crossings(self, path_list):



        for i, path in enumerate(path_list):

            crossed_into_noi = False
            crossed_into_noc = False
            last_was_noc = None

            flagged_path = False


            src_r = path[0]
            dest_r = path[-1]
            print(f'path {i} : {src_r}->{dest_r}')
            line_str = '\t\t\t'
            first_line = '\t\t\t'
            second_line = '\t\t\t'
            for r in path:
                is_noc = self.r_is_noc(r)

                if is_noc:
                    line_str += '(noc)->'
                    first_line += 'x'
                    second_line += ' '
                else:
                    line_str += '(noi)->'
                    first_line += ' '
                    second_line += 'x'

                if last_was_noc is None:
                    last_was_noc = is_noc
                    continue

                this_crosses_into_noi = False
                this_crosses_into_noc = False

                if last_was_noc and not is_noc:
                    this_crosses_into_noi = True
                elif not last_was_noc and is_noc:
                    this_crosses_into_noc = True

                if this_crosses_into_noc and crossed_into_noc:
                    print(f'FLAG!! double cross')
                    print(line_str)
                elif this_crosses_into_noi and crossed_into_noi:
                    print(f'FLAG!! double cross')
                    print(line_str)


                crossed_into_noi = this_crosses_into_noi
                crossed_into_noc = this_crosses_into_noc
                last_was_noc = is_noc

            print(line_str)

            print(first_line)
            print(second_line)



            # if i % 10 == 0:
            #     inp = input('continue?')
            #     if 'n' in inp:
            #         break


    def organize_flows_increasing_variety(self, flows, all_paths):

        sorted_flows = []

        sorting_dict = {}

        max_n_options = 0

        for flow in flows:
            s = flow[0]
            d = flow[1]

            path_options = all_paths[s][d]
            n_options = len(path_options)

            # print(f'{s}->{d} over ({n_options}) {path_options}')

            try:
                sorting_dict[n_options].append(flow)
            except:
                sorting_dict.update({n_options : [flow]}) 

            max_n_options = max(max_n_options, n_options)

        # for key, val in sorting_dict.items():
        #     print(f'sorting_dict[{key}]={val}')
        # print(f'max n = {max_n_options}')

        # quit()

        for i in range(max_n_options + 1):
            try:
                these_flows = sorting_dict[i]
            except:
                continue
            for flow in these_flows:
                sorted_flows.append(flow)

        # print(f'sorted_flows={sorted_flows}')

        # quit()

        return sorted_flows

    ###################################################################
    # naive

    def naive(self, picky=False, injej=False, ndbt=False, ndbt_picky=False, ndbt_injej=False):
        # assert(self.all_short_paths is not None)

        if picky:
            min_path_list = self.all_short_picky_paths
        elif injej:
            min_path_list = self.all_short_injej_paths
        elif ndbt:
            min_path_list = self.all_short_ndbt_paths
        elif ndbt_picky:
            min_path_list = self.all_short_ndbt_picky_paths
        elif ndbt_injej:
            min_path_list = self.all_short_ndbt_injej_paths
        else:
            min_path_list = self.all_short_paths

        nr = self.n_routers
        naive_path_list = []

        for src in range(nr):
            for dest in range(nr):
                if src==dest:
                    continue
                any_path = random.choice(min_path_list[src][dest])
                naive_path_list.append(any_path.copy())

                # first_path = min_path_list[src][dest][0]
                # naive_path_list.append(first_path.copy())

        return naive_path_list

    # def naive_picky_paths(self):
    #     assert(self.all_short_picky_paths is not None)
    #     nr = self.n_routers
    #     naive_path_list = []

    #     for src in range(nr):
    #         for dest in range(nr):
    #             first_path = self.all_short_picky_paths[src][dest][0]
    #             any_path = random.choice(self.all_short_picky_paths[src][dest])
    #             naive_path_list.append(any_path.copy())

    #     return naive_path_list

    ###################################################################
    # bsorm
    def bsorm_weight_of_edge(self, src, dest, demand):
        res_cap = self.bsorm_residual_capacities[src][dest]

        if res_cap < demand:
            return self.INF

        w = 1.0 / (res_cap - demand)
        return w

    def bsorm_update_capacities_on_path(self, path, demand):

        path_len = len(path)

        for i in range(path_len - 1):
            src = path[i]
            dest = path[i+1]

            assert(self.bsorm_residual_capacities[src][dest] >= demand)

            self.bsorm_residual_capacities[src][dest] -= demand

    def bsorm(self, use_rand_idx=True, picky=False):
        nr = self.n_routers
        # uniform demand
        demand = 1.0/(float(nr*nr - nr))

        lefts = [0,5,10,15]        
        rights = [4,9,14,19]
        exteriors = lefts + rights

        # exteriors = 
        interiors = [x for x in range(nr) if x not in exteriors]

        flows = []

        mem_flows = []
        
        
        r_map = self.r_map
        for dest in exteriors:
            for i in range(nr):
                if r_map[i][dest] >= 1:
                    mem_flows.append((i,dest,demand))
        
        
        # all "mem" flows are any src to exterior router
        sources = [x for x in range(nr)]
        if use_rand_idx:
            random.shuffle(sources)



        # these_exteriors = deepcopy(exteriors)
        # random.shuffle(these_exteriors)
        # sources = these_exteriors + interiors

        for src in sources:
            # new_flows = []

            these_exteriors = deepcopy(exteriors)
            if use_rand_idx:
                random.shuffle(these_exteriors)
            for dest in these_exteriors:
                if src == dest:
                    continue

                if (src,dest,demand) not in mem_flows:
                    mem_flows.append((src,dest,demand))
                else:
                    print(f'{(src,dest,demand)} alreday in list')
            
            # if use_rand_idx:
            #     random.shuffle(mem_flows)

            # mem_flows += new_flows


        sorted_mem_flows = self.organize_flows_increasing_variety(mem_flows, self.all_short_paths)


        # if use_rand_idx:
        #     random.shuffle(mem_flows)
        sources = [x for x in range(nr)]
        if use_rand_idx:
            random.shuffle(sources)
        other_flows = []
        for src in sources:
            these_interiors = deepcopy(interiors)
            if use_rand_idx:
                random.shuffle(these_interiors)
            for dest in these_interiors:
                if src == dest:
                    continue
                other_flows.append((src,dest,demand))


        sorted_other_flows = self.organize_flows_increasing_variety(other_flows, self.all_short_paths)


        # if use_rand_idx:
        #     random.shuffle(other_flows)

        flows = sorted_mem_flows + sorted_other_flows
        

        # mem oblivious way
        # for src in range(nr):
        #     for dest in range(nr):
        #         if src == dest:
        #             continue
        #         flows.append((src,dest,demand))



        best_paths = [[[] for _ in range(nr) ] for __ in range(nr)]

        # set this up early. doesnt matter
        for i in range(nr):
            best_paths[i][i] = [i]

        i = 0
        for f_src, f_dest, f_demand in flows:
            if self.verbose:
                print('-'*36)
                print(f'flow {i} {f_src}->{f_dest} w/ demand {f_demand}')
            i += 1

            min_hop_low_weight_path = \
                self.get_lowest_weight_path(f_src, f_dest, f_demand, 'bsorm',picky=picky)

            best_paths[f_src][f_dest] = min_hop_low_weight_path.copy()

            self.bsorm_update_capacities_on_path(min_hop_low_weight_path, f_demand)

        # flatten
        path_list = list(chain.from_iterable(best_paths))
        return path_list.copy()

    ###################################################################
    # cload

    def cload_weight_of_edge(self, src, dest, demand):
        cur_demand = self.cload_loads[src][dest]

        w = cur_demand + demand
        return w

    def cload_update_loads_on_path(self, path, demand):

        path_len = len(path)

        for i in range(path_len - 1):
            src = path[i]
            dest = path[i+1]

            if self.verbose:
                print(f'cload_loads[{src}][{dest}]={self.cload_loads[src][dest] } and demand {demand}')

            self.cload_loads[src][dest] += demand

    def cload(self, use_rand_idx=True, picky=False, ndbt=False):
        nr = self.n_routers
        # uniform demand
        demand = 1.0#/(float(nr*nr - nr))


        lefts = [0,5,10,15]        
        rights = [4,9,14,19]
        exteriors = lefts + rights

        # exteriors = 
        interiors = [x for x in range(nr) if x not in exteriors]


        flows = []

        mem_flows = []


        
        r_map = self.r_map
        for dest in exteriors:
            for i in range(nr):
                if r_map[i][dest] >= 1:
                    mem_flows.append((i,dest,demand))
        
        


        # all "mem" flows are any src to exterior router
        sources = [x for x in range(nr)]
        if use_rand_idx:
            random.shuffle(sources)
        for src in sources:
            # new_flows = []

            these_exteriors = deepcopy(exteriors)
            if use_rand_idx:
                random.shuffle(these_exteriors)
            for dest in these_exteriors:
                if src == dest:
                    continue
                if (src,dest,demand) not in mem_flows:
                    mem_flows.append((src,dest,demand))
            
            # if use_rand_idx:
            #     random.shuffle(mem_flows)

            # mem_flows += new_flows

        sorted_mem_flows = self.organize_flows_increasing_variety(mem_flows, self.all_short_paths)


        # if use_rand_idx:
        #     random.shuffle(mem_flows)
        sources = [x for x in range(nr)]
        if use_rand_idx:
            random.shuffle(sources)
        other_flows = []
        for src in sources:
            these_interiors = deepcopy(interiors)
            if use_rand_idx:
                random.shuffle(these_interiors)
            for dest in these_interiors:
                if src == dest:
                    continue
                other_flows.append((src,dest,demand))


        sorted_other_flows = self.organize_flows_increasing_variety(other_flows, self.all_short_paths)


        # if use_rand_idx:
        #     random.shuffle(other_flows)

        flows = sorted_mem_flows + sorted_other_flows
        # flows = mem_flows + other_flows

        # # old way (mem oblivious)
        # for src in range(nr):
        #     for dest in range(nr):
        #         if src == dest:
        #             continue
        #         flows.append((src,dest,demand))

        # if use_rand_idx:
        #     random.shuffle(flows)

        best_paths = [[[] for _ in range(nr) ] for __ in range(nr)]

        # set this up early. doesnt matter
        for i in range(nr):
            best_paths[i][i] = [i]

        i = 0
        for f_src, f_dest, f_demand in flows:
            if self.verbose:
                print('-'*36)
                print(f'flow {i} {f_src}->{f_dest} w/ demand {f_demand}')
            i += 1

            min_hop_low_weight_path = \
                self.get_lowest_weight_path(f_src, f_dest, f_demand, 'cload', picky=picky, ndbt=ndbt , use_rand_idx=use_rand_idx)

            best_paths[f_src][f_dest] = min_hop_low_weight_path.copy()

            self.cload_update_loads_on_path(min_hop_low_weight_path, f_demand)

        # flatten
        path_list = list(chain.from_iterable(best_paths))
        return path_list.copy()




    ###################################################################
    # injej



    def injej_picky(self, underlying_alg, use_rand_idx=True):
        nr = self.n_routers

        flows = []
        for src in range(nr):
            for dest in range(nr):
                if src == dest:
                    continue
                flows.append((src,dest))
                # print(f'added {src},{dest}')

        # print(f'flows={flows}')

        if use_rand_idx:
            random.shuffle(flows)

        # print(f'flows={flows}')

        best_paths = [[[] for _ in range(nr) ] for __ in range(nr)]

        # set this up early. doesnt matter
        for i in range(nr):
            best_paths[i][i] = [i]


        # routing idea:
        # if underlying alg has a valid path select it
        #   valid =
        #           only use noc OR
        #           only use noi OR
        #           if crossing domains, must do immediately
        #           crossing domains : src != dest domain, router along path != src/dest


        # underlying routing
        key = underlying_alg
        i_paths = self.path_list_dict[key]

        # also, lets get the noi routing
        # TODO








        i = 0
        for f_src, f_dest in flows:
            if self.verbose:
                print('-'*36)
                print(f'flow {i} {f_src}->{f_dest}')

            i += 1


            min_path_set = self.all_short_paths[f_src][f_dest]

            if self.verbose:
                print(f'Considering min_path_set[{src}][{dest}]={min_path_set}')

            # dummy max
            # TODO: what's the theoretical max?
            lowest_weight = self.INF
            lowest_weight_path = None

            for path_num, path in enumerate(min_path_set):

                # if naive
                is_valid = self.is_valid_picky_path(path)
                if not is_valid:
                    print(f'FLAG::: skipping invalid path!')
                    continue


                best_paths[f_src][f_dest] = path.copy()
                break

            print(f'found valid path {f_src}->{f_dest}={best_paths[f_src][f_dest]}')



        #     # get interposer src, dest
        #     i_src = self.map_NoC_to_NoI(f_src)
        #     i_dest = self.map_NoC_to_NoI(f_dest)

        #     # print(f'flow #{i} {f_src}->{f_dest}')
        #     # print(f'injej::\n\ti_src,dest={i_src},{i_dest}')
        #     # print(f'\n\tipaths={i_paths}')

        #     # get interposer path
        #     i_path = self.get_path_from_flat_list(i_src, i_dest, i_paths)

        #     full_path = []
        #     if f_src != i_src:
        #         full_path.append(f_src)
        #     for n in i_path:
        #         full_path.append(n)
        #     if f_dest != i_dest:
        #         full_path.append(f_dest)

        #     best_paths[f_src][f_dest] = full_path.copy()

        #     # print(f'found injej path {f_src}->{f_dest}={full_path}')

        # flatten
        path_list = list(chain.from_iterable(best_paths))
        return path_list.copy()

    def injej(self, underlying_alg, use_rand_idx=True):
        nr = self.n_routers

        flows = []
        for src in range(nr):
            for dest in range(nr):
                if src == dest:
                    continue
                flows.append((src,dest))
                # print(f'added {src},{dest}')

        # print(f'flows={flows}')

        if use_rand_idx:
            random.shuffle(flows)

        # print(f'flows={flows}')

        best_paths = [[[] for _ in range(nr) ] for __ in range(nr)]

        # set this up early. doesnt matter
        for i in range(nr):
            best_paths[i][i] = [i]

        # underlying routing
        key = underlying_alg
        i_paths = self.path_list_dict[key]



        i = 0
        for f_src, f_dest in flows:
            if self.verbose:
                print('-'*36)
                print(f'flow {i} {f_src}->{f_dest}')

            i += 1

            # get interposer src, dest
            i_src = self.map_NoC_to_NoI(f_src)
            i_dest = self.map_NoC_to_NoI(f_dest)

            # print(f'flow #{i} {f_src}->{f_dest}')
            # print(f'injej::\n\ti_src,dest={i_src},{i_dest}')
            # print(f'\n\tipaths={i_paths}')

            # get interposer path
            i_path = self.get_path_from_flat_list(i_src, i_dest, i_paths)

            full_path = []
            if f_src != i_src:
                full_path.append(f_src)
            for n in i_path:
                full_path.append(n)
            if f_dest != i_dest:
                full_path.append(f_dest)

            best_paths[f_src][f_dest] = full_path.copy()

            # print(f'found injej path {f_src}->{f_dest}={full_path}')

        # flatten
        path_list = list(chain.from_iterable(best_paths))
        return path_list.copy()

    def map_NoC_to_NoI(self, r):
        # for mesh
        if self.n_routers == 128:
            return r % 64

        n_noi = 20
        n_rows_noi = 4
        n_per_row_noi = n_noi // n_rows_noi

        # else 20r NoI
        if r < n_noi:
            return r

        # zero the index for the noc router
        zindexed_r = r - n_noi

        noc_row = zindexed_r // 8
        noc_col = zindexed_r % 8


        noi_row = noi_row = noc_row // 2
        noi_col = noi_col = (noc_col +1) //2

        noi_r = noi_row*n_per_row_noi + noi_col


        return noi_r

    def is_valid_picky_path(self, path):

        crossed_into_noi = False
        crossed_into_noc = False

        into_noi_crossings = 0
        into_noc_crossings = 0

        inject_hop = None
        eject_hop = None

        last_was_noc = None

        flagged_path = False

        print(f'picky_path():: path={path}')


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

        print(f'path {src_r}->{dest_r} : injects at {inject_hop}and ejects at {eject_hop}')
        print(f'\t\t: noc crossings = {into_noc_crossings} and into noi crossings = {into_noi_crossings}')


        if into_noc_crossings > 1:
            return False
        if into_noi_crossings > 1:
            return False

        if should_never_cross and (crossed_into_noi or crossed_into_noc):
            print(f'should never cross')
            return False

        if crossed_into_noi and inject_hop != 1:
            print(f'injected at wrong time')
            return False
        if crossed_into_noc and eject_hop != len(path) - 1:
            print(f'ejected at wrong time')
            return False



        return True


    ###################################################################
    # both


    def get_lowest_weight_path(self, src, dest, demand, weight_type, picky=False, ndbt=False, use_rand_idx=False):

        # switch here. so simple
        if picky:
            min_path_set = self.all_short_picky_paths[src][dest]
        elif ndbt:
            min_path_set = self.all_short_ndbt_paths[src][dest]
        else:
            min_path_set = self.all_short_paths[src][dest]


        if self.verbose:
            print(f'Considering min_path_set[{src}][{dest}]={min_path_set}')

        if use_rand_idx:
            random.shuffle(min_path_set)



        # dummy max
        # TODO: what's the theoretical max?
        lowest_weight = self.INF
        lowest_max_weight = self.INF
        lowest_weight_path = None

        for path_num, path in enumerate(min_path_set):

            if verbose:
                print(f'considering {path_num}th path : {path}')
            # if picky_injej:
            #     is_valid = self.is_valid_picky_path(path)
            #     if not is_valid:
            #         print(f'FLAG::: skipping invalid path!')
            #         continue

            path_len = len(path)
            path_weight = 0
            path_max_weight = 0
            for i in range(path_len - 1):
                node_a = path[i]
                node_b = path[i+1]

                w = 0
                if weight_type == 'bsorm':
                    w = self.bsorm_weight_of_edge(node_a, node_b, demand)
                else:
                    w = self.cload_weight_of_edge(node_a, node_b, demand)
                path_weight += w

                if w > path_max_weight:
                    path_max_weight = w

            # lowest max load (prioriry)
            if path_max_weight < lowest_max_weight:
                if verbose:
                    print(f'found new lowest max laod={path_max_weight} (was {lowest_max_weight}) from path {path}')
                lowest_max_weight = path_max_weight
                lowest_weight = path_weight
                lowest_weight_path = path.copy()        

            # otherwise if lower total load but same max (secondary)
            elif path_weight < lowest_weight and path_max_weight == lowest_max_weight:
                if verbose:
                    print(f'found new lowest total load={path_weight} (was {lowest_weight}) from path {path}')
                lowest_max_weight = path_max_weight
                lowest_weight = path_weight
                lowest_weight_path = path.copy()
            else:
                pass
                # print(f'path_weoghht {path_weight} too heavy for lowest {lowest_weight}')

        if self.verbose:
            print(f'Found lowest weight path between {src} -> {dest}')
            print(f'\tpath (len={len(lowest_weight_path)}) (weight={lowest_weight}, max={lowest_max_weight}) = {lowest_weight_path}')

        return lowest_weight_path.copy()

    def get_path_from_flat_list(self, src, dest, pl):
        # print(f'looking for {src}->{dest}')

        if src == dest:
            # print(f'found self')
            return [src]

        for p in pl:
            if src != p[0]:
                continue
            if dest != p[-1]:
                continue

            # print(f'found {p}')
            return p.copy()

    ###################################################################
    # prints

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

global verbose
verbose = False

def convert_all_in_dir(dir, mask=None):
    global verbose

    for root, dirs, files  in os.walk(dir):

        for file in files:


            if mask is not None:
                if mask not in file:
                    continue

            file_path = os.path.join(root,file)

            print('\n' + '='*72 )
            print(f'Beginning file:\n\t{file} ({file_path})\n')
            convert_pathlist_to_nrl(file_path)
            print(f'\nCompleted file:\n\t{file} ({file_path})')
            print('='*72 +'\n')
            # quit()


def convert_pathlist_to_nrl(fname):

    global verbose

    r = Routing()

    r.verbose = verbose

    r.pathlist_to_nrl(fname)

    del(r)

def route_file(fname, alg=None, nonmin=None):

    global verbose

    r = Routing()

    r.verbose = verbose

    r.route(fname, alg_type=alg, nonmin=nonmin)

    del(r)

def route_all_in_dir(dir, mask, nonmin, alg=None):

    global verbose

    for root, dirs, files  in os.walk(dir):

        for file in files:


            if mask is not None:
                if mask not in file:
                    continue

            file_path = os.path.join(root,file)

            print('\n' + '='*72 )
            print(f'Beginning file:\n\t{file} ({file_path})\n')
            route_file(file_path, alg=alg, nonmin=nonmin)
            print(f'\nCompleted file:\n\t{file} ({file_path})')
            print('='*72 +'\n')

def main():
    parser = argparse.ArgumentParser(description='Verify topology values')
    parser.add_argument('--filename',type=str,help='.map file to evaluate')
    parser.add_argument('--pathlist',type=str,help='pathlist to convert to nrl')
    parser.add_argument('--convert_pathlist',action='store_true',help='...')

    parser.add_argument('--all_in_dir', type=str, help='directory to list for all files')
    parser.add_argument('--all_mask', type=str, help='only do for files with this str in filename')
    parser.add_argument('--verbose',action='store_true',help='debug prints')
    parser.add_argument('--allow_nonmin_by',type=int,help='extra distance allowed in path')
    parser.add_argument('--alg',type=str,help='alg (naive, bsorm, cload)')

    # for quick testing
    parser.add_argument('--qt',action='store_true')

    args = parser.parse_args()

    if args.qt:
        args.filename = './files/paper_solutions/20r/kite_large.map'
        args.verbose = True

    global verbose
    verbose = args.verbose
        

    if args.convert_pathlist and args.all_in_dir is not None:
        convert_all_in_dir(args.all_in_dir)

    elif args.pathlist is not None:
        convert_pathlist_to_nrl(args.pathlist)

    elif args.all_in_dir is not None:
        route_all_in_dir(args.all_in_dir, args.all_mask, args.allow_nonmin_by, alg=args.alg, )

    elif args.filename is not None:
        route_file(args.filename, alg=args.alg, nonmin=args.allow_nonmin_by)

    else:
        print('No file list provided. Exiting...')
        quit(-1)

if __name__ == '__main__':
    main()

