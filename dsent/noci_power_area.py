
# Copyright (c) 2014 Mark D. Hill and David A. Wood
# Copyright (c) 2024 Purdue University
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
# Modified by David Smelt for Garnet2.0
# Modified by Conor Green for NetSmith



from subprocess import call
import string, sys, subprocess, os, re


build_dir = 'ext/dsent'

rebuild = False

if rebuild:
    # Compile DSENT to generate the Python module and then import it.
    # This script assumes it is executed from the gem5 root.
    print("Attempting compilation")

    src_dir = './ext/dsent'
    build_dir = './build/ext/dsent'


    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    os.chdir(build_dir)

    print( '../../../%s' % src_dir)

    # called from build dir
    error = call(['cmake', '../../../%s' % src_dir])
    if error:
        print("Failed to run cmake")
        exit(-1)

    error = call(['make'])
    if error:
        print("Failed to run make")
        exit(-1)

    print("Compiled dsent")
    os.chdir("../../../")


sys.path.append(build_dir)
import dsent


# Begin python script


print("Usage: %s <simulation directory> " \
            "<router config file> <link config file>" % sys.argv[0])
print("If unspecified, <router config file> will default to " \
        "<simulation directory>/router.cfg and")
print("<link config file> will default to " \
        "<simulation directory>/electrical-link.cfg")

print("WARNING: configuration files for DSENT and McPAT are separate. " \
        "Changes made to one are not reflected in the other.")

from ConfigParser import ConfigParser
from collections import Counter
from math import sqrt
import math


VERBOSE = False



global is_mesh
is_mesh = False

########################################################################
# 24 x 36 mm active interposer
# 2mm core to core minimal distance
# 0.2 um microbump overhead
########################################################################


def calc_dist(x_d, y_d):

    d = (x_d**2) + (y_d**2)
    return sqrt(d)

########################################################################################################

def is_noi_r(r):

    if is_mesh and r < 64:
        return True
    elif r < 20:
        return True
    
    return False

