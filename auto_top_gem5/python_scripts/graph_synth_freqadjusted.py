import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from matplotlib import rc

import csv
import sys


use_latex_legend = False

# shortcut
MAX_VAL = 30#None
MAX_Y = 25

DPI = 1200
use_input = False

desired_topologies_30r=[
        # '30r_4p_25ll_runsol',
        # '30r_15ll_opt',
        '30r_kite_small',
        '30r_4p_15ll_runsol_ulinks',

        '30r_ft_x',
        '30r_kite_med',
        '30r_4p_2ll_runsol_ulinks',
        '30r_butter_donut_x',
        '30r_dbl_bfly_x',
        '30r_kite_large',
        '30r_4p_25ll_runsol_ulinks',


        # '30r_4p_2ll_runsol',
                # '30r_butter_donut_x',

        ]



rename_dict = {
    # '30r_15ll_opt':'NS-Sym Small',
     '30r_4p_15ll_runsol_ulinks':'NS-LatOp Small',
# '30r_4p_25ll_runsol':'NS-Sym Large',
'30r_4p_25ll_runsol_ulinks':'NS-LatOp Large',
# '30r_4p_2ll_runsol':'NS-Sym Medium',
 '30r_4p_2ll_runsol_ulinks':'NS-LatOp Med',
'30r_butter_donut_x':'Butter Donut', '30r_dbl_bfly_x':'Dbl Butterfly',
'30r_kite_large':'Kite Large', '30r_kite_med':'Kite Med', '30r_kite_small':'Kite Small',
'30r_ft_x':'Folded Torus',
'cmesh_x':'CMesh', 'mesh':'Mesh'}

double_rename = {'Kite Small':'Kite',
'Kite Med':'Kite',
'Kite Large':'Kite',
'NS-LatOp Small':'NS-LatOp',
'NS-LatOp Med':'NS-LatOp',
'NS-LatOp Large':'NS-LatOp',
'NS-BWOp Small':'NS-BWOp',
'NS-BWOp Med':'NS-BWOp',
'NS-BWOp Large':'NS-BWOp',
}

color_dict = {'NS-LatOp Small':'tab:red',
                'NS-BWOp Small':'tab:green',

              'NS-LatOp Med':'tab:red',
              'NS-BWOp Med':'tab:green',

              'NS-LatOp Large':'tab:red',
              'NS-BWOp Large':'tab:green',

              'NS-SCOp Small':'tab:blue',
              'NS-SCOp Med':'tab:blue',
              'NS-SCOp Large':'tab:blue',

            #   'Kite Small':'tab:brown',
              'Kite Small':'lightcoral',
              'LPBT-Power Small':'blueviolet',
              'LPBT-Hops Small':'peru',

            #   'Kite Med':'tab:brown',
              'Kite Med':'lightcoral',
              'LPBT-Hops Med':'peru',
              'Folded Torus':'tab:grey',
            #   'Butter Donut':'lightcoral',
              'Butter Donut':'tab:brown',

              'Dbl Butterfly':'tab:cyan',
            #   'Kite Large':'tab:brown',
              'Kite Large':'lightcoral',


              'NS-ShufOpt Small':'k',
              'NS-ShufOpt Med':'k',
              'NS-ShufOpt Large':'k',

              'CMesh':'gold'
              }

# latop='s'
# bwop='D'
# prev='o'

latop='o'
bwop='o'
prev='D'

label_to_marker={
'NS-LatOp Small':latop,
                'NS-BWOp Small':bwop,

              'NS-LatOp Med':latop,
              'NS-BWOp Med':bwop,
              'NS-LatOp Large':latop,
              'NS-BWOp Large':bwop,

              'Kite Small':prev,
              'Kite Med':prev,
              'Folded Torus':prev,
              'Butter Donut':prev,
              'Dbl Butterfly':prev,
              'Kite Large':prev,

}




topo_to_marker={
'ns_s_latop':latop,
'ns_m_latop':latop,
'ns_l_latop':latop,
'ns_s_bwop':bwop,
'ns_s_scop':bwop,
'20r_4p_15ll_runsol_scbw':bwop,

'20r_4p_15ll_runsol_shuffle_ulinks':bwop,

'ns_m_bwop':bwop,
'ns_m_scop':bwop,
'20r_4p_2ll_runsol_scbw':bwop,

'20r_4p_2ll_runsol_shuffle_ulinks':bwop,


'ns_l_bwop':bwop,
'ns_l_scop':bwop,
'20r_4p_25ll_runsol_scbw':bwop,

'20r_4p_25ll_runsol_shuffle_ulinks':bwop,


'butter_donut_x':prev,
'dbl_bfly_x':prev,
'kite_large':prev,
'kite_medium':prev,
'kite_small':prev,
'ft_x':prev,
'lpbt_s_power':prev,
                'lpbt_s_latop':prev,
                'lpbt_m_latop':prev,


# 'cmesh_x', 'mesh'
}

desired_topologies=[
#     '20r_15ll_opt', '20r_15ll_opt_ulinks',
# '20r_25ll_timed7days', '20r_25ll_timed7days_ulinks',
# '20r_2ll_opt', '20r_2ll_runsol_ulinks',

'kite_small',
'lpbt_s_latop',
'lpbt_s_power',
'ns_s_latop',
# 'ns_s_bwop',
# '20r_4p_15ll_runsol_scbw',
'ns_s_scop',
'20r_4p_15ll_runsol_shuffle_ulinks',


'ft_x',
'kite_medium',
'lpbt_m_latop',

'ns_m_latop',
# 'ns_m_bwop',

# TODO here
# '20r_4p_2ll_runsol_scbw',
'ns_m_scop',
'20r_4p_2ll_runsol_shuffle_ulinks',


'butter_donut_x',
'dbl_bfly_x',
'kite_large',
'ns_l_latop',
# 'ns_l_bwop',
# '20r_4p_25ll_runsol_scbw',
'ns_l_scop',
'20r_4p_25ll_runsol_shuffle_ulinks',




# 'cmesh_x', 'mesh'
]


desired_topologies_64r=[

'kite_small',
'ns_s_latop',

'ft_x',
'kite_medium',
'ns_m_latop',

'butter_donut_x',
'dbl_bfly_x',
'ns_l_latop',

]



rename_dict = {
    '20r_15ll_opt':'NS-Sym Small', '20r_15ll_opt_ulinks':'NS-Asym Small',
'20r_25ll_timed7days':'NS-Sym Large', '20r_25ll_timed7days_ulinks':'NS-Asym Large',
'20r_2ll_opt':'NS-Sym Medium', '20r_2ll_runsol_ulinks':'NS-Asym Medium',
'ns_s_latop':'NS-LatOp Small','ns_s_bwop':'NS-BWOp Small',
'ns_m_latop':'NS-LatOp Med','ns_m_bwop':'NS-BWOp Med',
'ns_l_latop':'NS-LatOp Large','ns_l_bwop':'NS-BWOp Large',
'butter_donut_x':'Butter Donut', 'dbl_bfly_x':'Dbl Butterfly',
'kite_large':'Kite Large', 'kite_medium':'Kite Med', 'kite_small':'Kite Small',
'ft_x':'Folded Torus',
'cmesh_x':'CMesh', 'mesh':'Mesh',
    'lpbt_20r_5p_15ll_power_runsol_noci':'LPBT-Power Small',
    'lpbt_20r_5p_15ll_total_hops_runsol_noci':'LPBT-Hops Small',
    'lpbt_20r_5p_2ll_total_hops_runsol_noci':'LPBT-Hops Med',
                'lpbt_s_power':'LPBT-Power Small',
                'lpbt_s_latop':'LPBT-Hops Small',
                'lpbt_m_latop':'LPBT-Hops Med',
                    # '30r_15ll_opt':'NS-Sym Small',
     '30r_4p_15ll_runsol_ulinks':'NS-LatOp Small',
# '30r_4p_25ll_runsol':'NS-Sym Large',
'30r_4p_25ll_runsol_ulinks':'NS-LatOp Large',
# '30r_4p_2ll_runsol':'NS-Sym Medium',
 '30r_4p_2ll_runsol_ulinks':'NS-LatOp Med',
'30r_butter_donut_x':'Butter Donut', '30r_dbl_bfly_x':'Dbl Butterfly',
'30r_kite_large':'Kite Large', '30r_kite_med':'Kite Med', '30r_kite_small':'Kite Small',
'30r_ft_x':'Folded Torus',
'cmesh_x':'CMesh', 'mesh':'Mesh',

'20r_4p_15ll_runsol_scbw':'NS-SCOp Small',
'20r_4p_2ll_runsol_scbw':'NS-SCOp Med',
'20r_4p_25ll_runsol_scbw':'NS-SCOp Large',


'ns_s_scop':'NS-SCOp Small',
'ns_m_scop':'NS-SCOp Med',
'ns_l_scop':'NS-SCOp Large',


'20r_4p_15ll_runsol_shuffle_ulinks':'NS-ShufOpt Small',
'20r_4p_2ll_runsol_shuffle_ulinks':'NS-ShufOpt Med',
'20r_4p_25ll_runsol_shuffle_ulinks':'NS-ShufOpt Large',


}

