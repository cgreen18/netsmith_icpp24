#!/usr/bin/python3

import os
import csv
import sys

import math

metrics = [
    # 'simSeconds',
        'simTicks',
            'numCycles',
            'simInsts',
            'average_packet_latency',
            # 'average_flit_latency',

            # 'packets_received::total',
            # 'packets_injected::total',
            # 'hops',
            'cumulativeCycles',
            'maxCycles',
            'geoIPC',
            'mpki'
            # 'avg_link_utilization'
           ]

print(f'metrics =\n{metrics}')

desired_which = 2

def parse_block( block):

    if len(block) == 0:
        return []

    avg_flit_lat = 0

    cumCycles = 0
    specificCycles = -1
    geoIPC = 1
    nGeoIPC = 0

    l2_misses = 0
    totInsts = 0

    data_dict = {}

    for met in metrics:
        data_dict.update({met : -1.0})

    which_cpu = 'null'

    which = 0
    for line in block:

        if 'Begin' in line:
            which += 1

        if which < desired_which:
            continue


        # if 'switch_cpu' not in line:
        #     continue

        sep = line.split()
        if len(sep) < 2:
            continue
        data = sep[1]
        for met in metrics:
            if met in line:
                if float(data) != 0:
                    data_dict.update({ met : float(data)})

        if 'numInsts' in line:
            thisInsts = float(data)

            if thisInsts >= 10000000:

                which_cpu = sep[0]
                which_cpu = which_cpu.split('.')[1]

                # print(f'found cpu {which_cpu} that reached max')


        if 'numCycles' in line:
            thisCycles = float(data)
            if thisCycles > specificCycles:
                specificCycles = float(data)
                # print(f'tracking specificCycles = {data} for cpu {which_cpu}')
                which_cpu = 'null'
        if 'numCycles' in line:
            cumCycles += float(data)
            # if 'cpu0' in line:
            #     if met in line:
            #         if float(data) != 0:
            #             data_dict.update({ met : float(data)})
            # if 'packet' in line:
            #     if met in line:
            #         if float(data) != 0:
            #             data_dict.update({ met : float(data)})
        if 'L2cache.m_demand_misses' in line:
            l2_misses += float(data)


        if 'numInsts' in line:
            totInsts += float(data)

        if 'ipc' in line:
            geoIPC *= float(data)
            nGeoIPC += 1

    try:
        geoIPC = math.pow(geoIPC, 1/ nGeoIPC)
    except:
        geoIPC = 0

    # print(f'after parsing block, geoIPC={geoIPC}')

    data_dict.update({'cumulativeCycles' : cumCycles})
    data_dict.update({'maxCycles' : specificCycles})
    data_dict.update({'geoIPC' : geoIPC})

    try:
        mpki = 1000*l2_misses / totInsts
    except:
        mpki = 0
    data_dict.update({'mpki' : mpki})

    l = []
    for met in metrics:
        l.append(data_dict[met])

    # l.append(cumCycles)
    # try:
    #     l.append(specificCycles)
    # except:
    #     l.append(-1)

    return l

if (len(sys.argv) < 3):
    print(f'not enough args')
    print(f'<python> <script> <input_dir> <output_file_name>')
    quit()

output_name = sys.argv[2]

output_file = open(output_name,'w+')

csv_lines = []
csv_lines.append([ 'bench','config','description'])

for met in metrics:
    csv_lines[-1].append(met)

data_dir = str(sys.argv[1])

which = 0

for root, dirs, files, in os.walk(data_dir):
    # print(f'root={root}, dirs={dirs}, files={files}')

    if 'stats.txt' in files:
        cur_path = os.path.join(root, 'stats.txt')

        # if 'OoO' not in cur_path:
        #     continue

        #if 'size2048' not in cur_path and 'baseline' not in cur_path and 'assoc512' not in cur_path and 'assoc1024' not in cur_path:
        #    continue

        root_split = root.split('/')

        cur_file = open(cur_path)
        lines = cur_file.readlines()

        if 'cmesh' in root:
            pass
            #continue

        if 'bsorm' not in root:
            pass
            #continue




        # sim_cycles = root_split[1]
        # mixed_domain_or_same = root_split[2]
        # mem_or_coh = root_split[3]
        # config = root_split[4]
        # inj_rate = root_split[5]


        # print(f'{root_split}')

        bench = root_split[3]
        config = root_split[4]

        extra = ''
        try:
            extra = root_split[5]
        except:
            pass

        if 'yara' in root:
            bench = root_split[8]
            config = root_split[9]
            try:
                extra = root_split[10]
            except:
                pass


        data = [ bench,config, extra]


        block = parse_block( lines)


        data += block

        # if len(data) >= 4:
            # print(f'data = {data}')
        print(f'data = {data}')

        if data != []:
            csv_lines.append(data)


wr = csv.writer(output_file, delimiter=',')
wr.writerows(csv_lines)

output_file.close()