## Compute the power and area used for all routers and the CPU die area
def computeRouterPowerAndArea(routers, stats_file, config, router_config_file,
                              int_links, ext_links, num_cycles, num_cpus):
    results = []
    num_keys = 15
    sum_strings = [""] * num_keys
    avg_strings = [""] * num_keys

    total_router_dynamic = 0
    total_router_leakage = 0
    total_router_area  = 0

    for router in routers:

        frequency = getClock(router, config)

        # Count number of ports to int_links for this router
        int_nports = 0
        router_is_noc = False
        for int_link in int_links:

            # int_links are defined unidirectionally
            if config.get(int_link, "src_node") == router:
                int_nports += 1


                # found this source
                s, d = parse_src_dest_from_link(int_link, config)

                if not is_noi_r(s):
                    router_is_noc = True

            if config.get(int_link, "dst_node") == router:
                int_nports += 1


        if router_is_noc:
            continue

        # Count number of ports to ext_links for this router
        ext_nports = 0
        for ext_link in ext_links:
            if config.get(ext_link, "int_node") == router:

                # ext_links are defined bidirectionally
                ext_nports += 2
        if ext_nports == 0:
            ext_nports = 1

        # All ports are bidirectional
        nports = int_nports + ext_nports

        # Set port amounts in router config file
        setConfigParameter(router_config_file, "NumberInputPorts", int_nports)
        setConfigParameter(router_config_file, "NumberOutputPorts", ext_nports)

        buf_activity_rd = getStatsForString(stats_file, router + ".buffer_reads")
        buf_activity_wr = getStatsForString(stats_file, router + ".buffer_writes")
        xbar_activity   = getStatsForString(stats_file, router + ".crossbar_activity")
        sw_activity_in  = getStatsForString(stats_file, router + ".sw_input_arbiter_activity")
        sw_activity_out = getStatsForString(stats_file, router + ".sw_output_arbiter_activity")

        # Calculate injection (number of flits per cycle per port)
        # for this router, based on stats
        if VERBOSE:
            print('numcycles')
            print(num_cycles)
            print('int_nports')
            print(int_nports)
            print('ext_nports')
            print(ext_nports)

            print('buf_activity_rd = {}, buf_activity_wr={}, xbar_activity={}, sw_activity_out={}'.format(buf_activity_rd,buf_activity_wr,xbar_activity, sw_activity_out))

        buf_rd_injrate  = ext_nports * buf_activity_rd / float(num_cycles) / int_nports
        buf_wr_injrate  = ext_nports * buf_activity_wr / float(num_cycles) / int_nports
        xbar_injrate    = ext_nports * xbar_activity / float(num_cycles) / int_nports
        sa_injrate      = ext_nports * sw_activity_out / float(num_cycles) / int_nports

        # Set injection rates in router config file
        setConfigParameter(router_config_file, "BufRdInjectionRate", buf_rd_injrate)
        setConfigParameter(router_config_file, "BufWrInjectionRate", buf_wr_injrate)
        setConfigParameter(router_config_file, "XbarInjectionRate", xbar_injrate)
        setConfigParameter(router_config_file, "SAInjectionRate", sa_injrate)

        # Initialize DSENT with router config file
        dsent.initialize(router_config_file)

        if VERBOSE:
            print('relevant router results')
            # Print results, overwriting relevant parameters, for this router
            print("\n%s:" % router)

        # Run DSENT
        dsent_out = dsent.computeRouterPowerAndArea(frequency)
        dsent_out_dict = dict(dsent_out)

        if VERBOSE:
            print('dsent_out_dict={}'.format(dsent_out_dict))

        # rename keys
        rename_dict = {}


        # populate total area key
        area_subsections = ['Buffer', 'Crossbar','SwitchAllocator','Other']
        total_area = 0.0
        for term in area_subsections:
            key = 'Area:' + term
            total_area += dsent_out_dict[key]

        total_router_area += total_area

        dsent_out_dict.update({'Area:Total':total_area})

        results.append(dsent_out_dict)

        # Finalize DSENT
        dsent.finalize()

    # Calculate sum for all routers
    result_sum = Counter()
    for d in results:
        result_sum.update(d)
    result_sum = dict(result_sum)

    # Calculate maximum total router area
    max_router_area = 0.0

    for d in results:
        #print('d')
        #print(d)
        for k, v in d.iteritems():
            #print('k/v')
            #print(k)
            #print(v)
            if "Area:Total" in k:
                #print('area in k pringing v')
                #print(v)
                if v > max_router_area:
                    max_router_area = v

    if VERBOSE:
        print('max_router_area')
        print(max_router_area)
    assert(max_router_area > 0.0)

    nrows = config.getint("system.ruby.network", "num_rows")

    # just hardcode
    nrows = 4
    concentration_factor = 4
    num_cpus = 64
    if config.has_option("system.ruby.network", "concentration_factor"):
        concentration_factor = config.getint("system.ruby.network",
                                             "concentration_factor")



    ncols = num_cpus / nrows / concentration_factor
    assert(nrows > 0 and ncols > 0)

    num_vertical_cpus = nrows
    num_horizontal_cpus = ncols
    if concentration_factor > 1:
        # For concentrated meshes, 2 CPUs per router are placed along the y-axis
        num_vertical_cpus = num_cpus / (concentration_factor * 2)
        num_horizontal_cpus = num_cpus / num_vertical_cpus


    # Assume size of a single core based on limited models
    # (core_area, model_name, model_die_size, model_core_size) = getCoreAreaForCoreCount(num_cpus)

    model_name =  "14nm 76-core (XCC) Knights Landing"



    # hardcode for 2.2x2.2mm^2 cores
    model_core_size = 2.2*2.2

    # hardcode for 24x36mm^2 interposer
    model_die_size = 24*36

    # 16 cpu per core
    core_area = (model_die_size / 1e6) / 16.0

    if VERBOSE:
        print('corearea')
        print(core_area)
        print('model die size')
        print(model_die_size)
        print('model core size')
        print(model_core_size)
    # quit()


    # Cache and directory controllers are assumed to be located at a 45 degree
    # angle from the router at a distance of 0.1 * sqrt(core_area)
    # => set external link wire length to:
    ext_wire_length = 0.1 * sqrt(core_area)

    die_area = 0.0
    int_wire_length = 0.0

    # Calculate NoC area;
    # The lateral space between a router and a CPU is ext_wire_length / sqrt(2)
    die_area_x = nrows * (ext_wire_length / sqrt(2) + sqrt(max_router_area))\
                 + num_vertical_cpus * sqrt(core_area)
    die_area_y = ncols * (ext_wire_length / sqrt(2) + sqrt(max_router_area))\
                 + num_horizontal_cpus * sqrt(core_area)
    die_area = die_area_x * die_area_y

    # Calculate internal link wire length
    # For odd-dimensional topologies, take the largest dimension
    int_wire_length = max(die_area_y, die_area_x) / (max(num_vertical_cpus,
                          num_horizontal_cpus) - 1.0)

    assert(die_area > 0.0 and int_wire_length > 0.0)

    # Generate output strings in the correct order
    for k, v in result_sum.iteritems():
        sum_strings[getResultKey(k)] = str(k) + str(v)

    # Print sum totals and CPU die area
    print("\nSum totals for all %d routers:" % len(routers))
    print("\n".join(sum_strings))

    print("\nDie area model scaled in proportion to a {0}:".format(model_name))
    print("\twhich amounts to:")
    print("\t\tDie area: {0:f} mm^2".format(model_die_size))
    print("\t\tApproximated core area: {0:f} mm^2".format(model_core_size))
    print("\n\tScaled core area of one CPU: {0:f} mm^2".format(core_area * 1e6))
    print("\tTotal core area excluding uncore and NoC: {0:f} mm^2".format(\
        num_cpus * core_area * 1e6))
    print("\tTotal CPU die area: {0:f} mm^2".format(die_area * 1e6))

    # input('good?')

    # Calculate sum power for all routers + links
    router_dynamic = 0.0
    router_leakage = 0.0
    for k, v in result_sum.iteritems():
        if "Dynamic" in k:
            router_dynamic += v
        elif "Leakage" in k:
            router_leakage += v

    print("\nSum power for all routers:")
    print("    Dynamic power: %f" % (router_dynamic))
    print("    Leakage power: %f" % (router_leakage))
    print("\nSum area for all routers:")
    print("    Area: %f" % (total_router_area))

    return (router_dynamic, router_leakage, total_router_area)
    # return (result_sum, int_wire_length, ext_wire_length)

