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


import sys
import ast
from copy import deepcopy

in_file = sys.argv[1]

pl = []

with open(in_file,'r') as inf:
    
    for line in inf:
        if '[' not in line:
            continue
        pl.append(line)

changes = {}
small_changes = {}

any_changes = {}

for i, p_str in enumerate(pl):
    # print(f'path {p_str}')
    as_list = ast.literal_eval(p_str)

    if len(as_list) == 1:
        continue

    s = as_list[0]
    d = as_list[-1]

    cur = as_list[0]
    reps = 0

    p_dict = {}

    for x in as_list:
        try:
            p_dict[x] += 1
        except:
            p_dict.update({x:1})

    for x, c in p_dict.items():
        if c > 1:
            any_changes.update({i:x})
        # if c >= 10:
        #     changes.update({i : x})
        # elif c > 1:
        #     small_changes.update({i:x})

    # for n in as_list[1:]:
    #     if cur == n:
    #         reps += 1
    #     else:
    #         reps = 0

    #     cur = n

        # print(f'{s}->...{d}. cur={cur} and reps={reps}')


    



        # # long repeats are total errors (remove all cur)
        # if reps >= 5:
        #     # input('here')
        #     changes.update({i:cur})

        #     try:
        #         del small_changes[i]
        #     except:
        #         pass

        # # small repeats are semi errors (keep cur but remove repeates)
        # if reps >= 1:
        #     # input('here')
        #     small_changes.update({i:cur})

    
    # if s > 12:
    #     quit()

# for ind, change in changes.items():
#     as_list = ast.literal_eval(pl[ind])
#     pl[ind] = f'{[x for x in as_list if x!=change]}\n'

#     print(f'(big) fixed pl[{ind}] : {as_list} => {pl[ind]}')
#     # quit()

# for ind, change in small_changes.items():
#     as_list = ast.literal_eval(pl[ind])


#     new_p = []

#     for p in as_list:
#         if p not in new_p:
#             new_p.append(p)
    

#     # ind_of_change = 0
#     # for i,n in enumerate(as_list):
#     #     if n == change:
#     #         ind_of_change = i
#     #         break

#     # ind_after_change = 0
#     # before = True
#     # after = False
#     # for i,n in enumerate(as_list):
#     #     if n == change:
#     #         before = False
        
#     #     if not before and n!= change:
#     #         ind_after_change = i
#     #         break

#     # new_p = as_list[:ind_of_change]
#     # new_p.append(change)
#     # new_p += as_list[ind_after_change:]

#     # print(f'reconstructing {as_list} as {new_p}')
#     # print(f'ind_of_change = {ind_of_change}, ind_after={ind_after_change}')



#     pl[ind] = f'{[x for x in new_p]}\n'

#     print(f'(small) fixed pl[{ind}] : {as_list} => {pl[ind]}')
#     # quit()


for ind, change in any_changes.items():
    as_list = ast.literal_eval(pl[ind])


    s = as_list[0]

    reversed_list = deepcopy(as_list)
    reversed_list.reverse()

    valid_reverse_path = []
    repeated = False
    prev_n = reversed_list[0]
    valid_reverse_path.append(prev_n)
    for n in reversed_list[1:]:
        if n == prev_n:
            repeated = True
            _ = valid_reverse_path.pop()
            break

        valid_reverse_path.append(n)
        
        prev_n = n

    valid_reverse_path.append(s)
    new_p = deepcopy(valid_reverse_path)
    new_p.reverse()

    pl[ind] = f'{[x for x in new_p]}\n'

    print(f'(any) fixed pl[{ind}] : {as_list} => {pl[ind]} ')

done = True

print(f'-'*72)
for p in pl:

    

    as_list = ast.literal_eval(p)

    p_dict = {}

    for x in as_list:
        try:
            p_dict[x] += 1
        except:
            p_dict.update({x:1})

    for x, c in p_dict.items():
        if c > 1:
            done = False

            print(f'error w/ path {p} due to {x} : {c}')

if not done:
    print(f'- NOT DONE {in_file}')
    quit()
else:
    print(f'+ DONE {in_file}')


with open(in_file,'w') as of:
# for p in pl:
    of.writelines(pl)

