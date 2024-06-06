import matplotlib.pyplot as plt
import csv
import numpy as np
import sys

from matplotlib import rc


# infile_name = 'paper_outputs/parsec_noci_250kBL2_10m.csv'
infile_name = 'paper_outputs/parsec_noci_500kBL2_10m.csv'
# infile_name = 'paper_outputs/parsec_noci_largemem_3GHzCPU.csv'
# infile_name = 'paper_outputs/parsec_noci_largemem_20m.csv'
infile_name = 'parsec_results/parsec_noci_largemem_18GHz_500kB_100m.csv'

infile_name = 'parsec_results/w_warmup_100m_100m.csv'
infile_name = 'parsec_results/128kb_18ghz_1m.csv'
infile_name = 'parsec_results/3rlat.csv'
infile_name = 'parsec_results/best_100m.csv'
infile_name = 'parsec_results/csvs/64width_100m.csv'
infile_name = 'parsec_results/csvs/8reps_100m.csv'
infile_name = 'parsec_results/csvs/64width_18GHz_100mwarm_100msim_3jul.csv'
infile_name = 'parsec_results/csvs/64width_36GHz_10mwarm_100msim_4jul.csv'
# infile_name = 'parsec_results/csvs/moesi.csv'



# True
# False

use_totcycles = False
# use_totcycles = True

use_numcycles = True
use_numcycles = False

use_simticks = False
# use_simticks = True

use_siminsts = False
# use_siminsts = True

use_ipc = False

# use_pkt_lat = True
# outfile_suffix = '2MB_18GHz_20m_pktLat'

use_both = True

outfile_suffix = '500kB_10m_both_simticks_lim_v3'

outfile_suffix = '128kb_18ghz_1m_both'
outfile_suffix = '3rlat_both'
outfiitle_suffix = 'best_100m_both'
outfile_suffix = '64width_18GHz_100m_both'
outfile_suffix = '64width_36GHz_10mwarm_100msimul_both'
# outfile_suffix = 'moesi'

outfile_suffix = '38GHz_100mwarm_100msimul_both'


count_type = ''

try:
    infile_name = sys.argv[1]
    outfile_suffix = sys.argv[2]
    count_type = sys.argv[3]
except:
    pass


if count_type == 'simticks':
    use_simticks = True
if count_type == 'numcycles':
    use_numcycles = True
if count_type == 'totcycles':
    use_totcycles = True
if count_type == 'siminsts':
    use_siminsts = True
if count_type == 'ipc':
    use_ipc = True

if use_numcycles:
    outfile_suffix += '_ncycles'
if use_totcycles:
    outfile_suffix += '_totcycles'
if use_simticks:
    outfile_suffix += '_simticks'
if use_siminsts:
    outfile_suffix += '_siminsts'
if use_ipc:
    outfile_suffix += '_ipc'

print(f'reading from {infile_name}, writing to {outfile_suffix}, using {count_type}')

# 500kB

# incomple
bad_benches = []

bad_benches += ['vips']

# bad_benches += ['swaptions','fluidanimate']

# bad_benches += ['blackscholes']
# bad_benches += []
# bad_benches += ['canneal','fluidanimate','facesim','swaptions']
# bad_benches += ['ferret']

# # # 250kB
# bad_benches += ['blackscholes']

# actuyally just slow
# timeout
# bad_benches += ['streamcluster']
# bad_benches += ['raytrace']
# bad_benches += ['streamcluster','vips','dedup','ferret']

# bad_benches += ['dedup']

topos = []


double_rename = {'Kite Small':'Kite',
'Kite Med':'Kite',
'Kite Large':'Kite',
'NS-LatOp Small':'NS-LatOp',
'NS-LatOp Med':'NS-LatOp',
'NS-LatOp Large':'NS-LatOp',
'NS-BWOp Small':'NS-BWOp',
'NS-BWOp Med':'NS-BWOp',
'NS-BWOp Large':'NS-BWOp',
'NS-SCOp Small':'NS-SCOp',
'NS-SCOp Med':'NS-SCOp',
'NS-SCOp Large':'NS-SCOp',
'LPBT-Power Small':'LPBT-P',
'LPBT-Hops Small':'LPBT-H',
'LPBT-Hops Med':'LPBT-H',
'Folded Torus':'Folded Torus',
'Butter Donut':'Butter Donut',
'Dbl Butterfly':'Dbl Butterfly'

}