########################################################################################################

## Compute the power consumed by the given ext_links
def computeExtLinkPower(num_cycles, ext_wire_length, wire_delay_scale, ext_links, stats_file,config, link_config_file, num_links=1e9):
    results = []
    single_link_utilization = getStatsForString(stats_file, "system.ruby.network.ext_in_link_utilization")
    single_link_utilization += getStatsForString(stats_file, "system.ruby.network.ext_out_link_utilization")
    injrate = single_link_utilization / float(num_cycles) / (len(ext_links) * 2)

    assert(injrate > 0.0)

    i = 1
    for link in ext_links:
        if i > num_links:
            break

        frequency = getClock(link + ".network_links0", config)
        delay = config.getint(link, "latency")

        # Calculate wire delay. wire_length is in meters and wire_delay_scale is in ns/mm
        # => multiply their product by 1e-6 to get the delay in seconds
        wire_delay = ext_wire_length * wire_delay_scale * 1e-6

        # Set injection rate, and wire length and wire delay in link config file
        setConfigParameter(link_config_file, "InjectionRate", injrate)
        setConfigParameter(link_config_file, "WireLength", ext_wire_length)
        setConfigParameter(link_config_file, "Delay", wire_delay)

        dsent.initialize(link_config_file)

        if VERBOSE:
            if num_links == 1:
                print("\nSingle ext_link power:")
            else:
                print("\n%s.network_links0 power: " % link)

        dsent_out = dsent.computeLinkPower(frequency)
        results.append(dict(dsent_out))

        if VERBOSE:
            print("%s.network_links0 wire length: %f mm" % (link, ext_wire_length * 1000))

        dsent.finalize()
        dsent.initialize(link_config_file)

        i += 1
        if i > num_links:
            break

        frequency = getClock(link + ".network_links1", config)
        

        dsent_out = dsent.computeLinkPower(frequency)
        results.append(dict(dsent_out))

        if VERBOSE:
            print("\n%s.network_links1 power: " % link)
            print("%s.network_links1 wire length: %f mm" % (link, ext_wire_length * 1000))

        dsent.finalize()
        i += 1

    return results

