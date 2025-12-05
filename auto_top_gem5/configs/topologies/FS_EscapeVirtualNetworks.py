from sys import int_info
from m5.params import *
from m5.objects import *

from common import FileSystemConfig

from topologies.BaseTopology import SimpleTopology

import math
import ast

class FS_EscapeVirtualNetworks(SimpleTopology):
    description='FS_EscapeVirtualNetworks'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):

        verbose = False

        nodes = self.nodes

        # cpu/mem organization
        n_cpus = options.num_cpus
        n_dirs = options.num_dirs
        n_noi_routers = options.noi_routers

        # clks
        noi_clk = options.noi_clk

        n_noi_rows = round(math.sqrt(n_noi_routers))

        per_row = n_noi_routers // n_noi_rows

        l1_caches = [n for n in nodes if n.type == 'L1Cache_Controller']
        l2_caches = [n for n in nodes if n.type == 'L2Cache_Controller']
        assert(len(l2_caches) == len(l1_caches))

        dirs = [n for n in nodes if n.type == 'Directory_Controller']
        dmas = [n for n in nodes if n.type == 'DMA_Controller']
        others = [n for n in nodes if n not in l1_caches and n not in l2_caches and n not in dirs and n not in dmas]

        print(f'l1_caches({len(l1_caches)})={l1_caches}\n')
        print(f'l2_caches({len(l2_caches)})={l2_caches}\n')
        print(f'dirs({len(dirs)})={dirs}\n')
        print(f'dmas({len(dmas)})={dmas}\n')
        print(f'others({len(others)})={others}\n')

        # obligatory required sets
        link_latency = options.link_latency
        router_latency = options.router_latency

        n_routers = n_noi_routers 

        ###############################################################

        flat_nr_map_path = options.flat_nr_map_file

        # this is 3d (20x20x20) or (84x84x84)
        (flat_nr_maps, routing_alg) = self.ingest_flat_map_list(flat_nr_map_path, n_routers)

        flat_vn_map_path = options.flat_vn_map_file

        # this is 2d (20x20) or (84x84)
        flat_vn_map = self.ingest_flat_map(flat_vn_map_path, n_routers)

        # CDC stuff
        noi_clk_domain = SrcClockDomain(clock = noi_clk, voltage_domain=\
                    VoltageDomain(voltage=options.sys_voltage) )


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

        for r in range(n_noi_routers):
            routers[r].clk_domain = noi_clk_domain

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
            # print(f'Adding external link: l1 cache node {i} <-> router {i} ')

            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= l1_caches[i],
                                    int_node= routers[i],
                                    latency=link_latency,
                                    ))
            link_count += 1

        # l2s -> noc routers
        for i in range(len(l2_caches)):
            # print(f'Adding external link: l1 cache node {i} <-> router {i} ')

            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= l2_caches[i],
                                    int_node= routers[i],
                                    latency=link_latency,
                                    ))
            link_count += 1

        # dmas -> noc routers
        # use a prime to spread dmas so that all routers used before repeating
        prime_mult = 7
        n_dma = len(dmas)
        for i in range(n_dma):
            idx = (i*prime_mult) % n_dma
            # print(f'Adding external link: dma node {i} <-> router {idx} ')

            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= dmas[i],
                                    int_node= routers[idx],
                                    latency=link_latency,
                                    ))
            link_count += 1


        # utilize per_row. alternate "left" and "right" sides
        edges = [ ]
        n_allocated = 0
        allocate_left = True
        while n_allocated < n_dirs:
            if allocate_left:
                edges.append( (n_allocated*per_row) % n_noi_routers )
            else:
                edges.append( (n_allocated*per_row - 1) % n_noi_routers )
            allocate_left = not allocate_left
            n_allocated += 1

        assert(len(edges) == n_dirs)

        for i in range(n_dirs):

            targ = edges[i]
            ext_links.append(ExtLink(link_id=link_count,
                                    ext_node= dirs[i],
                                    int_node= routers[targ],
                                    latency=link_latency))
            link_count += 1

            if verbose:
                print(f'Adding external link (id {link_count}): (memory) dir node {i} <-> noi router {targ}')



        ###############################################################
        # int links
        ###############################################################

        # routers -> routers
        # based on topology .map file
        map_file = options.router_map_file
        r_map = self.ingest_map(map_file, n_routers)

        n_int_links = 0

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


                    int_links.append(IntLink(link_id=link_count,
                                src_node=routers[src_r],
                                dst_node=routers[dest_r],
                                src_outport=s_name,
                                dst_inport=d_name,
                                latency = this_link_latency
                                ))

                    if verbose:
                        print(f'Adding  internal link (id {link_count}) {src_r}->{dest_r}')

                    # print(f'Adding internal link (id:{n_int_links}) {s_name} ({src_r})->{d_name} ({dest_r}) latency: {this_link_latency} and weight: {w}')
                    link_count += 1
                    n_int_links +=1


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

            for row in in_file:
                row = row.replace('\n','')
                r_conns = row.split(" ")
                if '' in r_conns:
                    r_conns.remove('')

                try:
                    r_conns = [int(elem) for elem in r_conns]
                except Exception as e:
                    print(f'e={e}')
                    r_conns = [int(float(elem)) for elem in r_conns]
                r_map.append(r_conns)

        assert(len(r_map) == n_routers)

        return r_map

    def ingest_flat_map(self, path_name, n_routers):
        print(f'ingesting {path_name}')

        r_map = []

        with open(path_name, 'r') as in_file:

            for row in in_file:

                row = row.replace('\n','')
                r_conns = row.split(" ")
                if '' in r_conns:
                    r_conns.remove('')

                try:
                    r_conns = [int(elem) for elem in r_conns]
                except Exception as e:
                    print(f'e={e}')
                    r_conns = [int(float(elem)) for elem in r_conns]

                r_map += r_conns


        return r_map

    def ingest_flat_map_list(self, path_name, n_routers):

        print(f'ingesting {path_name} w/ # rotuers = {n_routers}')
        # quit()

        routing_alg = None
        flat_nr_map = []
        nr_map_dict = {}

        iter_num = 0

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

                    iter_num += 1

                flat_nr_map.append(a_routers_map.copy())
                nr_map_dict.update({i : a_routers_map.copy()})

        new_flat = []
        for i, r_nrl in nr_map_dict.items():
            new_flat.append(r_nrl)

        return (new_flat, routing_alg)