custom_rename = {'bdonut':'butter_donut_x','ft':'ft_x','dbl_bfly':'dbl_bfly_x','kite_med':'kite_medium','48r_4p_25ll_runsol_ulinks':'ns_l_latop','48r_4p_2ll_runsol_ulinks':'ns_m_latop','48r_4p_15ll_runsol_ulinks':'ns_s_latop'}


# cycles are system anyway
def convert(inj_cycles, freq):#, size):

    # inj rate is pkts/cpu/cycle
    # want ratio of cycle / ns so
    # 2 Ghz => 2000000000 cycles / sec
    # 2000000000 cycles / sec => 0.5ns


    # 4 Ghz => 0.25
    

    return inj_cycles*freq


def gen_synth_20r_3subplots_shuffle(infile_name='./synth_outputs/simple_2b.csv', param_mem_or_coh='coh',param_alg='cload'):

    print(f'reading from {infile_name}')
    # input('press any key')

    data = {}
    configs = []

    with open(infile_name, 'r') as inf:
        csv_inf = csv.reader(inf)

        headers = []

        time_axis = []

        for line in csv_inf:

            if len(headers) == 0:
                headers = line
                continue

            if '' in line:
                line.remove('')

            # if 'coh' in line:
            #     continue


            # print(f'{line}')
            # quit()


            mem_or_coh = line[2]
            config = line[4]
            alg = line[3]

            # new order
            config = line[3]
            alg = line[4]


            # if param_alg not in alg:
            #     print(f'{param_alg} not in {alg}')
            #     continue


            inj_rate_str = line[5]
            # inj_rate_str = line[4]

            try:
                pkt_lat_str = line[6]
                # pkt_lat_str = line[5]
            except:
                pkt_lat_str = '100000000.0'
                # pkt_lat_str = '0'

            configs.append(config)

            # hotfix
            if len(inj_rate_str) == 3:
                inj_rate_str = inj_rate_str + '0'

            inj_rate = float(inj_rate_str.split('_')[-1])
            factor = 100
            
            if len(inj_rate_str.split('_')[-1]) >= 3:
                # print(f'odd')
                factor = 1000

            inj_rate = inj_rate / factor

            # parse and convert to ns
            pkt_lat = float(pkt_lat_str) / 1000.0

            # init
            try:
                _ = data[mem_or_coh]
            except:
                data.update({mem_or_coh : {} })

            try:
                _ = data[mem_or_coh][config]
            except:
                data[mem_or_coh].update({config : {}})

            data[mem_or_coh][config].update({inj_rate : pkt_lat})


    for memcoh, config_data_dict in data.items():
        # if memcoh == 'coh':
            # continue
        print(f'{memcoh}')
        for config,inj_data_dict in config_data_dict.items():
            print(f'\t{config}')
            for ir, pl in inj_data_dict.items():

                # c_ir = ir*2*4*()

                print(f'\t\t{ir} : {pl}')

    ######################################################################################

    plt.cla()
    # plt.clear()
    plt.rc('font', size=16) #controls default text size
    plt.rc('axes', titlesize=14) #fontsize of the title
    plt.rc('axes', labelsize=14) #fontsize of the x and y labels
    plt.rc('xtick', labelsize=10) #fontsize of the x tick labels
    plt.rc('ytick', labelsize=10) #fontsize of the y tick labels
    plt.rc('legend', fontsize=14)

    if use_latex_legend:
        plt.rc('text', usetex=True)

    fig = plt.figure(figsize=(7,4))

    axes = []
    axes.append(fig.add_subplot(3,1,1))
    axes.append(fig.add_subplot(3,1,2))
    axes.append(fig.add_subplot(3,1,3))



    # for memcoh, config_data_dict in data.items():
    #     print(f'{memcoh}')
    #     for config,inj_data_dict in config_data_dict.items():
    #         print(f'\t{config}')
    #         for ir, pl in inj_data_dict.items():
    #             print(f'\t\t{ir} : {pl}')


    config_data_dict = data[param_mem_or_coh]
    # for config,inj_data_dict in config_data_dict.items():
    #     if config not in desired_topologies:
    #         print(f'config {config} not in desired {desired_topologies}')
    #         continue

    mylabels = []


    for config in desired_topologies:
        try:
            inj_data_dict = config_data_dict[config]
        except:
            continue
        # print(f'\t{config}')
        injs = []
        lats = []

        max_val = len(inj_data_dict)

        # print(f'max_val={max_val}')
        # quit()

        if MAX_VAL is not None:
            max_val = MAX_VAL

        # print(f'({len(inj_data_dict)}) {inj_data_dict}')
        # quit()

        # X = [i/100.0 for i in range(1,max_val+1)]
        # X = [i/100.0 for i in range(1,max_val+1)]

        step = 0.005

        X = [round(x,3) for x in np.arange(0.005,(max_val+1)/100.0,step)]

        print(f'X={X}')
        # quit()

        for x in X:
            injs.append(x)

            try:
                lat = inj_data_dict[x]
            except:
                lat = 10000000000

            lats.append(lat)



        # small
        size = 0
        if '_m_' in config:
            size = 1
        elif 'ft_x' in config:
            size = 1
        elif 'med' in config:
            size = 1
        elif '_l_' in config:
            size = 2
        elif 'dbl' in config or 'butt' in config:
            size = 2
        elif 'large' in config:
            size = 2
        elif '2ll' in config:
            size = 1
        elif '25ll' in config:
            size = 2

        print(f'{config} : size={size}')


        # print(f'before ns adjust:\n\tX={X}')



        # # convert cycles of cpu to ns
        # sys_clk = 4
        # X = [2*convert(x,sys_clk) for x in X]

        # print(f'after ns adjust:\n\tX={X}')



        # size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}

        # clk_adjustment = size_to_freq[size] / sys_clk

        # X = [clk_adjustment*x for x in X]

        # print(f'after noi clk adjust:\n\tX={X}')


        max_x = max(X)

        # input('good?')

        # for ir, pl in inj_data_dict.items():
            # print(f'\t\t{ir} : {pl}')



            # injs.append(ir)
            # lats.append(pl)



        new_name = rename_dict[config]
        mylabels.append(new_name)
        mark = topo_to_marker[config]
        col = color_dict[new_name]




        print(f'before ns adjust:\n\injs={injs}')

        # convert cycles of cpu to ns
        sys_clk = 4
        injs = [2*convert(x,sys_clk) for x in injs]

        print(f'after ns adjust:\n\injs={injs}')



        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        injs = [clk_adjustment*x for x in injs]


        injs = [round(x,3) for x in injs]

        print(f'after noi clk adjust:\n\injs={injs}')



        ############3
        print(f'before ns adjust:\n\injs={injs}')

        # convert cycles of cpu to ns
        sys_clk = 4
        # lats = [2*convert(x,sys_clk) for x in lats]

        print(f'after ns adjust:\n\lats={lats}')


        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        lats = [x/clk_adjustment for x in lats]

        lats = [round(l,3) for l in lats]
        print(f'after noi clk adjust:\n\lats={lats}')


        sorted_lats = [x for _,x in sorted(zip(injs,lats))]
        sorted_injs= [x for x,_ in sorted(zip(injs,lats))]

        # print(f'plotting {sorted_injs} : {sorted_lats}')
        # print(f'plotting {sorted_injs} v {sorted_lats}')
        print(f'topology : {new_name}')
        for i, injr in enumerate(sorted_injs):
            print(f'\t{injr:5} : {sorted_lats[i]}')

        # input('good?')

        # plt.plot(injs, lats, label=new_name,linestyle='--',marker=mark, markersize=5,color=col)

        is_ns = False
        if 'NS' in new_name:
            is_ns = True

        msize = 5
        if not is_ns:
            msize = 6

        axes[size].plot(sorted_injs, sorted_lats, label=new_name,linestyle='--',marker=mark, markersize=msize,color=col)

    # print(f'my_labels={mylabels}')
    # quit()

    y = np.arange(0.0,36,10)
    y_minor = np.arange(0.0,35,5)

    for ax in axes:
        ax.set_yticks(y)
        ax.set_yticks(y_minor,minor=True)






    xticks = np.arange(0,1.5,.1)
    xticks_min = np.arange(0,1.5,.05)

    # convert cycles of cpu to ns
    # sys_clk = 4
    # xticks = [2*convert(x,sys_clk) for x in xticks]

    # size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
    # clk_adjustment = size_to_freq[size] / sys_clk
    # xticks = [clk_adjustment*x for x in xticks]

    # xticks_min = [2*convert(x,sys_clk) for x in xticks_min]

    # size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
    # clk_adjustment = size_to_freq[size] / sys_clk
    # xticks_min = [clk_adjustment*x for x in xticks_min]


    # axes[2].set_xticks(x)
    # axes[2].set_xticks(xmin,minor=True)


    if param_mem_or_coh == 'coh':
        # coh
        max_x = 0.55
    else:
        # mem
        max_x = 0.4
    
    
    max_y = 35.0

    # if MAX_Y is not None:
    #     max_y = MAX_Y

    for ax in axes:

        ax.set_xticks(xticks)
        ax.set_xticks(xticks_min,minor=True)

        # plt.grid(which='major',alpha=0.5)
        # plt.grid(which='minor',alpha=0.2)
        # plt.ylim([6, 22.5])
        # plt.xlim([0.0, 0.18])
        ax.grid(which='major',alpha=0.5)
        ax.grid(which='minor',alpha=0.2)
        ax.set_ylim([0, max_y ])
        ax.set_xlim([0.0, max_x])

    axes[1].set_xticklabels([])
    axes[0].set_xticklabels([])

    # axes[2].set_xlabel("Injection Rate  (pkts/cpu/cycle)")
    axes[2].set_xlabel("Injection Rate  (pkts/cpu/ns)")

    axes[1].set_ylabel("Avg. Pkt. Latency (ns)")
    # plt.grid()

    twins = []
    for ax in axes:
        twins.append(ax.twinx())

    twins[0].set_ylabel('Small')
    twins[1].set_ylabel('Medium')
    twins[2].set_ylabel('Large')
    twins[0].set_yticklabels([])
    twins[1].set_yticklabels([])
    twins[2].set_yticklabels([])

    labels = []
    handles = []
    for ax in axes:
        _handles, _labels = ax.get_legend_handles_labels()
        for h in _handles:
            handles.append(h)
        for l in _labels:

            l = l.replace(' Large','')
            l = l.replace(' Med','')
            l = l.replace(' Small','')


            labels.append(l)



    # handles, labels = ax.get_legend_handles_labels()

    proxy0 = plt.plot([],[],color='none',label=' ')
    proxy7 = plt.plot([],[],color='none',label=' ')
    proxy14 = plt.plot([],[],color='none',label=' ')

    # proxy8 = plt.plot([],[],color='none',label=' ')
    # proxy9 = plt.plot([],[],color='none',label=' ')


    handles.insert(0,proxy0[0])
    handles.insert(7,proxy7[0])
    handles.insert(14,proxy14[0])

    # handles.insert(7,proxy7[0])
    # handles.insert(13,proxy14[0])

    # handles.insert(7,proxy7[0])
    # handles.insert(14,proxy14[0])

    # handles.insert(4,proxy4[0])
    # handles.insert(8,proxy8[0])
    # handles.insert(9,proxy9[0])
    # # print(proxy3)

    # # print(handles)
    # # quit()

    if use_latex_legend:
        labels.insert(0,r'\underline{Small}')
        labels.insert(7,r'\underline{Medium}')
        labels.insert(14,r'\underline{Large}')
    else:
        labels.insert(0,'Small')
        labels.insert(7,'Medium')
        labels.insert(14,'Large')

    # # handles, labels = ax.get_legend_handles_labels()

    # proxy0 = plt.plot([],[],color='none',label=' ')
    # proxy6 = plt.plot([],[],color='none',label=' ')
    # proxy12 = plt.plot([],[],color='none',label=' ')

    # # proxy8 = plt.plot([],[],color='none',label=' ')
    # # proxy9 = plt.plot([],[],color='none',label=' ')


    # handles.insert(0,proxy0[0])
    # handles.insert(6,proxy6[0])
    # handles.insert(12,proxy12[0])

    # # handles.insert(4,proxy4[0])
    # # handles.insert(8,proxy8[0])
    # # handles.insert(9,proxy9[0])
    # # # print(proxy3)

    # # # print(handles)
    # # # quit()

    # labels.insert(0,r'\underline{Small}')
    # labels.insert(6,r'\underline{Medium}')
    # labels.insert(12,r'\underline{Large}')

    # labels.insert(4,' ')
    # labels.insert(8,' ')
    # labels.insert(9,' ')



    # plt.legend(mylabels,ncol=3, bbox_to_anchor=(-0.1, 1.0, 1., .102), loc='lower left')


    print(f'handles={handles}')
    print(f'labels={labels}')

    if param_mem_or_coh == 'coh':
        axes[0].legend(handles, labels,ncol=3,bbox_to_anchor=(-0.04, 0.94, 0.2, 0.1), loc='lower left', )


    name = f'./synth_outputs/graphs/simple_20r_shuffle_{param_mem_or_coh}_{param_alg}_freqadjusted.png'
    plt.savefig(name,bbox_inches='tight',dpi=DPI)
    # plt.savefig(name,bbox_inches='tight')
    if use_input:
        input(f'wrote to {name}')

    plt.show()


