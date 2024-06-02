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

from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import csr_matrix
import numpy as np
from mip import Model

import argparse

VERBOSE = False

def read_allpath_list(file_name):

    pathlist = []
    n_links = 0
    n_paths = 0
    n_routers = 0
    src_dest_to_paths_map = {}
    with open(file_name,'r') as inf:
        for line in inf.readlines():
            raw_line = line.replace('\n','')
            print(f'raw_line={raw_line}')
            this_path = [int(x) for x in raw_line.split(" ")]
            pathlist.append(this_path)
            path_len = len(this_path) - 1

            s = this_path[0]
            d = this_path[-1]

            try:
                src_dest_to_paths_map[(s,d)].append(n_paths)
            except: 
                src_dest_to_paths_map.update({(s,d) : [n_paths]})

            n_links += path_len
            n_paths += 1

            for e in this_path:
                n_routers = max(e,n_routers)
    # account for zero indexing
    n_routers += 1

    print(f'read pathlsit from {file_name}')
    if VERBOSE:
        print(f'\t{pathlist}')
        input(f'src_dest_to_paths_map ({len(src_dest_to_paths_map)}) = {src_dest_to_paths_map}')
    
    print(f'w/ n_routers = {n_routers}, n_paths= { n_paths}, and n_links = {n_links}')

    return pathlist,n_routers,  n_paths, n_links, src_dest_to_paths_map