## Compute the power consumed by the given int_links
def computeNoCNoIIntLinkPowerAndArea(num_cycles, phys_dist_dict, wire_delay_scale, int_links, stats_file,config, link_config_file):
    
    # print('compute int link got args\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format(num_cycles, phys_dist_dict, wire_delay_scale, int_links, stats_file,config, link_config_file))

    results = []
    injrate = getStatsForString(stats_file, "system.ruby.network.int_link_utilization")\
                                / float(num_cycles) / len(int_links)

    assert(injrate > 0.0)


    total_area = 0


    for (i, link) in enumerate(int_links):


        int_wire_length = .1/(1e3)

        # .1mm
        int_wire_width = .00005
        int_wire_area = int_wire_length*int_wire_width
        total_area += int_wire_area

        frequency = getClock(link + ".network_link", config)

        # Multiply wire length by 'latency' for FlattenedButterfly, which is
        # set to the factored distance between routers
        router_distance = config.getint(link, "latency")
        wire_length = router_distance * int_wire_length

        # Calculate wire delay. wire_length is in meters and wire_delay_scale is in ns/mm
        # => multiply their product by 1e-6 to get the delay in seconds
        wire_delay = wire_length * wire_delay_scale * 1e-6

        # Set injection rate, and wire length and wire delay in link config file
        setConfigParameter(link_config_file, "InjectionRate", injrate)
        setConfigParameter(link_config_file, "WireLength", wire_length)
        setConfigParameter(link_config_file, "Delay", wire_delay)


        # Calculate and set delay in link config file
        dsent.initialize(link_config_file)

        # print("\n%s.network_link power: " % link)

        dsent_out = dsent.computeLinkPower(frequency)
        results.append(dict(dsent_out))

        # print("%s.network_link wire length: %f mm" % (link, wire_length * 1000))

        dsent.finalize()

    return results, total_area

## Compute the power consumed by the given int_links
def computeNoINoIIntLinkPowerAndArea(num_cycles, phys_dist_dict, wire_delay_scale, int_links, stats_file,config, link_config_file):
    
    # print('compute int link got args\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format(num_cycles, phys_dist_dict, wire_delay_scale, int_links, stats_file,config, link_config_file))

    results = []
    injrate = getStatsForString(stats_file, "system.ruby.network.int_link_utilization")\
                                / float(num_cycles) / len(int_links)

    assert(injrate > 0.0)

    # hardcoded for 20r interposer
    n_cols = 5
    n_rows = 4
    x_base_dist = phys_dist_dict['noi']['x']
    y_base_dist = phys_dist_dict['noi']['y']

    total_area = 0

    for (i, link) in enumerate(int_links):

        # for noc->noc
        s, d = parse_src_dest_from_link(link, config)

        s_col = s % n_cols
        s_row = s % n_rows

        d_col = d % n_cols
        d_row = d % n_rows

        x_hops = abs(d_col - s_col)
        y_hops = abs(d_row - s_row)

        
        x_dist = x_hops*x_base_dist
        y_dist = y_hops*y_base_dist

        int_wire_length = calc_dist(x_dist, y_dist) / (1e3)

        # .1mm
        int_wire_width = .0001
        int_wire_area = int_wire_length*int_wire_width
        total_area += int_wire_area

        frequency = getClock(link + ".network_link", config)

        # Multiply wire length by 'latency' for FlattenedButterfly, which is
        # set to the factored distance between routers
        router_distance = config.getint(link, "latency")
        wire_length = router_distance * int_wire_length

        # Calculate wire delay. wire_length is in meters and wire_delay_scale is in ns/mm
        # => multiply their product by 1e-6 to get the delay in seconds
        wire_delay = wire_length * wire_delay_scale * 1e-6

        # Set injection rate, and wire length and wire delay in link config file
        setConfigParameter(link_config_file, "InjectionRate", injrate)
        setConfigParameter(link_config_file, "WireLength", wire_length)
        setConfigParameter(link_config_file, "Delay", wire_delay)


        # Calculate and set delay in link config file
        dsent.initialize(link_config_file)

        # print("\n%s.network_link power: " % link)

        dsent_out = dsent.computeLinkPower(frequency)
        results.append(dict(dsent_out))

        # print("%s.network_link wire length: %f mm" % (link, wire_length * 1000))

        dsent.finalize()

    return results, total_area