color_dict = {'NS-LatOp Small':'tab:blue',
                'NS-BWOp Small':'tab:orange',
                'NS-SCOp Small':'tab:orange',

              'NS-LatOp Med':'tab:red',
              'NS-BWOp Med':'tab:purple',
              'NS-SCOp Med':'tab:purple',

              'NS-LatOp Large':'tab:green',
              'NS-BWOp Large':'tab:gray',
              'NS-SCOp Large':'tab:gray',

              'Kite Small':'tab:olive',
              'LPBT-Power Small':'blueviolet',
              'LPBT-Hops Small':'peru',

              'Kite Med':'tab:brown',
              'LPBT-Hops Med':'teal',

              'Butter Donut':'lightcoral',
              'Dbl Butterfly':'tab:cyan',
              'Kite Large':'mediumaquamarine',
              'Folded Torus':'goldenrod',

              'CMesh':'gold'  }

rename_dict = { '20r_15ll_opt_ulinks_noci':'NS-LatOp Small',
                '20r_2ll_runsol_ulinks_noci':'NS-LatOp Med',
                '20r_25ll_timed7days_ulinks_noci':'NS-LatOp Large',
                '20r_15ll_opt_8bw_4diam_ulinks_noci':'NS-BWOp Small',
                '20r_4p_2ll_runsol_12bw_ulinks_noci':'NS-BWOp Med',
                '20r_4p_25ll_runsol_14bw_ulinks_noci':'NS-BWOp Large',
                'butter_donut_x_noci':'Butter Donut',
                'cmesh_x_noci':'CMesh',
                'dbl_bfly_x_noci':'Dbl Butterfly',
                'kite_small_noci':'Kite Small',
                'kite_medium_noci':'Kite Med',
                'ft_x_noci':'Folded Torus',
                'kite_large_noci':'Kite Large',
                'ns_s_latop_noci':'NS-LatOp Small',
                'ns_s_bwop_noci':'NS-BWOp Small',
                'ns_m_latop_noci':'NS-LatOp Med',
                'ns_m_bwop_noci':'NS-BWOp Med',
                'ns_l_latop_noci':'NS-LatOp Large',
                'ns_l_bwop_noci':'NS-BWOp Large',
                'ns_s_latop':'NS-LatOp Small',
                'ns_s_bwop':'NS-BWOp Small',
                'ns_m_latop':'NS-LatOp Med',
                'ns_m_bwop':'NS-BWOp Med',
                'ns_l_latop':'NS-LatOp Large',
                'ns_l_bwop':'NS-BWOp Large',
                'butter donut':'Butter Donut',
                'dbl bfly':'Dbl Butterfly',
                'kite small':'Kite Small',
                'kite med':'Kite Medium',
                'kite large':'Kite Large',
                'mesh_noci':'Mesh',
                'lpbt_20r_5p_15ll_power_runsol_noci':'LPBT-Power Small',
                'lpbt_20r_5p_15ll_total_hops_runsol_noci':'LPBT-Hops Small',
                'lpbt_20r_5p_2ll_total_hops_runsol_noci':'LPBT-Hops Med',
                'lpbt_s_power_noci':'LPBT-Power Small',
                'lpbt_s_latop_noci':'LPBT-Hops Small',
                'lpbt_m_latop_noci':'LPBT-Hops Med',
                'ns_s_scop':'NS-SCOp Small',
                'ns_m_scop':'NS-SCOp Med',
                'ns_l_scop':'NS-SCOp Large',
                'ns_s_scop_noci':'NS-SCOp Small',
                'ns_m_scop_noci':'NS-SCOp Med',
                'ns_l_scop_noci':'NS-SCOp Large',
                }

# desired_topologies=[
# # '20r_15ll_opt', '20r_15ll_opt_ulinks',
# # '20r_25ll_timed7days', '20r_25ll_timed7days_ulinks',
# # '20r_2ll_opt', '20r_2ll_runsol_ulinks',
# 'ns_s_latop',
# 'ns_m_latop',
# 'ns_l_latop',
# # 'ns_s_bwop',
# # 'ns_m_bwop',
# # 'ns_l_bwop',
# 'butter_donut_x', 'dbl_bfly_x',
# 'kite_large', 'kite_medium', 'kite_small',
# 'cmesh_x',

# # 'mesh'
# ]

# used after rename
desired_topologies = [
'Kite Small',
'LPBT-Hops Small',
'LPBT-Power Small',
'NS-LatOp Small',
# 'NS-BWOp Small',
'NS-SCOp Small',

'Folded Torus',
'Kite Med',
'LPBT-Hops Med',
'NS-LatOp Med',
# 'NS-BWOp Med',
'NS-SCOp Med',

'Butter Donut',
'Dbl Butterfly',
'Kite Large',
'NS-LatOp Large',
# 'NS-BWOp Large',
'NS-SCOp Large',

# 'CMesh'
]