def gen_synth_20r_3subplots(infile_name='./synth_outputs/simple_2b.csv', param_mem_or_coh='coh',param_alg='cload'):

    print(f'reading from {infile_name}')
    # input('press any key')

    data = {}
    configs = []

    with open(infile_name, 'r') as inf:
        csv_inf = csv.reader(inf)

        headers = []

        time_axis = []

        for line in csv_inf:

            if len(headers) == 0:
                headers = line
                continue

            if '' in line:
                line.remove('')

            # if 'coh' in line:
            #     continue


            # print(f'{line}')
            # quit()


            mem_or_coh = line[2]
            config = line[4]
            alg = line[3]

            # new order
            config = line[3]
            alg = line[4]


            # if param_alg not in alg:
            #     print(f'{param_alg} not in {alg}')
            #     continue


            inj_rate_str = line[5]
            # inj_rate_str = line[4]

            try:
                pkt_lat_str = line[6]
                # pkt_lat_str = line[5]
            except:
                pkt_lat_str = '100000000.0'
                # pkt_lat_str = '0'

            configs.append(config)

            # hotfix
            if len(inj_rate_str) == 3:
                inj_rate_str = inj_rate_str + '0'

            inj_rate = float(inj_rate_str.split('_')[-1])
            factor = 100
            
            if len(inj_rate_str.split('_')[-1]) >= 3:
                # print(f'odd')
                factor = 1000

            inj_rate = inj_rate / factor

            # parse and convert to ns
            pkt_lat = float(pkt_lat_str) / 1000.0

            # init
            try:
                _ = data[mem_or_coh]
            except:
                data.update({mem_or_coh : {} })

            try:
                _ = data[mem_or_coh][config]
            except:
                data[mem_or_coh].update({config : {}})

            data[mem_or_coh][config].update({inj_rate : pkt_lat})


    for memcoh, config_data_dict in data.items():
        # if memcoh == 'coh':
            # continue
        print(f'{memcoh}')
        for config,inj_data_dict in config_data_dict.items():
            print(f'\t{config}')
            for ir, pl in inj_data_dict.items():

                # c_ir = ir*2*4*()

                print(f'\t\t{ir} : {pl}')

    ######################################################################################

    plt.cla()
    # plt.clear()
    plt.rc('font', size=16) #controls default text size
    plt.rc('axes', titlesize=14) #fontsize of the title
    plt.rc('axes', labelsize=14) #fontsize of the x and y labels
    plt.rc('xtick', labelsize=10) #fontsize of the x tick labels
    plt.rc('ytick', labelsize=10) #fontsize of the y tick labels
    plt.rc('legend', fontsize=14)

    if use_latex_legend:
        plt.rc('text', usetex=True)

    fig = plt.figure(figsize=(7,4))

    axes = []
    axes.append(fig.add_subplot(3,1,1))
    axes.append(fig.add_subplot(3,1,2))
    axes.append(fig.add_subplot(3,1,3))



    # for memcoh, config_data_dict in data.items():
    #     print(f'{memcoh}')
    #     for config,inj_data_dict in config_data_dict.items():
    #         print(f'\t{config}')
    #         for ir, pl in inj_data_dict.items():
    #             print(f'\t\t{ir} : {pl}')


    config_data_dict = data[param_mem_or_coh]
    # for config,inj_data_dict in config_data_dict.items():
    #     if config not in desired_topologies:
    #         print(f'config {config} not in desired {desired_topologies}')
    #         continue

    mylabels = []


    for config in desired_topologies:
        try:
            inj_data_dict = config_data_dict[config]
        except:
            continue
        # print(f'\t{config}')
        injs = []
        lats = []

        max_val = len(inj_data_dict)

        # print(f'max_val={max_val}')
        # quit()

        if MAX_VAL is not None:
            max_val = MAX_VAL

        # print(f'({len(inj_data_dict)}) {inj_data_dict}')
        # quit()

        # X = [i/100.0 for i in range(1,max_val+1)]
        # X = [i/100.0 for i in range(1,max_val+1)]

        step = 0.005

        X = [round(x,3) for x in np.arange(0.005,(max_val+1)/100.0,step)]

        print(f'X={X}')
        # quit()

        for x in X:
            injs.append(x)

            try:
                lat = inj_data_dict[x]
            except:
                lat = 10000000000

            lats.append(lat)



        # small
        size = 0
        if '_m_' in config:
            size = 1
        elif 'ft_x' in config:
            size = 1
        elif 'med' in config:
            size = 1
        elif '_l_' in config:
            size = 2
        elif 'dbl' in config or 'butt' in config:
            size = 2
        elif 'large' in config:
            size = 2
        elif '2ll' in config:
            size = 1
        elif '25ll' in config:
            size = 2

        print(f'{config} : size={size}')


        # print(f'before ns adjust:\n\tX={X}')



        # # convert cycles of cpu to ns
        # sys_clk = 4
        # X = [2*convert(x,sys_clk) for x in X]

        # print(f'after ns adjust:\n\tX={X}')



        # size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}

        # clk_adjustment = size_to_freq[size] / sys_clk

        # X = [clk_adjustment*x for x in X]

        # print(f'after noi clk adjust:\n\tX={X}')


        max_x = max(X)

        # input('good?')

        # for ir, pl in inj_data_dict.items():
            # print(f'\t\t{ir} : {pl}')



            # injs.append(ir)
            # lats.append(pl)



        new_name = rename_dict[config]
        mylabels.append(new_name)
        mark = topo_to_marker[config]
        col = color_dict[new_name]




        print(f'before ns adjust:\n\injs={injs}')

        # convert cycles of cpu to ns
        sys_clk = 4
        injs = [2*convert(x,sys_clk) for x in injs]

        print(f'after ns adjust:\n\injs={injs}')



        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        injs = [clk_adjustment*x for x in injs]


        injs = [round(x,3) for x in injs]

        print(f'after noi clk adjust:\n\injs={injs}')



        ############3
        print(f'before ns adjust:\n\injs={injs}')

        # convert cycles of cpu to ns
        sys_clk = 4
        # lats = [2*convert(x,sys_clk) for x in lats]

        print(f'after ns adjust:\n\lats={lats}')


        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        lats = [x/clk_adjustment for x in lats]

        lats = [round(l,3) for l in lats]
        print(f'after noi clk adjust:\n\lats={lats}')


        sorted_lats = [x for _,x in sorted(zip(injs,lats))]
        sorted_injs= [x for x,_ in sorted(zip(injs,lats))]

        # print(f'plotting {sorted_injs} : {sorted_lats}')
        # print(f'plotting {sorted_injs} v {sorted_lats}')
        print(f'topology : {new_name}')
        for i, injr in enumerate(sorted_injs):
            print(f'\t{injr:5} : {sorted_lats[i]}')

        # input('good?')

        # plt.plot(injs, lats, label=new_name,linestyle='--',marker=mark, markersize=5,color=col)

        is_ns = False
        if 'NS' in new_name:
            is_ns = True

        msize = 5
        if not is_ns:
            msize = 6

        axes[size].plot(sorted_injs, sorted_lats, label=new_name,linestyle='--',marker=mark, markersize=msize,color=col)

    # print(f'my_labels={mylabels}')
    # quit()

    y = np.arange(0.0,36,10)
    y_minor = np.arange(0.0,35,5)

    for ax in axes:
        ax.set_yticks(y)
        ax.set_yticks(y_minor,minor=True)






    xticks = np.arange(0,1.5,.1)
    xticks_min = np.arange(0,1.5,.05)

    # convert cycles of cpu to ns
    # sys_clk = 4
    # xticks = [2*convert(x,sys_clk) for x in xticks]

    # size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
    # clk_adjustment = size_to_freq[size] / sys_clk
    # xticks = [clk_adjustment*x for x in xticks]

    # xticks_min = [2*convert(x,sys_clk) for x in xticks_min]

    # size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
    # clk_adjustment = size_to_freq[size] / sys_clk
    # xticks_min = [clk_adjustment*x for x in xticks_min]


    # axes[2].set_xticks(x)
    # axes[2].set_xticks(xmin,minor=True)

    # coh
    if param_mem_or_coh == 'coh':
        max_x = 1.175

    # mem
    else:
        max_x = 0.9


    max_y = 30.0

    if MAX_Y is not None:
        max_y = MAX_Y

    for ax in axes:

        ax.set_xticks(xticks)
        ax.set_xticks(xticks_min,minor=True)

        # plt.grid(which='major',alpha=0.5)
        # plt.grid(which='minor',alpha=0.2)
        # plt.ylim([6, 22.5])
        # plt.xlim([0.0, 0.18])
        ax.grid(which='major',alpha=0.5)
        ax.grid(which='minor',alpha=0.2)
        ax.set_ylim([0, max_y ])
        ax.set_xlim([0.0, max_x])

    axes[1].set_xticklabels([])
    axes[0].set_xticklabels([])

    # axes[2].set_xlabel("Injection Rate  (pkts/cpu/cycle)")
    axes[2].set_xlabel("Injection Rate  (pkts/cpu/ns)")

    axes[1].set_ylabel("Avg. Pkt. Latency (ns)")
    # plt.grid()

    twins = []
    for ax in axes:
        twins.append(ax.twinx())

    twins[0].set_ylabel('Small')
    twins[1].set_ylabel('Medium')
    twins[2].set_ylabel('Large')
    twins[0].set_yticklabels([])
    twins[1].set_yticklabels([])
    twins[2].set_yticklabels([])

    labels = []
    handles = []
    for ax in axes:
        _handles, _labels = ax.get_legend_handles_labels()
        for h in _handles:
            handles.append(h)
        for l in _labels:

            l = l.replace(' Large','')
            l = l.replace(' Med','')
            l = l.replace(' Small','')

            labels.append(l)



    # handles, labels = ax.get_legend_handles_labels()

    proxy0 = plt.plot([],[],color='none',label=' ')
    proxy7 = plt.plot([],[],color='none',label=' ')
    proxy14 = plt.plot([],[],color='none',label=' ')

    # proxy8 = plt.plot([],[],color='none',label=' ')
    # proxy9 = plt.plot([],[],color='none',label=' ')


    handles.insert(0,proxy0[0])
    handles.insert(6,proxy7[0])
    handles.insert(12,proxy14[0])
    # handles.insert(7,proxy7[0])
    # handles.insert(14,proxy14[0])

    # handles.insert(4,proxy4[0])
    # handles.insert(8,proxy8[0])
    # handles.insert(9,proxy9[0])
    # # print(proxy3)

    # # print(handles)
    # # quit()

    if use_latex_legend:
        labels.insert(0,r'\underline{Small}')
        labels.insert(6,r'\underline{Medium}')
        labels.insert(12,r'\underline{Large}')
    else:
        labels.insert(0,'Small')
        labels.insert(6,'Medium')
        labels.insert(12,'Large')


    # # handles, labels = ax.get_legend_handles_labels()

    # proxy0 = plt.plot([],[],color='none',label=' ')
    # proxy6 = plt.plot([],[],color='none',label=' ')
    # proxy12 = plt.plot([],[],color='none',label=' ')

    # # proxy8 = plt.plot([],[],color='none',label=' ')
    # # proxy9 = plt.plot([],[],color='none',label=' ')


    # handles.insert(0,proxy0[0])
    # handles.insert(6,proxy6[0])
    # handles.insert(12,proxy12[0])

    # # handles.insert(4,proxy4[0])
    # # handles.insert(8,proxy8[0])
    # # handles.insert(9,proxy9[0])
    # # # print(proxy3)

    # # # print(handles)
    # # # quit()

    # labels.insert(0,r'\underline{Small}')
    # labels.insert(6,r'\underline{Medium}')
    # labels.insert(12,r'\underline{Large}')

    # labels.insert(4,' ')
    # labels.insert(8,' ')
    # labels.insert(9,' ')



    # plt.legend(mylabels,ncol=3, bbox_to_anchor=(-0.1, 1.0, 1., .102), loc='lower left')


    print(f'handles={handles}')
    print(f'labels={labels}')

    if param_mem_or_coh == 'coh':
        axes[0].legend(handles, labels,ncol=3,bbox_to_anchor=(-0.04, 0.94, 0.2, 0.1), loc='lower left', )


    name = f'./synth_outputs/graphs/simple_20r_{param_mem_or_coh}_{param_alg}_freqadjusted.png'
    plt.savefig(name,bbox_inches='tight',dpi=DPI)
    # plt.savefig(name,bbox_inches='tight')
    if use_input:
        input(f'wrote to {name}')

    plt.show()

