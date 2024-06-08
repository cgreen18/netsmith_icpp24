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


import os
import subprocess
import sys
import threading
import argparse
import numpy as np


MAX_PROCS = 28

global num_threads
num_threads = 0

sem = threading.Semaphore(MAX_PROCS)

global config_status
config_status = {}

status_lock = threading.Lock()

# TODO change
home = '/home/min/a/green456/netsmith_icpp24/auto_top_gem5'

home = os.getcwd()
# setup = ['cd', home, ';', 'module','load','gcc',';']
setup = ['module','load','gcc',';']
gem5_build = './build/Garnet_standalone/gem5.fast'
conf_script = 'configs/netsmith/netsmith_synth.py'
topo_conf_script = 'EscapeVirtualNetworks'
topology_to_n_routers_dict = {
    'cmesh_x':'20',
    'butter_donut_x':'20',
    'kite_large':'20',
    'kite_medium':'20',
    'ft_x':'20',
    'kite_small':'20',
    'cmesh':'24',
    'dbl_bfly':'24',
    'dbl_bfly_x':'20',
    'mesh':'64',
    'ns':'20',
    'lpbt':'20'}


sim_cycles = ['2147483647']
inj_rates = [str(x/100.0) for x in range(1, 11)]


# topologies
noi_clks_dict = {'mesh':'4GHz',
            'cmesh':'3.6GHz',
            'cmesh_x':'3.6GHz',
            'dbl_bfly':'2.7GHz',
            'dbl_bfly_x':'2.7GHz',
            'butter_donut_x':'2.7GHz',
            'kite_small':'3.6GHz',
            'kite_medium':'3.0GHz',
            'ft_x':'3.0GHz',
            'kite_large':'2.7GHz',
            # these will match part of name of our files
            '15ll':'3.6GHz',
            '2ll':'3.0GHz',
            '25ll':'2.7GHz',
            'ns_s_latop':'3.6GHz',
            'ns_s_bwop':'3.6GHz',
            'ns_m_latop':'3.0GHz',
            'ns_m_bwop':'3.0GHz',
            'ns_l_latop':'2.7GHz',
            'ns_l_bwop':'2.7GHz',
            'ns_s_latop_noci':'3.6GHz',
            'ns_s_bwop_noci':'3.6GHz',
            'ns_m_latop_noci':'3.0GHz',
            'ns_m_bwop_noci':'3.0GHz',
            'ns_l_latop_noci':'2.7GHz',
            'ns_l_bwop_noci':'2.7GHz',
            '20r_4p_15ll_runsol_scbw':'3.6GHz',
            '20r_4p_2ll_runsol_scbw':'3.0GHz',
            '20r_4p_25ll_runsol_scbw':'2.7GHz',
            'ns_s_scop':'3.6GHz',
            'ns_m_scop':'3.0GHz',
            'ns_l_scop':'2.7GHz',
            'dbl_bfly_x_noci':'2.7GHz',
            'butter_donut_x_noci':'2.7GHz',
            'kite_small_noci':'3.6GHz',
            'kite_medium_noci':'3.0GHz',
            'kite_large_noci':'2.7GHz',
            'ft_x_noci':'3.0GHz',
            'lpbt_s_hops':'3.6GHz',
            'lpbt_s_power':'3.6GHz',
            'lpbt_m_hops':'3.0GHz',
            's':'3.6GHz',
            'm':'3.0GHz',
            'l':'2.7GHz',
            'mesh_noci':'4.0GHz'}


global map_files
map_files = []


base_flags = ['--network','garnet',
        '--mem-type', 'SimpleMemory',
        #'--garnet-deadlock-threshold','50000000',
        '--routing-algorithm', '2',
        '--use_escape_vns',
        # '--vcs-per-vnet','6',
        # '--evn_deadlock_partition','2',
        # '--evn_n_deadlock_free','1',
        # '--evn_min_n_deadlock_free','4',
        '--synth_traffic',

        # allows non power of two # of directories
        # '--mem_size','536870900'
        ]