## Compute the power consumed by the given int_links
def computeNoCNoCIntLinkPowerAndArea(num_cycles, phys_dist_dict, wire_delay_scale, int_links, stats_file,config, link_config_file):
    
    # print('compute int link got args\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}'.format(num_cycles, phys_dist_dict, wire_delay_scale, int_links, stats_file,config, link_config_file))

    results = []
    injrate = getStatsForString(stats_file, "system.ruby.network.int_link_utilization")\
                                / float(num_cycles) / len(int_links)

    assert(injrate > 0.0)

    n_cols = 8
    n_rows = 8
    x_base_dist = phys_dist_dict['noc']['x']
    y_base_dist = phys_dist_dict['noc']['y']

    total_area = 0

    for (i, link) in enumerate(int_links):

        # for noc->noc
        s, d = parse_src_dest_from_link(link, config)

        s_col = s % n_cols
        s_row = s % n_rows

        d_col = d % n_cols
        d_row = d % n_rows

        x_hops = abs(d_col - s_col)
        y_hops = abs(d_row - s_row)

        
        x_dist = x_hops*x_base_dist
        y_dist = y_hops*y_base_dist

        int_wire_length = calc_dist(x_dist, y_dist) / (1e3)

        # .1mm
        int_wire_width = .0001
        int_wire_area = int_wire_length*int_wire_width
        total_area += int_wire_area

        # print('NoCNoC int_wire_length = {}m'.format(int_wire_length))
        # quit()

        frequency = getClock(link + ".network_link", config)

        # Multiply wire length by 'latency' for FlattenedButterfly, which is
        # set to the factored distance between routers
        router_distance = config.getint(link, "latency")
        wire_length = router_distance * int_wire_length

        # Calculate wire delay. wire_length is in meters and wire_delay_scale is in ns/mm
        # => multiply their product by 1e-6 to get the delay in seconds
        wire_delay = wire_length * wire_delay_scale * 1e-6

        # Set injection rate, and wire length and wire delay in link config file
        setConfigParameter(link_config_file, "InjectionRate", injrate)
        setConfigParameter(link_config_file, "WireLength", wire_length)
        setConfigParameter(link_config_file, "Delay", wire_delay)


        # Calculate and set delay in link config file
        dsent.initialize(link_config_file)

        # print("\n%s.network_link power: " % link)

        dsent_out = dsent.computeLinkPower(frequency)
        results.append(dict(dsent_out))

        # print("%s.network_link wire length: %f mm" % (link, wire_length * 1000))

        dsent.finalize()

    return results, total_area