def gen_synth_48r_3subplots(infile_name='./synth_outputs/simple_2b.csv', param_mem_or_coh='coh',param_alg='cload',traf='uniform'):

    print(f'reading from {infile_name}')
    # input('press any key')

    data = {}
    configs = []

    with open(infile_name, 'r') as inf:
        csv_inf = csv.reader(inf)

        headers = []

        time_axis = []

        for line in csv_inf:

            if len(headers) == 0:
                headers = line
                continue

            if '' in line:
                line.remove('')

            # if 'coh' in line:
            #     continue


            print(f'{line}')
            # quit()


            mem_or_coh = line[2]
            config = line[4]
            alg = line[3]

            # new order
            config = line[3]
            alg = line[4]

            # if 'latop' in config:
            #     continue

            config = config.replace('_48r_4p','')
            try:
                config = custom_rename[config]
            except:
                pass
            # # print(f'config={config}')


            # if 'shuffle_ulinks' in config:
            #     if '15ll' in config:
            #         config = 'ns_s_latop'
            #     elif '2ll' in config:
            #         config = 'ns_m_latop'
            #     elif '25ll' in config:
            #         config = 'ns_l_latop'

            # input(f'config={config}')

            # if param_alg not in alg:
            #     print(f'{param_alg} not in {alg}')
            #     continue


            inj_rate_str = line[5]
            # inj_rate_str = line[4]

            try:
                pkt_lat_str = line[6]
                # pkt_lat_str = line[5]
            except:
                pkt_lat_str = '100000000.0'
                # pkt_lat_str = '0'

            configs.append(config)

            # input(f'len(inj_rate_str.split("_")[-1]) = {len(inj_rate_str.split("_")[-1])}')

            # # hotfix
            # if len(inj_rate_str) == 3:
            #     inj_rate_str = inj_rate_str + '0'

            inj_rate = float(inj_rate_str.split('_')[-1])


            # input(f'raw = {inj_rate}')

            factor = 10000


            # factor = 10
            if len(inj_rate_str.split('_')[-1]) == 2:
                # input(f'odd')
                factor = 100
            if len(inj_rate_str.split('_')[-1]) == 3:
                # input(f'odd')
                factor = 1000



            inj_rate = inj_rate / factor

            # input(f'inj_rate = {inj_rate} correct?')

            # parse and convert to ns
            pkt_lat = float(pkt_lat_str) / 1000.0

            # init
            try:
                _ = data[mem_or_coh]
            except:
                data.update({mem_or_coh : {} })

            try:
                _ = data[mem_or_coh][config]
            except:
                data[mem_or_coh].update({config : {}})

            data[mem_or_coh][config].update({inj_rate : pkt_lat})


    # quit()


    for memcoh, config_data_dict in data.items():
        if memcoh == 'mem':
            continue
        print(f'{memcoh}')
        for config,inj_data_dict in config_data_dict.items():
            print(f'\t{config}')
            for ir, pl in inj_data_dict.items():
                print(f'\t\t{ir} : {pl}')

    ######################################################################################

    plt.cla()
    # plt.clear()
    plt.rc('font', size=16) #controls default text size
    plt.rc('axes', titlesize=14) #fontsize of the title
    plt.rc('axes', labelsize=14) #fontsize of the x and y labels
    plt.rc('xtick', labelsize=10) #fontsize of the x tick labels
    plt.rc('ytick', labelsize=10) #fontsize of the y tick labels
    plt.rc('legend', fontsize=14)


    if use_latex_legend:
        plt.rc('text', usetex=True)

    fig = plt.figure(figsize=(7,4))

    axes = []
    axes.append(fig.add_subplot(3,1,1))
    axes.append(fig.add_subplot(3,1,2))
    axes.append(fig.add_subplot(3,1,3))



    # for memcoh, config_data_dict in data.items():
    #     print(f'{memcoh}')
    #     for config,inj_data_dict in config_data_dict.items():
    #         print(f'\t{config}')
    #         for ir, pl in inj_data_dict.items():
    #             print(f'\t\t{ir} : {pl}')


    config_data_dict = data[param_mem_or_coh]
    # for config,inj_data_dict in config_data_dict.items():
    #     if config not in desired_topologies:
    #         print(f'config {config} not in desired {desired_topologies}')
    #         continue

    mylabels = []


    for config in desired_topologies:
        try:
            inj_data_dict = config_data_dict[config]
        except:
            continue
        # print(f'\t{config}')
        injs = []
        lats = []

        max_val = len(inj_data_dict)

        # print(f'max_val={max_val}')
        # quit()

        # if MAX_VAL is not None:
        #     max_val = MAX_VAL

        # print(f'({len(inj_data_dict)}) {inj_data_dict}')
        # quit()

        # X = [i/100.0 for i in range(1,max_val+1)]
        # X = [i/100.0 for i in range(1,max_val+1)]

        max_val = 8

        step = 0.0025

        X = [round(x,4) for x in np.arange(0.0025,0.08,step)]

        print(f'X={X}')
        # quit()

        for x in X:
            injs.append(x)

            print(f'trying inj_data_dict[{x}] ')

            try:
                lat = inj_data_dict[x]
                print(f'got inj_data_dict[x] = {inj_data_dict[x]}')
            except:
                lat = 10000000000

            lats.append(lat)

        max_x = max(X)

        # for ir, pl in inj_data_dict.items():
            # print(f'\t\t{ir} : {pl}')



            # injs.append(ir)
            # lats.append(pl)

        # small
        size = 0
        if '_m_' in config:
            size = 1
        elif 'ft_x' in config:
            size = 1
        elif 'med' in config:
            size = 1
        elif '_l_' in config:
            size = 2
        elif 'dbl' in config or 'butt' in config:
            size = 2
        elif 'large' in config:
            size = 2
        elif '2ll' in config:
            size = 1
        elif '25ll' in config:
            size = 2

        print(f'{config} : size={size}')


        new_name = rename_dict[config]
        mylabels.append(new_name)
        mark = topo_to_marker[config]
        col = color_dict[new_name]



        print(f'before ns adjust:\n\injs={injs}')


        # TODO uncomment
        # convert cycles of cpu to ns
        sys_clk = 4
        injs = [2*convert(x,sys_clk) for x in injs]

        print(f'after ns adjust:\n\injs={injs}')



        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        injs = [clk_adjustment*x for x in injs]


        injs = [round(x,3) for x in injs]

        print(f'after noi clk adjust:\n\injs={injs}')

        # end uncomment

        ############3
        print(f'before ns adjust:\n\injs={injs}')

        # convert cycles of cpu to ns
        sys_clk = 4
        # lats = [2*convert(x,sys_clk) for x in lats]

        print(f'after ns adjust:\n\lats={lats}')


        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        lats = [x/clk_adjustment for x in lats]

        lats = [round(l,3) for l in lats]
        print(f'after noi clk adjust:\n\lats={lats}')




        sorted_lats = [x for _,x in sorted(zip(injs,lats))]
        sorted_injs= [x for x,_ in sorted(zip(injs,lats))]


        # print(f'plotting {sorted_injs} : {sorted_lats}')
        # print(f'plotting {sorted(zip(injs,lats))}')
        # print(f'new_name={new_name}')
        # input(f'plotting {sorted(zip(injs,lats))}')


        # plt.plot(injs, lats, label=new_name,linestyle='--',marker=mark, markersize=5,color=col)

        is_ns = False
        if 'NS' in new_name:
            is_ns = True

        msize = 5
        if not is_ns:
            msize = 6

        axes[size].plot(sorted_injs, sorted_lats, label=new_name,linestyle='--',marker=mark, markersize=msize,color=col)

    # print(f'my_labels={mylabels}')
    # quit()

    y = np.arange(0.0,40,10)
    y_minor = np.arange(0.0,35,5)

    for ax in axes:
        ax.set_yticks(y)
        ax.set_yticks(y_minor,minor=True)





    xticks = np.arange(0,1.5,.1)
    xticks_min = np.arange(0,1.5,.025)

    # axes[2].set_xticks(x)
    # axes[2].set_xticks(xmin,minor=True)




    max_x = 0.525
    max_y = 35.0

    # if MAX_Y is not None:
    #     max_y = MAX_Y

    for ax in axes:

        ax.set_xticks(xticks)
        ax.set_xticks(xticks_min,minor=True)

        # plt.grid(which='major',alpha=0.5)
        # plt.grid(which='minor',alpha=0.2)
        # plt.ylim([6, 22.5])
        # plt.xlim([0.0, 0.18])
        ax.grid(which='major',alpha=0.5)
        ax.grid(which='minor',alpha=0.2)
        ax.set_ylim([0, max_y ])
        ax.set_xlim([0.0, max_x])

    axes[1].set_xticklabels([])
    axes[0].set_xticklabels([])

    axes[2].set_xlabel("Injection Rate  (pkts/cpu/ns)")

    axes[1].set_ylabel("Avg. Pkt. Latency (ns)")

    twins = []
    for ax in axes:
        twins.append(ax.twinx())

    twins[0].set_ylabel('Small')
    twins[1].set_ylabel('Medium')
    twins[2].set_ylabel('Large')
    twins[0].set_yticklabels([])
    twins[1].set_yticklabels([])
    twins[2].set_yticklabels([])

    labels = []
    handles = []
    for ax in axes:
        _handles, _labels = ax.get_legend_handles_labels()
        for h in _handles:
            handles.append(h)
        for l in _labels:

            l = l.replace(' Large','')
            l = l.replace(' Med','')
            l = l.replace(' Small','')


            labels.append(l)



    # handles, labels = ax.get_legend_handles_labels()

    proxy0 = plt.plot([],[],color='none',label=' ')
    proxy7 = plt.plot([],[],color='none',label=' ')
    proxy14 = plt.plot([],[],color='none',label=' ')
    proxy_a = plt.plot([],[],color='none',label=' ')

    proxy8 = plt.plot([],[],color='none',label=' ')
    # proxy9 = plt.plot([],[],color='none',label=' ')


    handles.insert(0,proxy0[0])
    handles.insert(3,proxy7[0])
    handles.insert(4,proxy8[0])

    handles.insert(8,proxy14[0])
    # handles.insert(7,proxy7[0])
    # handles.insert(14,proxy14[0])

    # handles.insert(4,proxy4[0])
    # handles.insert(8,proxy8[0])
    # handles.insert(9,proxy9[0])
    # # print(proxy3)

    # # print(handles)
    # # quit()

    if use_latex_legend:
        labels.insert(0,r'\underline{Small}')
        labels.insert(4,r'\underline{Medium}')
        labels.insert(8,r'\underline{Large}')
    else:
        labels.insert(0,'Large')
        labels.insert(4,'Medium')
        labels.insert(8,'Large')
    
    labels.insert(3,' ')


    # labels.insert(7,r'\underline{Medium}')
    # labels.insert(14,r'\underline{Large}')

    # # handles, labels = ax.get_legend_handles_labels()

    # proxy0 = plt.plot([],[],color='none',label=' ')
    # proxy6 = plt.plot([],[],color='none',label=' ')
    # proxy12 = plt.plot([],[],color='none',label=' ')

    # # proxy8 = plt.plot([],[],color='none',label=' ')
    # # proxy9 = plt.plot([],[],color='none',label=' ')


    # handles.insert(0,proxy0[0])
    # handles.insert(6,proxy6[0])
    # handles.insert(12,proxy12[0])

    # # handles.insert(4,proxy4[0])
    # # handles.insert(8,proxy8[0])
    # # handles.insert(9,proxy9[0])
    # # # print(proxy3)

    # # # print(handles)
    # # # quit()

    # labels.insert(0,r'\underline{Small}')
    # labels.insert(6,r'\underline{Medium}')
    # labels.insert(12,r'\underline{Large}')

    # labels.insert(4,' ')
    # labels.insert(8,' ')
    # labels.insert(9,' ')



    # plt.legend(mylabels,ncol=3, bbox_to_anchor=(-0.1, 1.0, 1., .102), loc='lower left')


    print(f'handles={handles}')
    print(f'labels={labels}')

    if param_mem_or_coh == 'coh':
        axes[0].legend(handles, labels,ncol=3,bbox_to_anchor=(-0.02, 0.94, 0.2, 0.1), loc='lower left', )


    name = f'./synth_outputs/graphs/48r_{param_mem_or_coh}_{param_alg}'

    if traf != 'uniform':
        name += f'_{traf}'

    name += '_freqadjusted'


    name += '.png'

    # input(f'out_name = {name}')

    plt.savefig(name,bbox_inches='tight',dpi=DPI)
    # plt.savefig(name,bbox_inches='tight')
    if use_input:
        input(f'wrote to {name}')

    plt.show()


