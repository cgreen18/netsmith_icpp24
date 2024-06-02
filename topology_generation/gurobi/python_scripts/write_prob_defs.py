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



n_routers = [6, 12, 16, 20, 30, 48, 64]
n_ports = [3,4,5,6]
longest_links = [15, 2, 25]


n_routers_to_rows_dict = {
                        6: 2,
                        12:3,
                        16:4,
                        20:4,
                        30:6,
                        48:6,
                        64:8}

def write_prob_def(name, nr, np, ll):

    n_rows = n_routers_to_rows_dict[nr]

    n_cols = nr // n_rows

    if len(str(ll)) > 1:
        ll /= 10.0

    out_lines = []
    out_lines.append(str(nr))
    out_lines.append('\n')
    out_lines.append(str(np))
    out_lines.append('\n')
    out_lines.append(str((ll)))
    out_lines.append('\n')
    out_lines.append(str(n_rows))
    out_lines.append('\n')

    x_locs = []
    y_locs = []
    for i in range(nr):
        col = i % n_cols
        row = i // n_cols
        x_locs.append(str(col))
        y_locs.append(str(row))

    # print(f'x_locs={x_locs}')
    # print(f'y_locs={y_locs}')


    x_str = ' '.join(x_locs)
    y_str = ' '.join(y_locs)
    out_lines.append(x_str)
    out_lines.append('\n')
    out_lines.append(y_str)

    # input(f'out_lines = {out_lines}')

    with open(name,'w+') as ouf:
        ouf.writelines(out_lines)
    print(f'wrote to {name}')

for nr in n_routers:
    for np in n_ports:
        for ll in longest_links:
            name = f'./files/prob_defs/dev_{nr}r_{np}p_{ll}ll.dat'
            write_prob_def(name, nr, np,ll)








