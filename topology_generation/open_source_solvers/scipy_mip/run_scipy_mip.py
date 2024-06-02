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

VERBOSE = True

# this function copied/modified from one on stack overflow
def read_mps(file_name, which_solver):

    print(f'Reading from {file_name} w/ {which_solver} solver')


    # use mip Model object
    mdl = Model(solver_name=which_solver)
    mdl.read(file_name)

    # model parameters
    num_vars = len(mdl.vars)
    num_cons = len(mdl.constrs)

    print(f'Read {num_vars} vars and {num_cons} constraints')

    # variable types and bounds
    lb = np.zeros(num_vars)
    ub = np.inf*np.ones(num_vars)
    integrality = np.zeros(num_vars)
    for i, var in enumerate(mdl.vars):
        if VERBOSE and i % 1000 == 0:
            print(f'\tBuilding bounds for var {i:05} / {num_vars:05}')
        lb[i] = var.lb
        ub[i] = var.ub
        if var.var_type != "C":
            integrality[i] = 1

    # objective
    c = np.zeros(num_vars)
    for i, var in enumerate(mdl.vars):
        if VERBOSE and i % 1000 == 0:
            print(f'\tBuilding objective for var {i:05} / {num_vars:05}')
        if var in mdl.objective.expr:
            c[i] = mdl.objective.expr[var]
    if mdl.sense != "MIN":
        c *= -1.0

    # constraint coefficient matrix
    b_l = -np.inf*np.ones((num_cons))
    b_u = np.inf*np.ones((num_cons))
    row_ind = []
    col_ind = []
    data    = []
    for i, con in enumerate(mdl.constrs):
        if VERBOSE and i % 1000 == 0:
            print(f'\tBuilding constr {i:05} / {num_cons:05}' )

        if con.expr.sense == "=":
            b_l[i] = con.rhs
            b_u[i] = con.rhs
        elif con.expr.sense == "<":
            b_u[i] = con.rhs
        elif con.expr.sense == ">":
            b_l[i] = con.rhs

        for j, var in enumerate(mdl.vars):
            if var in (expr := con.expr.expr):
                coeff = expr[var]
                row_ind.append(i)
                col_ind.append(j)
                data.append(coeff)
    A = csr_matrix((data, (row_ind, col_ind)), shape=(num_cons, num_vars))

    print(f'Sorted into var, constr, bound matrices')

    return c, b_l, A, b_u, lb, ub, integrality, mdl


def solve(mps_file_name, which_solver, out_name=None, time_limit=None):

    c, b_l, A, b_u, lb, ub, integrality, model = read_mps(mps_file_name, which_solver)

    # create optimize objects
    bounds = Bounds(lb, ub)
    constraints = LinearConstraint(A, b_l, b_u)

    options = {'disp':True}
    if time_limit is not None:
        options.update({'time_limit':time_limit})

    print(f'About to solve')
    res = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality,options=options)

    print(f'Result : {res}')



    # for i,x in enumerate(res.x):
    #     print(f'{i:02} : {x}')

    rmap_dict = {}
    n_routers = 0

    print(f'Printing map')
    for i,x in enumerate(model.vars):
        if 'map' not in str(x):
            continue
        var_val = int(round(res.x[i]))
        print(f'{i:02} : {x} = {var_val}')


        split_str = str(x).split('_')
        s_str = split_str[1]
        d_str = split_str[2]
        s = int(s_str[1:])
        d = int(d_str[1:])

        n_routers = max(s,n_routers)
        n_routers = max(d,n_routers)

        try:
            rmap_dict[s].update({d:var_val})
        except:
            rmap_dict.update({ s: {d:var_val} })

    # account for zero indexing
    n_routers += 1

    r_map = [[int(rmap_dict[s][d]) for d in range(n_routers)] for s in range(n_routers)]

    print(f'r_map ({len(r_map)})')
    for s, row in enumerate(r_map):
        print(f'{s:02} {row}')

    if out_name is None:
        out_name = mps_file_name.replace('mps','map')
        out_name = mps_file_name.replace('lp','map')
        out_name = out_name.split('/')[-1]

    out_path = f'./files/solutions/{out_name}'

    with open(out_path,'w+') as out_file:
        for row in r_map:
            line = ''
            for elem in row:
                line += str(elem) + ' '
            line = line[:-1] + '\n'
            out_file.write(line)

    print(f'wrote to {out_path}')

def main():

    parser = argparse.ArgumentParser(description='Solve MPS files with a couple solvers')
    parser.add_argument('--model_file',type=str,help='.mps/.lp model to solve',default='./../models/autotop_r6_p3_ll20_simple_avghops.mps')
    parser.add_argument('--solver',type=str,help='solver to use',default='GLOP')
    parser.add_argument('--time_limit',type=int,help='solver time limit in seconds')
    parser.add_argument('--out_map_name',type=str,help='name of file of output map')

    args = parser.parse_args()

    print(args)

    # ...

    solve(args.model_file, args.solver, time_limit=args.time_limit, out_name=args.out_map_name)


if __name__ == '__main__':
    main()