global outdir
outdir = './synth_outputs/simple'

class BenchmarkRun:

    def name_sim_cycles(self,sc):
        try:
            sc = int(sc)
        except:
            pass

        # if 3 digits at k level
        if sc // 1000 < 1000:
            return f'{sc//1000}k'
        #
        elif sc // 1000000 < 1000:
            return f'{sc//1000000}m'
        else:
            return f'{sc//1000000000}b'

    def __init__(self, map_file,n_routers, sim_cycle, inj_rate, mem_or_coh, n_evns, tot_vcs, noc_clk, hetero, n_cpus, dir_mult, traf_type='uniform',nr_list=None,vn_map=None, noi_freq=None):

        # simulation configs
        self.sim_cycles = sim_cycle
        self.inj_rate = inj_rate

        self.n_cpus = n_cpus
        self.dir_mult = dir_mult

        self.traf_type = traf_type

        # topology configs
        self.topology = map_file.replace('.map','').split('/')[-1]

        self.topology_map_file = map_file

        self.min_n_dl_free = n_evns
        self.n_evns = n_evns
        self.tot_vcs = tot_vcs
        self.n_dl_free = 1
        self.dl_part = self.tot_vcs - self.n_dl_free*self.min_n_dl_free

        self.topology_vn_file = vn_map

        self.topology_nr_list_file = nr_list


        self.hetero = hetero

        inj_rate_str = inj_rate.replace('.','_')

        sd_str = 'mixed'
        if not hetero:
            sd_str = 'same'

        self.mem_or_coh = mem_or_coh

        self.noc_clk = f'{noc_clk}GHz'

        self.noi_clk = self.noc_clk

        top_type = self.topology
        if '_s_' in self.topology:
            top_type = 's'
        elif '_m_' in self.topology:
            top_type = 'm'
        elif '_l_' in self.topology:
            top_type = 'l'
        elif '2ll' in self.topology:
            top_type = 'm'
        elif '15ll' in self.topology:
            top_type = 's'
        elif '25ll' in self.topology:
            top_type = 'l'

        if hetero and noi_freq is None:
            try:
                self.noi_clk = noi_clks_dict[top_type]
            except:
                print(f'Key error on topology {self.topology} w/ key={top_type} for noi freq.')
                quit(-1)
        elif hetero:
            self.noi_clk = noi_freq

        #self.output_dir = f'./outputs/{self.sim_cycles}/{self.noi_clk}/{self.mem_or_coh}/{self.topology}/{inj_rate_str}/''

        self.n_routers = str(n_routers)

        # output
        # ------

        desc = f'{self.n_evns}evns_{self.tot_vcs}vcs_{self.n_cpus}cpus_{self.dir_mult}xdirs_{self.noc_clk}'

        out_path_suffix = f'{self.name_sim_cycles(self.sim_cycles)}/{sd_str}/{self.traf_type}/{desc}/{self.mem_or_coh}/{self.topology}/{inj_rate_str}/'

        self.output_dir = os.path.join(outdir,out_path_suffix)


    def run(self):

        global config_status

        cmd = []

        # cmd += setup

        cmd += [gem5_build,
                # '--stdout-file log.out --stderr-file log.err -r -e',
                '-d', self.output_dir,
                conf_script,
                '--topology',topo_conf_script,
                '--noi_routers',self.n_routers,
                '--sim-cycles',self.sim_cycles,
                '--injectionrate',self.inj_rate,
                '--noc_clk',self.noc_clk,
                '--sys-clock',self.noc_clk,
                '--ruby-clock',self.noc_clk,
                # '--cpu-clock',self.noc_clk,
                '--noi_clk',self.noi_clk,
                '--router_map_file',self.topology_map_file,
                '--flat_vn_map_file',self.topology_vn_file,
                '--flat_nr_map_file',self.topology_nr_list_file,
                '--ruby'
                ]



        if self.mem_or_coh == 'mem':
            base_dirs = 16

            cmd += ['--mem_or_coh','mem']
        # coh
        else:

            base_dirs = self.n_cpus
            cmd += ['--mem_or_coh','coh']

        n_cpus = self.n_cpus
        n_dirs = self.dir_mult*base_dirs

        m_size = n_dirs*n_cpus*1000

        cmd += ['--mem-size',str(m_size)]
        cmd += ['--num-dirs', str(n_dirs)]
        cmd += ['--num-cpus',str(n_cpus)]

        cmd += base_flags


        cmd += ['--vcs-per-vnet',f'{self.tot_vcs}',
                '--evn_deadlock_partition',f'{self.dl_part}',
                '--evn_n_deadlock_free',f'{self.n_dl_free}',
                '--evn_min_n_deadlock_free',f'{self.min_n_dl_free}']

        if self.traf_type != 'uniform':
            cmd += ['--synthetic',f'{self.traf_type}']


        os.chdir(home)

        tdesc = f'{self.n_evns}_{self.tot_vcs}'
        desc = f'{self.mem_or_coh} : {self.topology:20} : {tdesc:20} w/ {self.traf_type:10} @ inj {self.inj_rate:5} w/ {self.n_cpus:3} cpus, {self.dir_mult}x dirs {self.noc_clk}'

        print(f'Runnning {desc}')

        # comment in/out to test script
        ###############################################################

        print(f'cmd={cmd}')
        print(' '.join(cmd))
        return

        res = None

        # res = subprocess.run(cmd, shell=True)
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
        # res = subprocess.run(cmd)


        status = 'No error'

        if res.returncode != 0:
            print(f"Config {desc}: gem5 exited with error code " \
                    + str(res.returncode))
            status = str(res.returncode)

        else:
            print(f"Config {desc} complete.")

        try:
            with open(os.path.join(self.output_dir, "stdout_stderr"), "w+") as fp:
                fp.writelines(res.stdout)
                fp.writelines(res.stderr)
        except:
            pass
        _dict = {f'{self.topology} ({self.output_dir})' : status}

        status_lock.acquire()
        config_status.update(_dict)
        # for config, status in config_status.items():
        #     print(config + ':\t' + status)
        status_lock.release()

