from sys import int_info
from m5.params import *
from m5.objects import *

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology

import math
import ast

class FS_NoCI_EscapeVirtualNetworks(SimpleTopology):
    description='FS_NoCI_EscapeVirtualNetworks'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):

        verbose = True
        verbose = False

        nodes = self.nodes

        # cpu/mem organization
        n_cpus = options.num_cpus
        n_dirs = options.num_dirs
        n_noi_routers = options.noi_routers
        n_noc_routers = 64
        n_chiplets = options.num_chiplets

        # traffic type
        is_mem_or_coh = options.mem_or_coh

        # clks
        noi_clk = options.noi_clk
        noc_clk = options.noc_clk

        n_noc_rows = options.noc_rows

        n_noi_rows = 4
        if n_noi_routers == 64:
            n_noi_rows = 8

        per_row = n_noi_routers // n_noi_rows

        N_CPUS = 64
        N_CHIPLETS = 4
        assert(n_cpus == N_CPUS)
        assert(n_chiplets == N_CHIPLETS)


        # layout
        NOC_ROWS = 4
        assert(n_noc_rows == NOC_ROWS)

        # layout
        n_cpus_per_chiplet = n_cpus // n_chiplets

        noc_per_row = n_cpus_per_chiplet // n_noc_rows

        # useless?
        noi_per_row = n_noi_routers // n_noi_rows

        l1_caches = [n for n in nodes if n.type == 'L1Cache_Controller']
        l2_caches = [n for n in nodes if n.type == 'L2Cache_Controller']
        dirs = [n for n in nodes if n.type == 'Directory_Controller']
        dmas = [n for n in nodes if n.type == 'DMA_Controller']
        others = [n for n in nodes if n not in l1_caches and n not in l2_caches and n not in dirs and n not in dmas]


        print(f'l1_caches({len(l1_caches)})={l1_caches}\n')
        print(f'l2_caches({len(l2_caches)})={l2_caches}\n')
        print(f'dirs({len(dirs)})={dirs}\n')
        print(f'dmas({len(dmas)})={dmas}\n')
        print(f'others({len(others)})={others}\n')

        # assert(n_cpus == len(caches))
        # assert(n_noi_routers == n_cpus)
        # assert(n_dirs == len(dirs))

        # nothing else (dma)
        # assert(n_cpus + n_dirs == len(nodes))



        # obligatory required sets
        link_latency = options.link_latency
        router_latency = options.router_latency

        # Will be part of self later
        # 1:1 ratio
        n_routers = n_noi_routers + n_noc_routers

        ###############################################################


        # vcmap_path = options.vc_map_file
        # vc_map = self.ingest_map(vcmap_path, n_routers)


        # nrmap_path = options.nr_map_file
        # nr_map = self.ingest_map(nrmap_path, n_routers)

        flat_nr_map_path = options.flat_nr_map_file

        # this is 3d (20x20x20) or (84x84x84)
        (flat_nr_maps, routing_alg) = self.ingest_flat_map_list(flat_nr_map_path, n_routers)

        flat_vn_map_path = options.flat_vn_map_file

        # this is 2d (20x20) or (84x84)
        flat_vn_map = self.ingest_flat_map(flat_vn_map_path, n_routers)

        # print(f'Ingested flat nr_maps({len(flat_nr_maps)})=\n\t{flat_nr_maps}')

        # print(f'flat_nr_maps[46] (len {len(flat_nr_maps[46])})={flat_nr_maps[46]}')

        # print(f'Ingested flat vc map({len(flat_vn_map)})=\n\t{flat_vn_map}')
        # quit(-1)


        # CDC stuff
        noc_clk_domain = SrcClockDomain(clock = noc_clk, voltage_domain=\
                    VoltageDomain(voltage=options.sys_voltage) )

        noi_clk_domain = SrcClockDomain(clock = noi_clk, voltage_domain=\
                    VoltageDomain(voltage=options.sys_voltage) )


        # TODO make latency dependent on link length
        # # this is for 1d
        # routers = [Router(router_id=i, latency = router_latency, \
        #     dest_to_vc=vc_map[i], next_router_map=nr_map[i]) \
        #     for i in range(n_routers)]

        # this is for 2d
        # pass correct block of maps from flat_nr_maps
        #   and copy of vn map
        routers = [Router(router_id=i, latency = router_latency,\
                # test_params=True,\
                # dest_to_vc=vc_map[i], next_router_map=nr_map[i],\
                flat_next_router_map=flat_nr_maps[i],\
                # flat_src_dest_to_evn=flat_vn_map
                )\
            for i in range(n_routers)]

        # [0, n_noi_routers) = [0,20)
        for r in range(n_noi_routers):
            routers[r].clk_domain = noi_clk_domain

        # [n_noi_routers, n_routers) = [20,84)
        for r in range(n_noi_routers, n_routers):
            routers[r].clk_domain = noc_clk_domain


        # important, set network stuff
        ############################################################################################################################3

        network.flat_src_dest_to_evn = flat_vn_map
        network.use_escape_vns = options.use_escape_vns
        network.n_deadlock_free = options.evn_n_deadlock_free
        network.evn_deadlock_partition = options.evn_deadlock_partition
        network.min_n_deadlock_free = options.evn_min_n_deadlock_free

        # should be false
        network.synth_traffic = options.synth_traffic


        ############################################################################################################################3

        # for unique identification
        link_count = 0

        int_links = []
        ext_links = []

        ###############################################################
        # ext links
        ###############################################################

        # l1s -> noc routers
        # assert(len(l1_caches) == n_cpus)
        for i in range(len(l1_caches)):
            idx = n_noi_routers + i
            # print(f'Adding external link: l1 cache node {i} <-> router {idx} ')

            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= l1_caches[i],
                                    int_node= routers[idx],
                                    latency=link_latency,

                                    # NoC on same freq as cores
                                    # int_cdc=False
                                    ))
            link_count += 1


        #print(f'len of l2caches = {len(l2_caches)}')
        #quit()

        # l2s -> noc routers
        assert(len(l2_caches) == 4 or len(l2_caches) == 64 or len(l2_caches) == 0)

        if len(l2_caches) == 4:
            l2_noc_routers = [18, 21, 42, 45]
            for i in range(len(l2_caches)):
                idx = l2_noc_routers[i] + n_noi_routers
                # print(f'Adding external link: l2 cache node {i} <-> router {idx} ')

                ext_links.append(ExtLink(link_id=link_count,
                                        ext_node= l2_caches[i],
                                        int_node= routers[idx],
                                        latency=link_latency,

                                        # NoC on same freq as cores
                                        # int_cdc=False
                                        ))
                link_count += 1
        # 64 l2 caches
        if len(l2_caches) == 64:
            for i in range(len(l2_caches)):
                idx = i + n_noi_routers
                # print(f'Adding external link: l2 cache node {i} <-> router {idx} ')

                ext_links.append(ExtLink(link_id=link_count,
                                        ext_node= l2_caches[i],
                                        int_node= routers[idx],
                                        latency=link_latency,

                                        # NoC on same freq as cores
                                        # int_cdc=False
                                        ))
                link_count += 1

        # dmas -> noc routers
        # assert(len(dmas) == 2)
        dma_noi_routers = [5,14]
        if n_noi_routers == 64:
            dma_noi_routers = [24,39]

        dma_noi_routers = [0,4,5,9,10,14,15,19,0,4,5,9,10,14,15,19,0,4,5,9,10,14,15,19,0,4,5,9,10,14,15,19]

        for i in range(len(dmas)):
            idx = dma_noi_routers[i]
            # print(f'Adding external link: dma node {i} <-> router {idx} ')

            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= dmas[i],
                                    int_node= routers[idx],
                                    latency=link_latency,
                                    ext_cdc=True
                                    ))
            link_count += 1


        edges = []

        # most topologies
        if n_noi_routers == 20:
            edges = [0,4,5,9,10,14,15,19]

        # aligned topologies
        elif n_noi_routers == 24:
            edges = [0,5,6,11,12,17,18,23]
        # mesh
        elif n_noi_routers == 64:
            edges = [x for x in range(0,64,8) ]
            edges += [x for x in range(7,64,8) ]
        else:
            print('error on n_noi_routers')
            quit(-1)

        # n_dirs should be 16 so 2 per
        dirs_per_router = n_dirs // len(edges)
        edges = edges*dirs_per_router

        # print(f'edges({len(edges)})={edges}')
        # print(f'n_dirs={n_dirs}')

        assert(len(edges) == n_dirs)

        for i in range(n_dirs):

            # cdc on faster
            # ext is noc. int is noi


            # noc faster => cdc on ext
            if noi_clk < noc_clk:
                has_ext_cdc = True
                has_int_cdc = False
            # noi slow
            else:
                has_ext_cdc = False
                has_int_cdc = True


            # idx = i % n_routers
            targ = edges[i]
            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= dirs[i],
                                    int_node= routers[targ],
                                    latency=link_latency,
                                    # NoI on diff freq than cores
                                    # CDC on slower => ext side
                                    ext_cdc=has_ext_cdc,
                                    int_cdc=has_int_cdc))
            link_count += 1

            if verbose:
                print(f'Adding external link (id {link_count}): (memory) dir node {i} (cdc? {has_ext_cdc}) <-> noi router {targ} (cdc? {has_int_cdc})')



        ###############################################################
        # int links
        ###############################################################

        # routers -> routers
        # based on topology .map file
        map_file = options.router_map_file
        r_map = self.ingest_map(map_file, n_routers)

        n_int_links = 0

        # vll
        # weight_mat = self.calc_vll_mat(n_routers)

        for src_r in range(n_routers):
            for dest_r, is_connected in enumerate(r_map[src_r]):
                assert(src_r < n_routers)
                assert(dest_r < n_routers)

                if(src_r == dest_r):
                        continue

                if(is_connected >= 1):


                    this_link_latency = link_latency

                    # vll
                    # if options.use_vll:
                    #     this_link_latency = weight_mat[src_r][dest_r]

                    s_row = src_r // per_row
                    s_col = src_r % per_row

                    d_row = dest_r // per_row
                    d_col = dest_r % per_row

                    w=1
                    s_name = f'src{src_r}_dest{dest_r}'
                    d_name = f'dest{dest_r}_src{src_r}'

                    # src noi
                    if src_r < n_noi_routers:
                        # noi -> noi
                        if dest_r < n_noi_routers:
                            int_links.append(IntLink(link_id=link_count,
                                        src_node=routers[src_r],
                                        dst_node=routers[dest_r],
                                        src_outport=s_name,
                                        dst_inport=d_name,
                                        latency = this_link_latency,
                                        # TODO UNCOMMENT?
                                        # clk_domain=noi_clk_domain,
                                        ))

                            if verbose:
                                print(f'Adding noi internal link (id {link_count}) {src_r}->{dest_r}')


                        # noi -> noc
                        else:
                            # dest is noc


                            # noc faster => cdc on noc=dest
                            if noi_clk < noc_clk:
                                has_src_cdc = False
                                has_dest_cdc = True
                            # noi slow
                            else:
                                has_src_cdc = True
                                has_dest_cdc = False
                            int_links.append(IntLink(link_id=link_count,
                                        src_node=routers[src_r],
                                        dst_node=routers[dest_r],
                                        src_outport=s_name,
                                        dst_inport=d_name,
                                        latency = this_link_latency,
                                        # noc always slower. noc slower

                                        # TODO UNCOMMENT
                                        # clk_domain = noc_clk_domain,
                                        # dst_cdc = False,
                                        # # cdc on noi (src)
                                        dst_cdc = has_dest_cdc,
                                        src_cdc = has_src_cdc
                                        ))
                            if verbose:
                                
                                print(f'Adding noi->noc internal link (id {link_count}) {src_r} (cdc? {has_src_cdc}) -> (cdc? {has_dest_cdc}) {dest_r}')
                                #  | (noc_domain) noc router <----out_link,in_link--->| CDC (noi domain) noi router |
                    # src noc
                    else:
                        # noc -> noi
                        if dest_r < n_noi_routers:

                            # cdc on slower
                            # cdc on faster?
                            # dest is noi

                            # noc slower => cdc on noc
                            # if noi_clk > noc_clk:
                            # noc faster => cdc on noc
                            if noi_clk < noc_clk:
                                has_src_cdc = True
                                has_dest_cdc = False
                            # noi slow
                            else:
                                has_dest_cdc = True
                                has_src_cdc = False


                            int_links.append(IntLink(link_id=link_count,
                                        src_node=routers[src_r],
                                        dst_node=routers[dest_r],
                                        src_outport=s_name,
                                        dst_inport=d_name,
                                        latency = this_link_latency,
                                        # noc always slower
                                        # TODO UNCOMMENT
                                        # clk_domain = noc_clk_domain,
                                        # cdc on noi (dest)
                                        src_cdc = has_src_cdc,
                                        dst_cdc = has_dest_cdc
                                        ))

                            if verbose:
                                print(f'Adding noc->noi internal link (id {link_count}) {src_r} (cdc? {has_src_cdc}) -> (cdc? {has_dest_cdc}) {dest_r}')
                            #  | (noc_domain) noc router <----out_link,in_link--->| CDC (noi domain) noi router |
                        # noc -> noc
                        else:
                            int_links.append(IntLink(link_id=link_count,
                                        src_node=routers[src_r],
                                        dst_node=routers[dest_r],
                                        src_outport=s_name,
                                        dst_inport=d_name,
                                        latency = this_link_latency,
                                        # clk_domain=noc_clk_domain,
                                        ))
                            if verbose:
                                print(f'Adding noc internal link (id {link_count}) {src_r}->{dest_r}')


                    # print(f'Adding internal link (id:{n_int_links}) {s_name} ({src_r})->{d_name} ({dest_r}) latency: {this_link_latency} and weight: {w}')
                    link_count += 1
                    n_int_links +=1

        #####

        # quit(-1)

        # print(f'int_links[0:10]={int_links[0:10]}')
        # print(f'int_links[0:10]={int_links[0:20]}')
        # print(f'int_links[20:30]={int_links[20:30]}')

        # Required to be set
        network.int_links = int_links
        network.ext_links = ext_links
        network.routers = routers

        if verbose:
            quit(-1)

    # Register nodes with filesystem
    def registerTopology(self, options):

        n_cpus = options.num_cpus
        per_cpu = MemorySize(options.mem_size) // n_cpus
        print(f'per_cpu={per_cpu}')
        for i in range(n_cpus):
            FileSystemConfig.register_node([i],
                    per_cpu, i)



    def ingest_map(self, path_name, n_routers):


        print(f'ingesting {path_name}')

        r_map = []

        with open(path_name, 'r') as in_file:

            # for _router in range(0,n_routers):
            #     row = in_file.readline()
            for row in in_file:
                row = row.replace('\n','')
                r_conns = row.split(" ")
                if '' in r_conns:
                    r_conns.remove('')
                # print(f'row={row}')
                # print(r_conns)
                # print(type(r_conns[0]))

                try:
                    r_conns = [int(elem) for elem in r_conns]
                except Exception as e:
                    print(f'e={e}')
                    r_conns = [int(float(elem)) for elem in r_conns]
                r_map.append(r_conns)

        # print(f'r_map({len(r_map)})={r_map}')
        #input('cont?')

        assert(len(r_map) == n_routers)

        return r_map

    def ingest_flat_map(self, path_name, n_routers):
        print(f'ingesting {path_name}')

        r_map = []

        with open(path_name, 'r') as in_file:

            # for _router in range(0,n_routers):
            #     row = in_file.readline()
            for row in in_file:

                row = row.replace('\n','')
                r_conns = row.split(" ")
                if '' in r_conns:
                    r_conns.remove('')
                # print(f'row={row}')
                # print(r_conns)
                # print(type(r_conns[0]))

                try:
                    r_conns = [int(elem) for elem in r_conns]
                except Exception as e:
                    print(f'e={e}')
                    r_conns = [int(float(elem)) for elem in r_conns]

                # r_map.append(r_conns)
                r_map += r_conns

        #input('cont?')

        # assert(len(r_map) == n_routers)b

        return r_map

    def ingest_flat_map_list(self, path_name, n_routers):

        print(f'ingesting {path_name} w/ # rotuers = {n_routers}')
        # quit()

        routing_alg = None
        flat_nr_map = []
        nr_map_dict = {}

        iter = 0

        with open(path_name, 'r') as inf:
            routing_alg = inf.readline()

            for i in range(n_routers):
                # flat_nr_map.append([])
                a_routers_map = []
                for j in range(n_routers):
                    thisline = inf.readline()


                    as_list = ast.literal_eval(thisline)
                    clean_as_list = [e for e in as_list]

                    # print(f'\titer {iter}. routing table for router {i} '+
                    #     f' row (src) {j} : (len {len(clean_as_list)})\n\t{clean_as_list}')
                    flat_nr_map.append(clean_as_list)
                    a_routers_map += clean_as_list

                    iter += 1

                # print(f'\titer {iter}. routing table for router {i} '+
                #     f' : (len {len(a_routers_map)})') #\n\t{a_routers_map}')

                # if i >= 0:
                #     inp = input('cont?')
                #     if 'n' in inp:
                #         quit(-1)

                flat_nr_map.append(a_routers_map.copy())
                nr_map_dict.update({i : a_routers_map.copy()})
        #         print(f'\tflat_nr_map({len(flat_nr_map)}x{len(flat_nr_map[0])})')


        # print(f'flat_nr_map({len(flat_nr_map)})')
        # for alist in flat_nr_map:
        #     for row in alist:
        #         print(f'{row}')

        new_flat = []
        for i, r_nrl in nr_map_dict.items():
            new_flat.append(r_nrl)
        #     print(f'\tnew_flat_nr_map({len(new_flat)}x{len(new_flat[0])})')


        # print(f'new_flat({len(new_flat)})')


        # quit(-1)

        return (new_flat, routing_alg)