def computeLinkPowerAndArea(num_cycles, num_cpus, n_routers,
                              int_links, ext_links,
                              stats_file, config, link_config_file):
    # my sets
    ext_wire_length = 2.0
    noc_noi_wire_length = 0.2

    phys_dist_dict = {'noc': {'x':2.25,'y':1.5}, 'noi':{'x':4.5,'y':3}}

    # given sets
    # Set wire delay factor according to ITRS projections
    wire_delay_proj = "ITRS projected estimated wire delay for 14 nm CMOS: 1.0 ns/mm"
    wire_delay_scale = 1.0

    print("\nUsing " + wire_delay_proj)


    int_num_links = len(int_links)
    ext_num_links = len(ext_links) * 2
    total_num_links = int_num_links + ext_num_links

    print("\nTotal number of links: %d" % total_num_links)
    print("                       %d bidirectional int_links" % (int_num_links / 2))
    print("                       %d bidirectional ext_links" % (ext_num_links / 2))

    ###########################################################################
    # int links


    nocnoc_links, noinoi_links, nocnoi_links = split_int_links(int_links, config)

    # nocnoc_links = nocnoc_links[:1]
    # noinoi_links = noinoi_links[:1]
    # nocnoi_links = nocnoi_links[:1]

    # print('From int_links: {}'.format(int_links))
    # print('Read...\n\tnocnoc {}\n\tnoinoi {}\n\tnocnoi {}'.format(nocnoc_links, noinoi_links, nocnoi_links))

    ###################################
    # noc -> noc

    # noc_noc_dsent_out, noc_noc_area = computeNoCNoCIntLinkPowerAndArea(num_cycles, phys_dist_dict, wire_delay_scale,
    #                                     nocnoc_links, stats_file, config,
    #                                     link_config_file)

    # print('noc_noc_dsent_out={}'.format(noc_noc_dsent_out))


    # # noc -> noi
    # noc_noi_dsent_out, noc_noi_area = computeNoCNoIIntLinkPowerAndArea(num_cycles, phys_dist_dict, wire_delay_scale,
    #                                     nocnoi_links, stats_file, config,
    #                                     link_config_file)

    # print('noc_noi_dsent_out={}'.format(noc_noi_dsent_out))

    # noi -> noi
    noi_noi_dsent_out, noi_noi_area = computeNoINoIIntLinkPowerAndArea(num_cycles, phys_dist_dict, wire_delay_scale,
                                        noinoi_links, stats_file, config,
                                        link_config_file)          


    if VERBOSE:

        print('noi_noi_dsent_out={}'.format(noi_noi_dsent_out))

    int_dynamic = 0.0
    int_leakage = 0.0
    int_area = 0.0

    # int_area += noc_noc_area
    # int_area += noc_noi_area
    int_area += noi_noi_area

    total_area = int_area


    # Calculate total int_link power consumption
    int_sum = Counter()
    # for d in int_dsent_out:
    #     int_sum.update(d)

    # for d in noc_noc_dsent_out:
    #     int_sum.update(d)
    # for d in noc_noi_dsent_out:
    #     int_sum.update(d)
    for d in noi_noi_dsent_out:
        int_sum.update(d)
    int_sum = dict(int_sum)

    # Get dynamic and leakage total power consumptions
    for k, v in int_sum.iteritems():
        if "Dynamic" in k:
            int_dynamic = v
        elif "Leakage" in k:
            int_leakage = v

    print("\nTotal power for all int_links:")
    print("    Dynamic power: %f" % int_dynamic)
    print("    Leakage power: %f" % int_leakage)

    ###########################################################################
    # ext links

    # def computeExtLinkPower(num_cycles, ext_wire_length, wire_delay_scale, ext_links, stats_file,config, link_config_file, num_links=1e9):
    # Compute the power consumed by for each ext_link
    ext_wire_length = .001


    # ext_dsent_out = computeExtLinkPower(num_cycles, ext_wire_length, wire_delay_scale,
    #                                     ext_links, stats_file, config,
    #                                     link_config_file)



    ext_dynamic = 0.0
    ext_leakage = 0.0

    # # Calculate total ext_link power consumption
    # ext_sum = Counter()
    # for d in ext_dsent_out:
    #     ext_sum.update(d)
    # ext_sum = dict(ext_sum)

    # for k, v in ext_sum.iteritems():
    #     if "Dynamic" in k:
    #         ext_dynamic = v
    #     elif "Leakage" in k:
    #         ext_leakage = v

    print("\nTotal power for all ext_links:")
    print("    Dynamic power: %f" % ext_dynamic)
    print("    Leakage power: %f" % ext_leakage)

    total_dynamic = int_dynamic + ext_dynamic
    total_leakage = int_leakage + ext_leakage
    print("\nTotal power for all links:")
    print("    Dynamic power: %f" % total_dynamic)
    print("    Leakage power: %f" % total_leakage)


    # expects this in return

    # Compute total link power consumption
    # (link_dynamic, link_leakage) 
    return (total_dynamic, total_leakage, total_area)

########################################################################################################

def parse_src_dest_from_link(link, config):
    outport = config.get(link, "src_outport")
    ops = outport.split('_')
    src_str = ops[0]
    dest_str = ops[-1]

    src = int(src_str.replace('src',''))
    dest = int(dest_str.replace('dest',''))
    
    return src, dest

def split_int_links(int_links, config):

    global is_mesh

    n_noi = 20

    if is_mesh:
        n_noi = 64

    noinoi_links = []
    nocnoc_links = []
    nocnoi_links = []

    for link in int_links:
        src, dest = parse_src_dest_from_link(link, config)

        # print('outpoty {} implies src {} dest {}'.format(outport, src, dest))

        if src >= n_noi and dest >= n_noi:
            nocnoc_links.append(link)
        elif src < n_noi and dest < n_noi:
            noinoi_links.append(link)
        else:
            nocnoi_links.append(link)


    # print('\tnocnoc ({}) {}\n\n\tnoinoi ({}) {}\n\n\tnocnoi ({}) {}'.format(len(nocnoc_links), nocnoc_links, len(noinoi_links) ,noinoi_links, len(nocnoi_links), nocnoi_links))

    return nocnoc_links, noinoi_links, nocnoi_links

########################################################################################################