data = {}

with open(infile_name, 'r') as inf:
    csv_inf = csv.reader(inf)

    headers = []

    bench_idx = 1
    topo_idx = 2
    max_cycles_idx = 11
    pkt_lat_idx = 6
    num_cycles_idx = 4
    tot_cycles_idx = 10

    for line in csv_inf:
        print(f'line={line}')

        if len(headers) == 0:
            headers = line
            bench_idx = headers.index('bench')
            topo_idx = headers.index('config')
            max_topo_idx = headers.index('config')
            max_cycles_idx = headers.index('maxCycles')
            pkt_lat_idx = headers.index( 'average_packet_latency')
            num_cycles_idx = headers.index('numCycles')
            tot_cycles_idx = headers.index('cumulativeCycles')
            sim_ticks_idx = headers.index('simTicks')
            ipc_idx = headers.index('geoIPC')
            continue

        bench = line[bench_idx]
        if bench in bad_benches:
            continue

        topo = line[topo_idx]

        topo = topo.replace('_naive_hops','')
        topo = topo.replace('_cload_picky_hops','')
        topo = topo.replace('_augmclb_hops','')
        topo = topo.replace('_picky_cohmem_prioritized_doubley_memory_mclb_hops','')
        topo = topo.replace('_nndbt_injej_none','')

        renamed_topo = rename_dict[topo]

        try:
            cycles_str = line[max_cycles_idx]

            # print(f'max cycles={cycles}')

            if use_numcycles:
                # numCycles instead of maxCycles
                cycles_str = line[num_cycles_idx]

                # print(f'num cycles={cycles}')

            # # totalCycles instead of maxCycles
            if use_totcycles:
                cycles_str = line[tot_cycles_idx]
                # print(f'cycles_str={cycles_str}')

                # print(f'tot cycles={cycles}')

            if use_simticks:
                cycles_str = line[sim_ticks_idx]

            if use_ipc:
                cycles_str = line[ipc_idx]


                # print(f'simticks cycles={cycles}')

            cycles = float(cycles_str)

            # print(f'cycles={cycles}')
        except:
            # print(f'defauting for topo={renamed_topo}')
            cycles = 0

        try:
            pkt_lat = float(line[pkt_lat_idx])
        except:
            pkt_lat = 0

        try:
            _ = data[bench]
        except:
            data.update({ bench : {} })

        try:
            _ = data[bench][renamed_topo]
            # _ = data[bench][topo]
        except:
            data[bench].update({renamed_topo : {}})
            # data[bench].update({topo : {}})


        data[bench][renamed_topo].update( {'maxCycles' : cycles })
        data[bench][renamed_topo].update( {'pkt_lat' : pkt_lat })
        # data[bench][topo].update( {'maxCycles' : cycles })
        # data[bench][topo].update( {'pkt_lat' : pkt_lat })

        # if 'mesh' in renamed_topo.lower():
        #     here = input(f'renamed_topo={renamed_topo} data[bench][renamed_topo] ={data[bench][renamed_topo]}')



        # if 'mesh' in renamed_topo.lower() and 'dedup' in bench:
        #     print(f'cycles = {cycles}')
        #     quit()


bench_list = []
topo_list = []
for bench, topo_data in data.items():

    if bench not in bench_list:
        bench_list.append(bench)

    try:
        mesh_base_cycles = topo_data['Mesh']['maxCycles']


    except:
        mesh_base_cycles = 0



    if mesh_base_cycles == 0:
        continue
    mesh_rel_cycles = 1
    topo_data['Mesh'].update({'relCycles' : mesh_rel_cycles})

    mesh_base_pkt_lat = topo_data['Mesh']['pkt_lat']
    topo_data['Mesh'].update({'rel_pkt_lat':1})

    for topo, met_data in topo_data.items():
        if topo not in topo_list:
            topo_list.append(topo)
        this_cycles = met_data['maxCycles']
        try:

            this_rel_cycles = mesh_base_cycles / this_cycles

            if use_siminsts or use_ipc:
                this_rel_cycles = this_cycles / mesh_base_cycles
        except:
            this_rel_cycles = 0
        met_data.update({ 'relCycles' : this_rel_cycles })

        # this_pkt_lat = met_data['pkt_lat']
        try:
            # rel_pkt_lat = met_data['pkt_lat'] / mesh_base_pkt_lat
            rel_pkt_lat = mesh_base_pkt_lat / met_data['pkt_lat']

        except:
            rel_pkt_lat = 0
        met_data.update({'rel_pkt_lat':rel_pkt_lat})


## calc goemean
gmeans = []