# Bench should be BenchmarkRun object
def run_benchmark(bench):
    sem.acquire()
    # bench.run()
    # quit()
    try:
        bench.run()
    except Exception as e:
        print(f'During run, exception...\n\t{e}')
    sem.release()


def main():



    global map_files
    global inj_rates

    parser = argparse.ArgumentParser()

    parser.add_argument('-s','--sim_cycles',type=str,
                default='1000',help='TODO')  # max is 2147483647
    parser.add_argument('--mem_only',action='store_true')
    parser.add_argument('--coh_only',action='store_true')

    parser.add_argument('--samefreq_only',action='store_true')
    parser.add_argument('--mixedfreq_only',action='store_true')

    parser.add_argument('--ours_only',action='store_true')
    parser.add_argument('--prev_only',action='store_true')
    parser.add_argument('--lpbt_only',action='store_true')


    parser.add_argument('--inj_start',type=float,default=0.01)
    parser.add_argument('--inj_end',type=float,default=0.1)
    parser.add_argument('--inj_step',type=float,default=0.01)

    parser.add_argument('--one_topo',type=str)
    parser.add_argument('--nr_list',type=str)
    parser.add_argument('--vn_map',type=str)
    parser.add_argument('--noi_freq',type=str)
    parser.add_argument('--n_evn',type=int)
    parser.add_argument('--tot_vcs',type=int)
    parser.add_argument('--n_routers',type=int)

    parser.add_argument('--map_file_dir',type=str,default='./configs/topologies/paper_solutions/')

    parser.add_argument('--sys_clk',type=float,default=4.0)
    parser.add_argument('--num_cpus',type=int,default=40)
    parser.add_argument('--dir_mult',type=int,default=8)
    parser.add_argument('--traffic',type=str,default='uniform')

    parser.add_argument('--topology_mask',type=str)


    args = parser.parse_args()

    sim_cycle = args.sim_cycles

    map_files_dir = args.map_file_dir
    for root, dirs, files in os.walk(map_files_dir):
        # print(files)
        for file in files:
            map_files.append(f'{root}/{file}')


    # if args.inj_start is not None or\
    #         args.inj_end is not None or\
    #         args.inj_step is not None:
    #     # factor of 100 since range only takes ints
    #     # should np.linspace or something later
    #     a = int(1000*args.inj_start)
    #     b = int(1000*args.inj_end)
    #     c = int(1000*args.inj_step)

    #     inj_rates = [str(x/1000.0) for x in range(a,b,c)]

    inj_rates = np.arange(args.inj_start, args.inj_end,args.inj_step)
    inj_rates = [str(round(x,3)) for x in inj_rates]

    # inj_rates.reverse()

    print(f'inj_rates = {inj_rates}')

    # quit()


    runs = []

    memcoh = ['mem','coh']
    if args.mem_only:
        memcoh = ['mem']
    elif args.coh_only:
        memcoh = ['coh']

    het_tf = True
    if args.samefreq_only:
        het_tf = False
    elif args.mixedfreq_only:
        het_tf = True

    # start back
    map_files.reverse()

    if args.ours_only:
        map_files = [s for s in map_files if 'ns_' in s]
    if args.prev_only:
        map_files = [s for s in map_files if 'kite' in s\
                        or 'bfly' in s\
                        or 'butter' in s\
                        or 'mesh'\
                        or 'ft' in s\
                        or 'lpbt' in s]
    if args.lpbt_only:
        map_files = [s for s in map_files if 'lpbt' in s]



    # map_files = [s for s in map_files if 'butter' in s]
    map_files = [s for s in map_files if 'noci' not in s]

    map_files = [s for s in map_files if 'bwop' not in s]

    if args.prev_only:
        map_files = [s for s in map_files if 'ns' not in s]

    print(f'{map_files}')
    # print(f'args.prev_only={args.prev_only}')
    # quit()



    n_evns = 2
    if args.n_evn:
        n_evns = int(args.n_evn)

    tot_vcs = 4
    if args.tot_vcs:
        tot_vcs = int(args.tot_vcs)

    n_routers = 4
    if args.n_routers:
        n_routers = int(args.n_routers)


    # map_files = [s for s in map_files if 'kite_large' in s]


    clk = args.sys_clk
    n_cpus = args.num_cpus
    dir_mult = args.dir_mult

    traf_t = args.traffic

    if args.one_topo is not None:
        map_files = [args.one_topo]

    i = 0
    for mem_or_coh in memcoh:
        for inj_rate in inj_rates:
            for map_file in map_files:
                print(f'{i:04} : Adding {map_file} {inj_rate} (pkts/cpu/cycle) w/ {n_cpus}cpus {dir_mult}x(20/8)dirs @ {clk}GHz')
                runs += [BenchmarkRun(map_file, n_routers, sim_cycle, inj_rate, mem_or_coh, n_evns, tot_vcs, clk, het_tf, n_cpus, dir_mult, traf_type=traf_t,nr_list=args.nr_list, vn_map=args.vn_map, noi_freq=args.noi_freq)]
                i+=1

    #quit()

    threads = [threading.Thread(target=run_benchmark, args=(x,)) for x in runs]

    # threads = [threads[0]]

    global num_threads
    num_threads = len(threads)

    print("Dispatching " + str(num_threads) + " threads")

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Done")

    status_lock.acquire()
    for config, status in config_status.items():
        print(config + ':\t' + status)
    status_lock.release()

if __name__ == '__main__':
    main()
