from sys import int_info
from m5.params import *
from m5.objects import *

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology

import math
import ast

class EscapeVirtualNetworks(SimpleTopology):
    description='EscapeVirtualNetworks'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes

        n_cpus = options.num_cpus
        n_dirs = options.num_dirs
        n_noi_routers = options.noi_routers

        is_mem_or_coh = options.mem_or_coh

        cpu_clk = options.ruby_clock
        noi_clk = options.noi_clk

        # noi_clk_int =



        n_rows = 4
        if n_noi_routers == 64:
            n_rows = 8

        per_row = n_noi_routers // n_rows

        # N_CPUS = 64
        # assert(n_cpus == N_CPUS)
        # for now equal dirs to cpus
        # assert(n_dirs == n_cpus)

        # no dma controllers
        assert('DMA_Controller' not in [n.type for n in nodes])

        caches = [n for n in nodes if n.type != 'Directory_Controller']
        dirs = [n for n in nodes if n.type == 'Directory_Controller']

        # print(f'caches({len(caches)})={caches}')
        # print(f'dirs({len(dirs)})={dirs}')

        assert(n_cpus == len(caches))
        # assert(n_noi_routers == n_cpus)
        # assert(n_dirs == len(dirs))

        # nothing else (dma)
        # assert(n_cpus + n_dirs == len(nodes))

        # obligatory required sets
        link_latency = options.link_latency
        router_latency = options.router_latency

        # Will be part of self later
        # 1:1 ratio
        n_routers = n_noi_routers


        # vcmap_path = options.vc_map_file
        # vc_map = self.ingest_map(vcmap_path, n_routers)


        # nrmap_path = options.nr_map_file
        # nr_map = self.ingest_map(nrmap_path, n_routers)

        flat_nr_map_path = options.flat_nr_map_file

        # this is 3d (20x20x20)
        (flat_nr_maps, routing_alg) = self.ingest_flat_map_list(flat_nr_map_path, n_routers)

        flat_vn_map_path = options.flat_vn_map_file

        # its 2d
        flat_vn_map = self.ingest_flat_map(flat_vn_map_path, n_routers)

        # print(f'Ingested flat nr_maps({len(flat_nr_maps)})=\n\t{flat_nr_maps}')

        # print(f'Ingested flat vc map({len(flat_vn_map)})=\n\t{flat_vn_map}')
        # quit()


        # CDC stuff
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

        # important, set network stuff
        ############################################################################################################################3

        network.flat_src_dest_to_evn = flat_vn_map
        network.use_escape_vns = options.use_escape_vns
        network.n_deadlock_free = options.evn_n_deadlock_free
        network.evn_deadlock_partition = options.evn_deadlock_partition
        network.min_n_deadlock_free = options.evn_min_n_deadlock_free

        network.synth_traffic = options.synth_traffic


        ############################################################################################################################3

        ext_cdc_required = True
        if noi_clk == cpu_clk:
            ext_cdc_required = False

        if ext_cdc_required:
            for r in range(n_noi_routers):
                routers[r].clk_domain = noi_clk_domain

        # print(f'ext_cdc_required = {ext_cdc_required}')

        # quit(-1)

        int_links = []
        ext_links = []


        # ext links
        # l1s/dirs -> routers
        link_count = 0
        for i in range(n_cpus):
            idx = i % n_routers
            # print(f'Adding external link: l1 cache node {i} <-> noi router {idx} ')

            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= caches[i],
                                    int_node= routers[idx],
                                    latency=link_latency,
                                    ext_cdc=ext_cdc_required))
            link_count += 1



        # if coh
        if is_mem_or_coh == 'coh':
            for i in range(n_dirs):
                idx = i % n_routers
                # print(f'Adding external link (id {link_count}): dir node {i} <-> noi router {idx}')

                ext_links.append(ExtLink(link_id=link_count,
                                        ext_node= dirs[i],
                                        int_node= routers[idx],
                                        latency=link_latency,
                                        ext_cdc=ext_cdc_required))
                link_count += 1

        else:
            edges = []
            if n_noi_routers == 20:
                edges = [0,4,5,9,10,14,15,19]


            elif n_noi_routers == 24:
                edges = [0,5,6,11,12,17,18,23]
            elif n_noi_routers == 64:
                edges = [x for x in range(0,64,8) ]
                edges += [x for x in range(7,64,8) ]
            elif n_noi_routers == 48:
                edges = [x for x in range(0,48,8)]
                edges += [x for x in range(7,48,8)]
            else:
                print('error on n_noi_routers')
                quit(-1)

            dirs_per_router = n_dirs // len(edges)
            edges = edges*dirs_per_router

            # print(f'edges({len(edges)})={edges}')
            # print(f'n_dirs={n_dirs}')

            assert(len(edges) == n_dirs)

            for i in range(n_dirs):

                # idx = i % n_routers
                targ = edges[i]
                # print(f'Adding external link (id {link_count}): dir node {i} <-> noi router {targ}')
                ext_links.append(ExtLink(link_id=link_count,
                                        ext_node= dirs[i],
                                        int_node= routers[targ],
                                        latency=link_latency,
                                        ext_cdc=ext_cdc_required))
                link_count += 1



        # int links
        # routers -> routers
        # based on topology .sol file
        map_file = options.router_map_file
        r_map = self.ingest_map(map_file, n_noi_routers)

        n_int_links = 0

        weight_mat = self.calc_vll_mat(n_routers)

        for src_r in range(n_routers):
            for dest_r, is_connected in enumerate(r_map[src_r]):
                assert(src_r < n_routers)
                assert(dest_r < n_routers)

                if(src_r == dest_r):
                        continue

                if(is_connected >= 1):


                    this_link_latency = link_latency
                    # vll
                    if options.use_vll:
                        this_link_latency = weight_mat[src_r][dest_r]


                    # # useless?
                    # s_name = f'r{src_r}_lc{link_count}'
                    # d_name = f'r{dest_r}_lc{link_count}'

                    s_row = src_r // per_row
                    s_col = src_r % per_row

                    d_row = dest_r // per_row
                    d_col = dest_r % per_row


                    w=1
                    s_name = f'src{src_r}_dest{dest_r}'
                    d_name = f'dest{dest_r}_src{src_r}'
                    int_links.append(IntLink(link_id=link_count,
                                    src_node=routers[src_r],
                                    dst_node=routers[dest_r],
                                    src_outport=s_name,
                                    dst_inport=d_name,
                                    latency = this_link_latency,
                                    # weight=w,
                                    # clk_domain=noi_clk_domain,
                                    ))
                    # print(f'Adding internal link (id:{n_int_links}) {s_name} ({src_r})->{d_name} ({dest_r}) latency: {this_link_latency} and weight: {w}')
                    link_count += 1
                    n_int_links +=1

        # print(f'int_links[0:10]={int_links[0:10]}')
        # print(f'int_links[0:10]={int_links[0:20]}')
        # print(f'int_links[20:30]={int_links[20:30]}')

        # Required to be set
        network.int_links = int_links
        network.ext_links = ext_links
        network.routers = routers

    # # Register nodes with filesystem
    # def registerTopology(self, options):

    #     # closest_power_of_two = int(math.log(options.num_cpus,2))**2
    #     # # if():
    #     # print(f'closest_power_of_two={closest_power_of_two}')
    #     # per_cpu = MemorySize(options.mem_size) // closest_power_of_two
    #     # for i in range(closest_power_of_two):
    #     #     FileSystemConfig.register_node([i],
    #     #             per_cpu, i)

    #     # n_cpus = 16
    #     # per_cpu = MemorySize(options.mem_size) // 16
    #     # for i in range(n_cpus):
    #     #     FileSystemConfig.register_node([i],
    #     #             per_cpu, i)


    #     n_cpus = options.num_cpus
    #     per_cpu = MemorySize(options.mem_size) // n_cpus
    #     print(f'per_cpu={per_cpu}')
    #     for i in range(n_cpus):
    #         FileSystemConfig.register_node([i],
    #                 per_cpu, i)

    # Register nodes with filesystem
    def registerTopology(self, options):

        n_cpus = options.num_cpus
        per_cpu = MemorySize(options.mem_size) // n_cpus
        # print(f'per_cpu={per_cpu}')
        for i in range(n_cpus):
            FileSystemConfig.register_node([i],
                    per_cpu, i)

    def calc_vll_mat(self, n_routers):

        weight_mat = []

        # true for both 20 and 30 router configs
        per_row = 5

        for i in range(n_routers):
            weight_mat.append([])
            for j in range(n_routers):

                i_row = i // per_row
                i_col = i % per_row

                j_row = j // per_row
                j_col = j % per_row

                delta_x = abs(i_col - j_col)
                delta_y = abs(i_row - j_row)

                dist = math.sqrt( delta_x*delta_x + delta_y*delta_y)

                # take upper val
                weight = math.ceil(dist)

                # init to 1
                weight_mat[i].append(weight)

        # print(f'weight_mat init to {weight_mat}')
        return weight_mat

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

        print(f'ingesting {path_name}')

        routing_alg = None
        flat_nr_map = []

        with open(path_name, 'r') as inf:
            routing_alg = inf.readline()

            for i in range(n_routers):
                # flat_nr_map.append([])
                a_routers_map = []
                for j in range(n_routers):
                    thisline = inf.readline()


                    as_list = ast.literal_eval(thisline)
                    clean_as_list = [e for e in as_list]

                    # print(f'\trouting table for router {i} '+
                    #     f' row (src) {j} : {clean_as_list}')
                    # flat_nr_map.append(clean_as_list)
                    a_routers_map += clean_as_list

                flat_nr_map.append(a_routers_map)


        # print(f'flat_nr_map({len(flat_nr_map)}) = {flat_nr_map}')
        # for alist in flat_nr_map:
        #     for row in alist:
        #         print(f'{row}')
        # quit(-1)

        return (flat_nr_map, routing_alg)