data.update({'geomean' : {}})

for topo in desired_topologies:

    runprod = 1
    n_elems = 0

    for bench in bench_list:
        if bench in bad_benches:
            continue

        try:
            val = data[bench][topo]['relCycles']
        except:
            val = 1
        runprod *= val
        n_elems += 1

    gmean = runprod**(1/n_elems)
    gmeans.append(gmean)
    data['geomean'].update({topo : {}})
    data['geomean'][topo].update({'relCycles' : gmean})

for topo in desired_topologies:

    runprod = 1
    n_elems = 0

    for bench in bench_list:
        if bench in bad_benches:
            continue

        try:
            val = data[bench][topo]['rel_pkt_lat']
        except:
            val = 1
        runprod *= val
        n_elems += 1

    gmean = runprod**(1/n_elems)
    gmeans.append(gmean)
    data['geomean'][topo].update({'rel_pkt_lat' : gmean})

for topo,topo_data in data['geomean'].items():
    print(f'{topo} geomean rel cycles={topo_data["relCycles"]}')
for topo,topo_data in data['geomean'].items():
    print(f'{topo} geomean pkt lat={topo_data["rel_pkt_lat"]}')
# quit()

tmp_bench = bench_list.copy()

# inj rate
bench_list = [
    'bodytrack',
    'swaptions',
    'canneal',
    'fluidanimate',
    'streamcluster',
    'ferret',
    'facesim',
    'dedup',
    'raytrace',
    'freqmine',
    'blackscholes',
    'x264',
    'geomean'
]

# mpki
bench_list = [
    'dedup',
    'swaptions',
    'bodytrack',
    'blackscholes',
    'raytrace',
    'fluidanimate',
    'streamcluster',
    'ferret',
    'facesim',
    'freqmine',
    'x264',
    'canneal',

    'geomean'
]

# ['canneal', 'bodytrack', 'streamcluster', 'facesim', 'raytrace', 'ferret', 'freqmine', 'blackscholes', 'dedup', 'x264', 'swaptions', 'fluidanimate']
# new_bench = []
# for b in ordered_benches:
#     # if b in bad_benches:
#     #     continue

#     new_bench.append(b)

# bench_list = new_bench.copy()

# bench_list.append('geomean')

print(f'bench_list={bench_list}')
# quit()




for bench, topo_data in data.items():

    print(f'bench={bench}')
    for topo, met_data in topo_data.items():
        print(f'\ttopo={topo}')
        for met, val in met_data.items():
            print(f'\t\t{met} : {val}')




# gen graph values

# list of lists
y_vals_list = []
y_labels = []

secondary_y_vals_list = []

x_val_list = []


for topo in desired_topologies:

    # if topo not in desired_topologies:
    #     continue

    y_vals_list.append([])
    secondary_y_vals_list.append([])

    try:
        new_name = double_rename[topo]
    except Exception as e:
        print(f'e={e}')
        quit()
        new_name = topo

    y_labels.append(topo)


    for bench in bench_list:
        if bench in bad_benches:
            continue

        #print(f'data[bench][topo]={data[bench][topo]}')


        if bench not in x_val_list:
            x_val_list.append(bench)

        try:
            print(f'data[{bench}][{topo}]={data[bench][topo]}')
        except:
            pass

        try:
            val = data[bench][topo]['relCycles']
        except:
            val = 0
        y_vals_list[-1].append(val)


        try:
            val = data[bench][topo]['rel_pkt_lat']
        except:
            val = 0
        secondary_y_vals_list[-1].append(val)









plt.cla()
# plt.clear()
plt.rc('font', size=10) #controls default text size
plt.rc('axes', titlesize=15) #fontsize of the title
plt.rc('axes', labelsize=14) #fontsize of the x and y labels
plt.rc('xtick', labelsize=14) #fontsize of the x tick labels
plt.rc('ytick', labelsize=10) #fontsize of the y tick labels
plt.rc('legend', fontsize=12)

plt.rc('text', usetex=True)

fig = plt.figure(figsize=(14,2))
ax = fig.add_subplot()

plt.ylabel('Execution Speedup')

if use_both:
    ax2 = ax.twinx()
    plt.ylabel('Pkt. Latency Reduction (+)')

# plt.xlabel("Injection Rate (pkts/cpu/cycle)")
# plt.ylabel("Speedup")
# ax.set_label('Execution Speedup')
# if use_both:
#     ax2.set_label('Avg. Pkt. Latency Reduction')

width = 0.4
gap = 0.05


last_of_size = [4,9]


n_benches = len(x_val_list)
mult = 8.5
x = np.arange(0,mult*n_benches,mult)