# FLAG
def gen_synth_64r_3subplots(infile_name='./synth_outputs/simple_2b.csv', param_mem_or_coh='coh',param_alg='cload',traf='uniform'):

    print(f'reading from {infile_name}')
    # input('press any key')

    data = {}
    configs = []

    with open(infile_name, 'r') as inf:
        csv_inf = csv.reader(inf)

        headers = []

        time_axis = []

        for line in csv_inf:

            if len(headers) == 0:
                headers = line
                continue

            if '' in line:
                line.remove('')

            # if 'coh' in line:
            #     continue


            print(f'{line}')
            # quit()


            mem_or_coh = line[2]
            config = line[3]
            alg = line[4]

            # if 'latop' in config:
            #     continue

            config = config.replace('_64r','')
            try:
                config = custom_rename[config]
            except:
                pass
            print(f'config={config}')


            inj_rate_str = line[5]
            # inj_rate_str = line[4]

            try:
                pkt_lat_str = line[6]
                flit_lat_str = line[7]
            except:
                pkt_lat_str = '100000000.0'
                flit_lat_str = '100000000.0'
                # pkt_lat_str = '0'

            configs.append(config)

            # input(f'len(inj_rate_str.split("_")[-1]) = {len(inj_rate_str.split("_")[-1])}')

            # # hotfix
            # if len(inj_rate_str) == 3:
            #     inj_rate_str = inj_rate_str + '0'

            inj_rate = float(inj_rate_str.split('_')[-1])


            # input(f'raw = {inj_rate}')

            factor = 10


            # factor = 10
            if len(inj_rate_str.split('_')[-1]) == 2:
                # input(f'odd')
                factor = 100
            if len(inj_rate_str.split('_')[-1]) == 3:
                # input(f'odd')
                factor = 1000



            inj_rate = inj_rate / factor

            # input(f'inj_rate = {inj_rate} correct?')

            # parse and convert to ns
            pkt_lat = float(pkt_lat_str) / 1000.0

            # init
            try:
                _ = data[mem_or_coh]
            except:
                data.update({mem_or_coh : {} })

            try:
                _ = data[mem_or_coh][config]
            except:
                data[mem_or_coh].update({config : {}})

            data[mem_or_coh][config].update({inj_rate : pkt_lat})


    # quit()


    for memcoh, config_data_dict in data.items():
        if memcoh == 'mem':
            continue
        print(f'{memcoh}')
        for config,inj_data_dict in config_data_dict.items():
            print(f'\t{config}')
            for ir, pl in inj_data_dict.items():
                print(f'\t\t{ir} : {pl}')

    ######################################################################################

    plt.cla()
    # plt.clear()
    plt.rc('font', size=16) #controls default text size
    plt.rc('axes', titlesize=14) #fontsize of the title
    plt.rc('axes', labelsize=14) #fontsize of the x and y labels
    plt.rc('xtick', labelsize=10) #fontsize of the x tick labels
    plt.rc('ytick', labelsize=10) #fontsize of the y tick labels
    plt.rc('legend', fontsize=14)

    if use_latex_legend:
        plt.rc('text', usetex=True)

    fig = plt.figure(figsize=(7,4))

    axes = []
    axes.append(fig.add_subplot(3,1,1))
    axes.append(fig.add_subplot(3,1,2))
    axes.append(fig.add_subplot(3,1,3))



    # for memcoh, config_data_dict in data.items():
    #     print(f'{memcoh}')
    #     for config,inj_data_dict in config_data_dict.items():
    #         print(f'\t{config}')
    #         for ir, pl in inj_data_dict.items():
    #             print(f'\t\t{ir} : {pl}')


    config_data_dict = data[param_mem_or_coh]
    # for config,inj_data_dict in config_data_dict.items():
    #     if config not in desired_topologies:
    #         print(f'config {config} not in desired {desired_topologies}')
    #         continue

    mylabels = []


    for config in desired_topologies_64r:

        print(f'config={config}')

        try:
            inj_data_dict = config_data_dict[config]
        except:
            continue
        # print(f'\t{config}')
        injs = []
        lats = []

        max_val = len(inj_data_dict)

        # print(f'max_val={max_val}')
        # quit()

        # if MAX_VAL is not None:
        #     max_val = MAX_VAL

        # print(f'({len(inj_data_dict)}) {inj_data_dict}')
        # quit()

        # X = [i/100.0 for i in range(1,max_val+1)]
        # X = [i/100.0 for i in range(1,max_val+1)]

        max_val = 8

        step = 0.0025
        step = 0.01

        X = [round(x,4) for x in np.arange(step,0.3,step)]

        print(f'X={X}')
        # quit()

        for x in X:
            injs.append(x)

            print(f'trying inj_data_dict[{x}] ')

            try:
                lat = inj_data_dict[x]
                print(f'got inj_data_dict[x] = {inj_data_dict[x]}')
            except:
                lat = 10000000000

            lats.append(lat)

        max_x = max(X)

        # for ir, pl in inj_data_dict.items():
            # print(f'\t\t{ir} : {pl}')



            # injs.append(ir)
            # lats.append(pl)

        # small
        size = 0
        if '_m_' in config:
            size = 1
        elif 'ft_x' in config:
            size = 1
        elif 'med' in config:
            size = 1
        elif '_l_' in config:
            size = 2
        elif 'dbl' in config or 'butt' in config:
            size = 2
        elif 'large' in config:
            size = 2
        elif '2ll' in config:
            size = 1
        elif '25ll' in config:
            size = 2

        print(f'{config} : size={size}')


        new_name = rename_dict[config]
        mylabels.append(new_name)
        mark = topo_to_marker[config]
        col = color_dict[new_name]



        print(f'before ns adjust:\n\injs={injs}')


        # TODO uncomment
        # convert cycles of cpu to ns
        sys_clk = 4
        injs = [2*convert(x,sys_clk) for x in injs]

        print(f'after ns adjust:\n\injs={injs}')



        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        injs = [clk_adjustment*x for x in injs]


        injs = [round(x,3) for x in injs]

        print(f'after noi clk adjust:\n\injs={injs}')

        # end uncomment

        ############3
        print(f'before ns adjust:\n\injs={injs}')

        # convert cycles of cpu to ns
        sys_clk = 4
        # lats = [2*convert(x,sys_clk) for x in lats]

        print(f'after ns adjust:\n\lats={lats}')


        size_to_freq = {0 : 3.6, 1: 3.0, 2:2.7}
        clk_adjustment = size_to_freq[size] / sys_clk

        lats = [x/clk_adjustment for x in lats]

        lats = [round(l,3) for l in lats]
        print(f'after noi clk adjust:\n\lats={lats}')




        sorted_lats = [x for _,x in sorted(zip(injs,lats))]
        sorted_injs= [x for x,_ in sorted(zip(injs,lats))]


        # print(f'plotting {sorted_injs} : {sorted_lats}')
        # # print(f'plotting {sorted(zip(injs,lats))}')
        # print(f'new_name={new_name}')
        # input(f'plotting {sorted(zip(injs,lats))}')


        # plt.plot(injs, lats, label=new_name,linestyle='--',marker=mark, markersize=5,color=col)

        is_ns = False
        if 'NS' in new_name:
            is_ns = True

        msize = 5
        if not is_ns:
            msize = 6

        axes[size].plot(sorted_injs, sorted_lats, label=new_name,linestyle='--',marker=mark, markersize=msize,color=col)

    # print(f'my_labels={mylabels}')
    # quit()

    y = np.arange(0.0,40,10)
    y_minor = np.arange(0.0,35,5)

    for ax in axes:
        ax.set_yticks(y)
        ax.set_yticks(y_minor,minor=True)





    xticks = np.arange(0,1.5,.1)
    xticks_min = np.arange(0,1.5,.025)

    # axes[2].set_xticks(x)
    # axes[2].set_xticks(xmin,minor=True)




    max_x = 1.125
    max_y = 35.0

    # if MAX_Y is not None:
    #     max_y = MAX_Y

    for ax in axes:

        ax.set_xticks(xticks)
        ax.set_xticks(xticks_min,minor=True)

        # plt.grid(which='major',alpha=0.5)
        # plt.grid(which='minor',alpha=0.2)
        # plt.ylim([6, 22.5])
        # plt.xlim([0.0, 0.18])
        ax.grid(which='major',alpha=0.5)
        ax.grid(which='minor',alpha=0.2)
        ax.set_ylim([0, max_y ])
        ax.set_xlim([0.0, max_x])

    axes[1].set_xticklabels([])
    axes[0].set_xticklabels([])

    axes[2].set_xlabel("Injection Rate  (pkts/cpu/ns)")

    axes[1].set_ylabel("Avg. Pkt. Latency (ns)")

    twins = []
    for ax in axes:
        twins.append(ax.twinx())

    twins[0].set_ylabel('Small')
    twins[1].set_ylabel('Medium')
    twins[2].set_ylabel('Large')
    twins[0].set_yticklabels([])
    twins[1].set_yticklabels([])
    twins[2].set_yticklabels([])

    labels = []
    handles = []
    for ax in axes:
        _handles, _labels = ax.get_legend_handles_labels()
        for h in _handles:
            handles.append(h)
        for l in _labels:

            l = l.replace(' Large','')
            l = l.replace(' Med','')
            l = l.replace(' Small','')


            labels.append(l)



    # handles, labels = ax.get_legend_handles_labels()

    proxy0 = plt.plot([],[],color='none',label=' ')
    proxy7 = plt.plot([],[],color='none',label=' ')
    proxy14 = plt.plot([],[],color='none',label=' ')
    proxy_a = plt.plot([],[],color='none',label=' ')

    proxy8 = plt.plot([],[],color='none',label=' ')
    # proxy9 = plt.plot([],[],color='none',label=' ')


    handles.insert(0,proxy0[0])
    handles.insert(3,proxy7[0])
    handles.insert(4,proxy8[0])

    handles.insert(8,proxy14[0])
    # handles.insert(7,proxy7[0])
    # handles.insert(14,proxy14[0])

    # handles.insert(4,proxy4[0])
    # handles.insert(8,proxy8[0])
    # handles.insert(9,proxy9[0])
    # # print(proxy3)

    # # print(handles)
    # # quit()

    if use_latex_legend:
        labels.insert(0,r'\underline{Small}')
        labels.insert(4,r'\underline{Medium}')
        labels.insert(8,r'\underline{Large}')
    else:
        labels.insert(0,'Small')
        labels.insert(4,'Medium')
        labels.insert(8,'Large')

    labels.insert(3,' ')

    # labels.insert(7,r'\underline{Medium}')
    # labels.insert(14,r'\underline{Large}')

    # # handles, labels = ax.get_legend_handles_labels()

    # proxy0 = plt.plot([],[],color='none',label=' ')
    # proxy6 = plt.plot([],[],color='none',label=' ')
    # proxy12 = plt.plot([],[],color='none',label=' ')

    # # proxy8 = plt.plot([],[],color='none',label=' ')
    # # proxy9 = plt.plot([],[],color='none',label=' ')


    # handles.insert(0,proxy0[0])
    # handles.insert(6,proxy6[0])
    # handles.insert(12,proxy12[0])

    # # handles.insert(4,proxy4[0])
    # # handles.insert(8,proxy8[0])
    # # handles.insert(9,proxy9[0])
    # # # print(proxy3)

    # # # print(handles)
    # # # quit()

    # labels.insert(0,r'\underline{Small}')
    # labels.insert(6,r'\underline{Medium}')
    # labels.insert(12,r'\underline{Large}')

    # labels.insert(4,' ')
    # labels.insert(8,' ')
    # labels.insert(9,' ')



    # plt.legend(mylabels,ncol=3, bbox_to_anchor=(-0.1, 1.0, 1., .102), loc='lower left')


    print(f'handles={handles}')
    print(f'labels={labels}')

    if param_mem_or_coh == 'coh':
        axes[0].legend(handles, labels,ncol=3,bbox_to_anchor=(-0.02, 0.94, 0.2, 0.1), loc='lower left', )


    name = f'./synth_outputs/graphs/48r_{param_mem_or_coh}_{param_alg}'

    if traf != 'uniform':
        name += f'_{traf}'

    name += '_freqadjusted'


    name += '.png'

    # input(f'out_name = {name}')

    plt.savefig(name,bbox_inches='tight',dpi=DPI)
    # plt.savefig(name,bbox_inches='tight')
    if use_input:
        input(f'wrote to {name}')

    plt.show()