def make_mclb_model(pathlist_name, out_name):


    allpath_list, n_routers, n_paths, n_links, src_dest_to_paths_map = read_allpath_list(pathlist_name)

    # max_cload (1), cload (n^2), flow_load (n^4), path_used (n_paths), link_used (n_links)
    n_vars = 1 + n_routers**2 + n_routers**4 + n_paths + n_links

    variable_index_map = {'max_cload':0,
                            'cload':1,
                            'flow_load':1 + n_routers**2,
                            'path_used':1 + n_routers**2 + n_routers**4,
                            'link_used':1 + n_routers**2 + n_routers**4 +  n_paths
                            }


    print(f'n_vars = {n_vars}')
    # input(f'variable_index_map={variable_index_map}')

    max_load = 2*n_routers*n_routers

    # variable types and bounds
    # 0 <= max_cload <= max_load
    # 0 <= cload <= max_load
    # 0 <= flow_load <= 1 (boolean)
    # 0 <= path_used <= 1 (boolean)
    # 0 <= link_used <= 1 (boolean)
    var_lb = np.zeros(n_vars)
    var_ub = np.ones(n_vars)
    # adjust max_cload, cload ub
    var_ub[:1 + n_routers**2] = max_load

    var_integrality = np.ones(n_vars)

    if VERBOSE:
        print(f'var_lb ({var_lb.shape}) = \n\t{var_lb}')
        print(f'var_ub ({var_ub.shape} = \n\t{var_ub}')
    # input(f'var_integrality ({var_integrality.shape} = \n\t{var_integrality}')

    obj_coeffs = np.zeros(n_vars)
    obj_coeffs[0] = 1
    # input(f'obj_coeffs ({obj_coeffs.shape}) = {obj_coeffs}')

    n_constrs = 0
    constr_lb_list = []
    constr_ub_list = []

    # list of rows/lists of constraint coeffs
    constr_A_list = []

    # max_cload constr
    # max_cload >= cload[i][j] forall i,j
    # =>
    # 0 <= max_cload - cload[i][j] <= max_load  forall i,j
    for i in range(n_routers):
        for j in range(n_routers):
            if(i==j):
                which_cload = i*n_routers + j
                cload_idx = variable_index_map['cload'] + which_cload

                if VERBOSE:
                    print(f'Skipping cload_idx={cload_idx}')
                continue
            # row width = n_vars
            this_row = np.zeros(n_vars)

            which_cload = i*n_routers + j
            cload_idx = variable_index_map['cload'] + which_cload
            this_row[cload_idx] = -1

            maxcload_idx = variable_index_map['max_cload']
            this_row[maxcload_idx] = 1

            if VERBOSE:
                print(f'Constraint #{n_constrs:02} set indices cload_idx={cload_idx} to -1 and maxcload_idx={maxcload_idx} to 1')
                print(f'\t0 <= A[{maxcload_idx}] - A[{cload_idx}] <= {max_load}')
            n_constrs += 1
            
            constr_A_list.append(this_row)
            constr_lb_list.append(0)
            constr_ub_list.append(max_load)

    # input(f'Completed max_cload constr\n')

    # cload constr
    # cload[a][b] == sum( sum( flow_load[i][j][a][b] ))
    # =>
    # 0 <= -1*cload[i][j] + flow_load[i][j][0][0] + flow_load[i][j][0][1] + ... + flow_load[i][j][n-1][n-1] <= 0
    for a in range(n_routers):
        for b in range(n_routers):
            if(a==b):
                continue
            # row width = n_vars
            this_row = np.zeros(n_vars)

            which_link = a*n_routers + b

            f_idxs = []
            for i in range(n_routers):
                for j in range(n_routers):
                    which_flow = i*n_routers*n_routers*n_routers + j*n_routers*n_routers
                    

                    flow_load_idx = variable_index_map['flow_load'] + which_flow + which_link
                    this_row[flow_load_idx] = 1
                    f_idxs.append(flow_load_idx)

                    if VERBOSE:
                        print(f'flow idx {flow_load_idx} for flow src, dest {i}->{j} and link between routers {a},{b}')
            
            which_cload = a*n_routers + b
            cload_idx = variable_index_map['cload'] + which_cload
            this_row[cload_idx] = -1

            if VERBOSE:
                print(f'Constraint #{n_constrs:02} set indices cload_idx={cload_idx} to -1 and flow_idxs={f_idxs} to 1')
                print(f'\t0 <= -1*A[{cload_idx}] +A[{f_idxs}] <= 0')
            n_constrs += 1

            constr_A_list.append(this_row)
            constr_lb_list.append(0)
            constr_ub_list.append(0)

    # input(f'Completed cload constr\n')

    eM = 2*max_load
    eps = 0.001

    # path selected
    # a) pl - eM <= -eM*path_used[p] + sum( flow_load[l]) <= pl - eps
    # b) 
    for which_path, path in enumerate(allpath_list):
        s = path[0]
        d = path[-1]

        pl = len(path) - 1

        if VERBOSE:
            print(f'path {which_path:02} = {path}')

        if(s==d):
            continue


        # row width = n_vars
        this_row = np.zeros(n_vars)

        path_idx = variable_index_map['path_used'] + which_path
        this_row[path_idx] = -eM

        which_flow = s*n_routers*n_routers*n_routers + d*n_routers*n_routers

        f_idxs = []
        for i in range(pl):
            a = path[i]
            b = path[i+1]

            which_link = a*n_routers + b

            flow_load_idx = variable_index_map['flow_load'] + which_flow + which_link

            this_row[flow_load_idx] = 1
            f_idxs.append(flow_load_idx)

            if VERBOSE:
                print(f'flow idx {flow_load_idx} for flow src, dest {s}->{d} and link between routers {a},{b}')

        if VERBOSE:
            print(f'Constraint #{n_constrs:02} set indices path_idx={path_idx} to -{eM} and flow_idxs={f_idxs} to 1')
            print(f'\t{pl} - {eM} <= -{eM}*A[{path_idx}] + A[{f_idxs}] <= {pl} - {eps}')
        n_constrs += 1

        constr_A_list.append(this_row)
        constr_lb_list.append(pl - eM)
        constr_ub_list.append(pl - eps)

    # input(f'Completed path selection constr')


    # path satisfied
    # 1 == sum( path_used[p] )
    # 1 <= path_used[0] + path_used[1] + ... path_used[n_paths between src, dest] <= 1 when 
    for i in range(n_routers):
        for j in range(n_routers):
            if(i==j):
                continue
            # row width = n_vars
            this_row = np.zeros(n_vars)

            p_idxs = []
            these_paths = src_dest_to_paths_map[(i,j)]
            for which_path in these_paths:
                path_idx = variable_index_map['path_used'] + which_path
                this_row[path_idx] = 1
                p_idxs.append(path_idx)

            if VERBOSE:
                print(f'Constraint #{n_constrs:02} for src->dest {i}->{j} set indices p_idxs={p_idxs} to 1')
            n_constrs += 1

            constr_A_list.append(this_row)
            constr_lb_list.append(1)
            constr_ub_list.append(1)

    constraints = LinearConstraint(constr_A_list, constr_lb_list, constr_ub_list)
    bounds = Bounds(var_lb,var_ub)

    res = milp(c=obj_coeffs, bounds=bounds, constraints=constraints, integrality=var_integrality)

    print(f'res = {res}')

    # for i,x in enumerate(res.x):
    #     print(f'{i:03} : {x}')

    
    # reconstruct cload
    if VERBOSE:
        print(f'cload')
    for row in range(n_routers ):
        row_idx = variable_index_map['cload'] + n_routers*row
        if VERBOSE:
            print(f'{row:02} : {", ".join([ f"{int(v):02}" for v in res.x[row_idx:row_idx+n_routers]]) }')

    # reconstruct flow_load
    flow_load_mat = []
    if VERBOSE:
        print(f'flow_load')
    for flow in range(n_routers*n_routers ):
        flow_load_mat.append([])
        if VERBOSE:
            print(f'flow {flow} {flow//n_routers}->{flow%n_routers}')
        for row_num in range(n_routers):
            
            row_idx = variable_index_map['flow_load'] + n_routers*row_num + n_routers*n_routers*flow
            if VERBOSE:
                print(f'{row_num:02} : {", ".join([ f"{int(v):02}" for v in res.x[row_idx:row_idx+n_routers]]) }')
            row = res.x[row_idx:row_idx+n_routers]
            flow_load_mat[flow].append(row)

    selected_paths = reconstruct_pathlist(flow_load_mat, n_routers)

    output_pathlist(selected_paths, out_name)