offset = -7*(width+gap)
for i in range(len(y_vals_list)):
    # print(f'x({len(x)})={x}')
    # print(f'y_vals({len(y_vals_list)})={y_vals_list}')
    offset += width+gap
    lab = y_labels[i]

    try:
        new_lab = double_rename[lab]
    except:
        new_lab = lab
    col = color_dict[lab]

    if use_both:
        ax.bar(x + offset, y_vals_list[i],width, edgecolor='black',linewidth=0.5,color=col,label=new_lab)

        pkt_lat_color = 'black'
        if 'NS' in y_labels[i]:
            pkt_lat_color = 'red'
        ax2.scatter(x+offset,secondary_y_vals_list[i],color=pkt_lat_color,marker='+',label=y_labels[i])

    elif not use_pkt_lat:
        ax.bar(x + offset, y_vals_list[i],width, edgecolor='black',linewidth=0.5,color=col,label=new_lab)
    else:
    # secondary_y_vals_list[]
        ax.bar(x + offset, secondary_y_vals_list[i],width, edgecolor='black',linewidth=0.5,color=col,label=new_lab)
        # ax2.scatter(x+offset,secondary_y_vals_list[i],color='k',marker='+',label=y_labels[i])
    if i in last_of_size:
        offset += 4*gap


ax.set_xticks(x)
# ax.set_xticklabels(x_val_list)#,horizontalalignment='left', rotation=-20, rotation_mode="anchor")
ax.set_xticklabels(x_val_list,horizontalalignment='left', rotation=-20, rotation_mode="anchor")

max_x = max(x)

ax.set_xlim([-3.5,max_x+(1.5*mult*width)])
# ax.set_xlim([-3.5,110])


y = np.arange(0.5,4.0,0.1)
y_minor = np.arange(0.5,4.0,0.1)
ax.set_yticks(y)
ax.set_yticks(y_minor,minor=True)

# FLAG

# ax.set_ylim([1.0,1.5])
# ax2.set_ylim([1.0,1.4])

# FLAG y lim ylim

# ax.set_ylim([0.8,1.45])
# ax2.set_ylim([0.8,1.45])


ax.set_ylim([0.5,1.55])
ax2.set_ylim([0.5,1.55])

ax.grid(which='major',alpha=0.5)
ax.grid(which='minor',alpha=0.5)

if use_both:
    ax2.grid(which='minor',alpha=0.15)

handles, labels = ax.get_legend_handles_labels()

p0 = plt.plot([],[],color='none',label=' ')
p4 = plt.plot([],[],color='none',label=' ')
p7 = plt.plot([],[],color='none',label=' ')
p8 = plt.plot([],[],color='none',label=' ')

p12 = plt.plot([],[],color='none',label=' ')
p15 = plt.plot([],[],color='none',label=' ')

p16 = plt.plot([],[],color='none',label=' ')
p20 = plt.plot([],[],color='none',label=' ')
p23 = plt.plot([],[],color='none',label=' ')


# proxy3 = plt.plot([],[],color='none',label=' ')
# proxy7 = plt.plot([],[],color='none',label=' ')

handles.insert(0,p0[0])
handles.insert(4,p4[0])
handles.insert(7,p7[0])
handles.insert(8,p8[0])

handles.insert(12,p12[0])
handles.insert(15,p15[0])
handles.insert(16,p16[0])

handles.insert(20,p20[0])
handles.insert(23,p23[0])

# handles.insert(7,proxy7[0])

labels.insert(0,r'\underline{Small}')
labels.insert(4,' ')
labels.insert(7,' ')

labels.insert(8,r'\underline{Medium}')
labels.insert(12,' ')
labels.insert(15,' ')

labels.insert(16,r'\underline{Large}')
labels.insert(20,' ')
labels.insert(23,' ')

# labels.insert(7,' ')

# ax.legend(handles, labels,ncol=5,bbox_to_anchor=(.1, 1.2))

# ax.legend(handles, labels,ncol=5,bbox_to_anchor=(0.225, 1.02, 1., .102))

ax.legend(handles, labels,ncol=6,bbox_to_anchor=(0.075, 1.0, 0.1, .1),loc='lower left')

# ax.legend(handles, labels,ncol=5)


# plt.title(outfile_suffix)

# plt.grid(linestyle='-', linewidth=0.5)

outname=f'./parsec_results/graphs/parsec_bar_{outfile_suffix}.png'
print(f'writing out to : {outname}')
# plt.savefig(outname,bbox_inches='tight',dpi=1200)
plt.savefig(outname,bbox_inches='tight')
print(f'wrote out to : {outname}')

plt.show()