# BIG DRIVER
## Parse gem5 stats.txt file
def parseStats(stats_file, config, router_config_file, link_config_file,
               routers, int_links, ext_links, num_cpus):

    global is_mesh

    if 'mesh' in stats_file:
        is_mesh = True

    print('Will read stats from {} (is mesh? {})'.format(stats_file, is_mesh))

    # Get number of cycles for SE/FE simulation
    num_cycles = getStatsForString(stats_file, "system.switch_cpus0.numCycles")
    if num_cycles == 0.0:
        num_cycles = getStatsForString(stats_file, "system.switch_cpus00.numCycles")
    if num_cycles == 0.0:
        num_cycles = getStatsForString(stats_file, "system.switch_cpus000.numCycles")
    if num_cycles == 0.0:
        num_cycles = getStatsForString(stats_file, "system.switch_cpus000.numCycles")

    # Get number of cycles for Garnet_standalone simulation
    if num_cycles == 0.0:
        num_cycles = getStatsForString(stats_file, "sim_ticks")

    print('Read numCycles = {} '.format(num_cycles))

    # quit()

    # Compute the power and area used by the routers
    (router_dynamic, router_leakage, router_area) = \
        computeRouterPowerAndArea(routers, stats_file, config, router_config_file,
                                    int_links, ext_links, num_cycles, num_cpus)

    # Compute total link power consumption
    (link_dynamic, link_leakage, link_area) = \
        computeLinkPowerAndArea(num_cycles, num_cpus, len(routers),
                              int_links, ext_links,
                              stats_file, config, link_config_file)


    total_dynamic = router_dynamic + link_dynamic
    total_leakage = router_leakage + link_leakage
    total_area = router_area

    print("\nArea for all routers + links:")
    print("    Router area:             %f" % (router_area))
    print("    Link area:               %f" % (link_area))
    print("    Total area:              %f" % (total_area))

    print("\nPower for all routers + links:")
    print("    Total dynamic power:     %f" % (total_dynamic))
    print("    Total leakage power:     %f" % (total_leakage))
    print("    Router dynamic power:    %f" % (router_dynamic))
    print("    Router leakage power:    %f" % (router_leakage))
    print("    Link dynamic power:      %f" % (link_dynamic))
    print("    Link leakage power:      %f" % (link_leakage))


    out_name_base = 'dsent_stats'

    topo = 'mesh'

    split_stats = stats_file.split('/')
    topo_section = split_stats[2]
    topo_split = topo_section.split('_')

    if 'ns' in stats_file or 'lpbt' in stats_file:
        topo = '_'.join( topo_split[:3])
    if 'butter' in stats_file or 'dbl' in stats_file:
        topo = '_'.join(topo_split[:3])
    if 'kite' in stats_file or 'ft_x' in stats_file:
        topo = '_'.join(topo_split[:2])
    if 'mesh' in stats_file:
        topo = 'mesh'

    write_out_power_area(out_name_base, topo, total_dynamic, total_leakage, router_area, link_area)

def write_out_power_area(base_name, topo, total_dynamic, total_leakage, router_area, link_area):

    out_path = './dsent_results/{}.csv'.format(base_name)

    oline = [topo, total_dynamic, total_leakage, router_area, link_area]

    oline_strs = [str(e)+',' for e in oline]

    oline_strs.append('\n')

    with open(out_path, 'a+') as of:
        of.writelines(oline_strs)

    print('wrote {}'.format(oline))
    print('Wrote out to {}'.format(out_path))

########################################################################
# Given helpers
########################################################################


## Return the key index of known result strings to order known result strings
## for more intuitive printing
def getResultKey(s):
    key_order = ["Buffer/Dynamic", "Buffer/Leakage", "Crossbar/Dynamic",
                 "Crossbar/Leakage", "Switch allocator/Dynamic",
                 "Switch allocator/Leakage", "Clock/Dynamic",
                 "Clock/Leakage", "Total/Dynamic", "Total/Leakage",
                 "Area/Buffer", "Area/Crossbar", "Area/Switch allocator",
                 "Area/Other", "Area/Total"]
    for (i, key) in enumerate(key_order):
        if key in s:
            return i
    return -1

## Overwrite a parameter in router/link config file
def setConfigParameter(config_file, string, new_val):
    try:
        new_string = string + (" " * max(1, 40 - len(string)))
        new_string += "= {0}".format(new_val)
        command = ["sed", "-i", "s/{0}.*=.*/{1}/".format(string, new_string),
                   config_file]

        proc = subprocess.Popen(command)
        proc.communicate()
    except OSError:
        pass