def main():

    try:
        memcoh = sys.argv[3]
    except:
        memcoh ='coh'

    try:
        alg = sys.argv[2]

    except:
        alg = 'naive'


    try:
        traf = sys.argv[4]

    except:
        traf = 'uniform'


    try:
        in_name = sys.argv[1]
    except:
        pass

    try:
        n_routers = int(sys.argv[5])
    except:
        n_routers = 20

    print(f'sys.argv={sys.argv}')

    # file_20r = 'synth_outputs/csvs/simple_compare_nndbt_prev_mclb_ours_same_4GHz_20nov.csv'
    # alg_20r = 'compare_nndbt_prev_mclb_ours_same_4GHz_22feb24'

    # gen_synth_20r_3subplots(infile_name = file_20r, param_mem_or_coh=memcoh, param_alg=alg_20r)

    # file_shuf = 'synth_outputs/csvs/simple_2b_mixed_shuffle_shuffletopos_mclb_hops_4_6_both_40cpu_4xdir_4GHz_005gran.csv'
    # alg_shuf = 'simple_2b_mixed_shuffle_shuffletopos_mclb_hops_4_6_both_40cpu_4xdir_4GHz'
    # gen_synth_20r_3subplots_shuffle(infile_name = file_shuf, param_mem_or_coh=memcoh, param_alg=alg_shuf)

    # file_48r = 'synth_outputs/csvs/48r_2b_mixed_uniform_mclbandnndbt_6_8_96cpus_2xdirs_4.0GHz_0025gran.csv'
    # alg_48r = 'mclbandnndbt_6_8_96cpus_2xdirs_4.0GHz'
    # gen_synth_48r_3subplots(infile_name = file_48r, param_mem_or_coh=memcoh, param_alg=alg_48r)

    if n_routers == 64:
        gen_synth_64r_3subplots(infile_name = file_64r, param_mem_or_coh='coh', param_alg=alg_64r)
    # gen_synth_64r_3subplots(infile_name = file_64r, param_mem_or_coh='mem', param_alg=alg_64r)

    if n_routers == 20:
        gen_synth_20r_3subplots(infile_name = in_name, param_mem_or_coh=memcoh, param_alg=alg)



    # gen_synth_20r_3subplots_shuffle(infile_name = in_name, param_mem_or_coh=memcoh, param_alg=alg)
    # gen_synth_48r_3subplots(infile_name = in_name, param_mem_or_coh=memcoh, param_alg=alg)

    # try:

    #     # gen_synth_30r_3subplots(infile_name=in_name,param_mem_or_coh=memcoh)
    # except:
    #     gen_synth_20r_3subplots(param_mem_or_coh=memcoh)
    #     # gen_synth_30r_3subplots(param_mem_or_coh=memcoh)


    # gen_synth_20r_coh(infile_name = in_name)

    # gen_synth_30r_mem()
    #gen_synth_30r()


if __name__ == '__main__':
    main()
