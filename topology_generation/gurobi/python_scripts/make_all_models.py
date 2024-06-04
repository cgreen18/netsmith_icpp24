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


import subprocess

exe_ns = './bin/auto_top'
exe_lpbt = './bin/lpbt'

n_rs = [6, 12, 20, 30, 48, 64]
#n_rs = [20, 30, 48, 64]
#n_ps = [3,4,5,6]
n_ps = [4]
lls = [15, 2, 25]
simple_mods = [False, True]
objs = ['total_hops','power']
use_lps = [False]#[False, True]
soses = [False]
use_sym = [False]

base_flags = ['--no_solve','--write_model']#,'--write_presolved']



def create_and_run_cmd_ns(n_routers, n_ports, longest_link, is_sym, simple_model, sos_allowed, obj, use_lp):

    cmd = []

    # setup = ['source','setup.sh;']

    # cmd += setup

    cmd += [exe_ns]

    pdef = f'files/prob_defs/dev_{n_routers}r_{n_ports}p_{longest_link}ll.dat'
    cmd += ['-if', pdef]

    if use_lp:
        cmd += ['--use_lp_model']



    cmd += ['-o',obj]

    cmd += base_flags

    #input(' '.join(cmd))

    cmd = ' '.join(cmd)

    print(cmd)
    # return

    res = None

    # res = subprocess.run(cmd, shell=True)
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    # res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)

    # quit()

def create_and_run_cmd_lpbt(n_routers, n_ports, longest_link, obj, use_lp):

    cmd = []

    # setup = ['source','setup.sh;']

    # cmd += setup

    cmd += [exe_lpbt]

    pdef = f'files/prob_defs/dev_{n_routers}r_{n_ports}p_{longest_link}ll.dat'
    cmd += ['-if', pdef]

    if use_lp:
        cmd += ['--use_lp_model']


    cmd += ['-o',obj]

    cmd += base_flags

    #input(' '.join(cmd))

    cmd = ' '.join(cmd)

    print(cmd)
    # return

    res = None

    # res = subprocess.run(cmd, shell=True)
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    # res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)

    # quit()

def main():
    for nr in n_rs:
        for p in n_ps:
            for ll in lls:
                for usym in use_sym:
                    for sm in simple_mods:
                        for sos in soses:
                            for o in objs:
                                for ulp in use_lps:
                                    # reg model and sos doesnt make sense
                                    if not sm and sos:
                                        continue

                                    # constraints too large
                                    if nr > 20 and (o == 'sc_bw' or o == 'bi_bw'):
                                        continue
                                    create_and_run_cmd_ns(nr, p, ll, usym, sm, sos, o, ulp)

    for nr in n_rs:
        for p in n_ps:
            for ll in lls:
                for o in objs:
                    for ulp in use_lps:
                        create_and_run_cmd_lpbt(nr, p+1, ll, o, ulp)

if __name__ == '__main__':
    main()