# Parse gem5 config.ini file for the configuration parameters related to
# the on-chip network.
def parseConfig(config_file):
    config = ConfigParser()
    if not config.read(config_file):
        print("ERROR: config file '", config_file, "' not found")
        sys.exit(1)

    if not config.has_section("system.ruby.network"):
        print("ERROR: Ruby network not found in ", config_file)
        sys.exit(1)

    if config.get("system.ruby.network", "type") != "GarnetNetwork" :
        print("ERROR: Garnet network not used in ", config_file)
        sys.exit(1)

    number_of_virtual_networks = config.getint("system.ruby.network",
                                               "number_of_virtual_networks")
    vcs_per_vnet = config.getint("system.ruby.network", "vcs_per_vnet")

    buffers_per_data_vc = config.getint("system.ruby.network",
                                        "buffers_per_data_vc")
    buffers_per_control_vc = config.getint("system.ruby.network",
                                           "buffers_per_ctrl_vc")

    ni_flit_size_bits = 8 * config.getint("system.ruby.network",
                                          "ni_flit_size")

    # Count number of CPUs
    num_cpus = 0
    children = config.get("system", "children")
    num_cpus = len(re.findall("cpu[0-9]+[0-9]*", children))
    assert(num_cpus > 0)

    routers = config.get("system.ruby.network", "routers").split()
    int_links = config.get("system.ruby.network", "int_links").split()
    ext_links = config.get("system.ruby.network", "ext_links").split()

    return (config, number_of_virtual_networks, vcs_per_vnet,
            buffers_per_data_vc, buffers_per_control_vc, ni_flit_size_bits,
            num_cpus, routers, int_links, ext_links)

## For the given object return clock as int 
def getClock(obj, config):
    if config.get(obj, "type") == "SrcClockDomain":
        clock = config.getint(obj, "clock")
        if clock > 10:
            # Clock defined in to num_ticks (=1e12) / frequency
            return int((1000.0 / config.getint(obj, "clock")) * 1e9)
        # Clock defined in GHz
        return int(config.getint(obj, "clock") * 1e9)

    if config.get(obj, "type") == "DerivedClockDomain":
        source = config.get(obj, "clk_domain")
        divider = config.getint(obj, "clk_divider")
        return getClock(source, config)  / divider

    source = config.get(obj, "clk_domain")
    return getClock(source, config)

## Parse stats.txt for the specified key and return the associated value as float
def getStatsForString(stats_file, key):
    which = 0
    desired_which = 2
    with open(stats_file, "rt") as f:
        for line in f:
            if 'Begin' in line:
                which += 1

            if which < desired_which:
                continue
            
            if key in line:
                # Remove comments
                comment_pos = line.find("#")
                if comment_pos > -1:
                    line = line[0:comment_pos]

                # Return last column as float
                split = line.split()
                try:
                    return float(split[-1])
                except:
                    return float(split[-2])
    return 0.0

# This script parses the config.ini and the stats.txt from a run and
# generates the power and the area of the on-chip network using DSENT
def main():
    if len(sys.argv) < 2:
        print("Usage: %s <simulation directory> " \
              "<router config file> <link config file>" % sys.argv[0])
        print("If unspecified, <router config file> will default to " \
              "<simulation directory>/router.cfg and")
        print("<link config file> will default to " \
              "<simulation directory>/electrical-link.cfg")
        exit(2)

    print("WARNING: configuration files for DSENT and McPAT are separate. " \
          "Changes made to one are not reflected in the other.")

    cfg_str = os.path.join(sys.argv[1], "config.ini")
    stats_str = os.path.join(sys.argv[1], "stats.txt")

    (config, number_of_virtual_networks, vcs_per_vnet, buffers_per_data_vc,
     buffers_per_control_vc, ni_flit_size_bits, num_cpus,
     routers, int_links, ext_links) = parseConfig(cfg_str)

    router_cfg = os.path.join(sys.argv[1], "router.cfg")
    link_cfg = os.path.join(sys.argv[1], "electrical-link.cfg")

    if len(sys.argv) > 2:
        router_cfg = sys.argv[2]
    if len(sys.argv) > 3:
        link_cfg = sys.argv[3]

    parseStats(stats_str, config, router_cfg, link_cfg, routers, int_links,
               ext_links, num_cpus)

if __name__ == "__main__":
    main()