def output_pathlist( path_list, file_name):

    with open(file_name, 'w+') as of:
        of.write(file_name + '\n')
        for path in path_list:
            of.write(f'{path}\n')

    print(f'Wrote to {file_name}')

# a 3D mat (flows x n_routers x n_routers)
def reconstruct_pathlist(flow_load, n_routers):
    selected_paths = []

    thresh = n_routers

    for i, load_mat in enumerate(flow_load):

        s = i // n_routers
        d = i % n_routers

        # print(f'flow {i} : {s}->{d}')

        if(s==d):
            selected_paths.append([s])
            continue

        cur = s
        path = [s]

        iters = 0
        bad_dests = []

        while(cur != d):
            # print(f'\tcur = {cur}')
            found_next = False
            for n in range(n_routers):
                # print(f'\tconsidering link {cur}->{n} w/ load_mat {load_mat[cur][n]}')

                if n in bad_dests:
                    continue

                if load_mat[cur][n] > 0:
                    cur = n
                    found_next = True
                    break

            if found_next:
                path.append(cur)

            iters += 1
            if iters > thresh:
                # input(f'bad dest {cur}')
                # restart
                bad_dests.append(cur)
                cur = s
                path = [s]
                iters = 0

            

        # print(f'w/ path {path}')
        selected_paths.append(path)

    return selected_paths

def make_test_model():
    '''
        obj:
            min x
        constr:
            x >= 3 + y
            x <= 2*y

            =>
            
            3 <= x - y <= inf
            -inf <= x - 2y <= 0

        bounds:
            x int, [-100,100]
            y dbl, [0, 100)
    '''

    obj_coeffs = np.array([1,0])

    l_bs = np.array([3,-np.inf])
    u_bs = np.array([np.inf, 0])
    A = np.array([ [1, -1] , [1, -2]])

    var_l_bs = np.array([-100,0])
    var_u_bs = np.array([100,100])

    constraints = LinearConstraint(A, l_bs, u_bs)
    bounds = Bounds(var_l_bs,var_u_bs)
    integrality = np.array([1,0])

    res = milp(c=obj_coeffs, bounds=bounds, constraints=constraints, integrality=integrality)

    print(f'res = {res}')

def main():

    parser = argparse.ArgumentParser(description='Solve MCLB formulation with open source solvers')
    parser.add_argument('--allpath_list',type=str,help='allpath_list to solve')
    parser.add_argument('--test_model',action='store_true',help='allpath_list to solve')
    parser.add_argument('--out_name',type=str,help='name of output pathlist file')

    parser.add_argument('--is_noci',action='store_true',help='...')
    parser.add_argument('--cohmem_prioritized',action='store_true',help='...')
    parser.add_argument('--doubley_memory',action='store_true',help='...')

    args = parser.parse_args()

    print(args)

    # ...

    if(args.test_model):
        make_test_model()

    make_mclb_model(args.allpath_list, args.out_name)

if __name__ == '__main__':
    main()
