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


'''
Visualizes topologies as node and edge graph
'''
from operator import invert
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

import time

import argparse
import os

# # for curved edges
# from matplotlib.collections import LineCollection
# from curved_edges import curved_edges

global n_routers
global n_ports
global r_map
r_map = []
global memcoh

# for debugging
verbose = False

global inverted_map
inverted_map = False

global directed
directed =  False

global highlight_bibw
highlight_bibw = False

global highlight_sc
highlight_sc = False

desired_solutions = ['20r_15ll_opt_whop_','20r_2ll_opt_whop_']

# for floyd warshall
INF = 999

def floyd_ret_val(G):
    dist = list(map(lambda p: list(map(lambda q: q, p)), G))

    for r in range(n_routers):
        for p in range(n_routers):
            for q in range(n_routers):
                dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])

    return dist

def ingest(file_name):

    global r_map
    global n_routers
    r_map = []
    n_routers = 0

    if '.sol' in file_name:
        ingest_sol(file_name)
    elif '.map' in file_name or '.vc' in file_name \
        or '.nr' in file_name:
        ingest_map(file_name)
    else:
        print(f'error on input file type')
        quit()

    if len(r_map) > 0:
        return True


def ingest_map(path_name):
    global n_routers
    global r_map
    global inverted_map

    file_name = path_name.split('/')[-1]

    print(f'ingesting map filename = {file_name}')

    with open(path_name, 'r') as in_file:

        # for _router in range(0,n_routers):
        #     row = in_file.readline()
        for row in in_file:
            r_conns = row.split(" ")
            if '\n' in r_conns:
                r_conns.remove('\n')

            print(f'r_conns({len(r_conns)})={r_conns}')

            try:
                r_conns = [int(elem) for elem in r_conns]
            except:
                r_conns = [int(float(elem)) for elem in r_conns]
            r_map.append(r_conns)

        # print(f'r_map({len(r_map)})={r_map}')
        # input('cont?')

    n_routers = len(r_map)
    input(f'n_routers={n_routers}')

    for i in range(n_routers):

        for j in range(n_routers):
            if inverted_map:
                r_map[i][j] = 1 - r_map[i][j]

        r_map[i][i] = 0



    print(f'r_map={r_map}')




def ingest_sol(file_name):
    global n_routers
    global n_ports
    global r_map
    global memcoh


    n_lines = 0
    with open(file_name, 'r') as in_file:
        for n_lines, line in enumerate(in_file):
            pass
    n_lines += 1


    with open(file_name, 'r') as in_file:


        n_routers = in_file.readline()
        n_ports = in_file.readline()


        n_routers = int(n_routers)
        n_ports = int(n_ports)

        if n_lines == n_routers + 3:
            memcoh = in_file.readline()
            memcoh = float(memcoh)
        else:
            memcoh = 1.0

        print(f'n_routers={n_routers}, n_ports={n_ports}, memcoh={memcoh}')

        for _router in range(0,n_routers):
            row = in_file.readline()
            r_conns = row.split(" ")
            try:
                r_conns = [int(elem) for elem in r_conns]
            except:
                r_conns = [int(float(elem)) for elem in r_conns]
            r_map.append(r_conns)

        # print(f'r_map({len(r_map)})={r_map}')
        # input('cont?')




def calc_worst_cut():
    global worst_cut
    global worst_cut_combo
    # global unidir_bibw

    global worst_bottleneck
    global worst_bottleneck_combo

    global n_routers

    verbose = True

    start_time = time.time()

    routers = range(0,n_routers)
    all_combos = list()
    n_in_set = int(n_routers / 2)
    all_combos += combinations(routers, n_in_set)

    # all_connected_combos = [a for a in all_combos if is_connected_two(a)]

    # quit()

    # print(f'total # combos {len(all_combos)}\ntotal # connected {len(all_connected_combos)}')

    # quit()

    least_combo = all_combos[0]
    least_left_combo = all_combos[0]
    print(f'============\nleast_combo={least_combo}')
    (least_bw, least_left_bw) = half_bw(least_combo, vb=verbose)

    n_pkts_crossing = n_in_set*float(n_routers-n_in_set)
    # worst_bottleneck = n_pkts_crossing / least_left_bw
    worst_bottleneck =  least_left_bw / n_pkts_crossing

    worst_bottleneck_combo = all_combos[0]




    if verbose:
        print(f'worst cut: first combo has bisection bw={least_bw} from combo {least_combo}')
        print(f'worst cut: first combo has worst_bottleneck={worst_bottleneck} from least left {least_left_bw} w/ n_kts_crossing {n_pkts_crossing}')


    print(f'about to consider sets of all sizes')



    for n_in_set in range(1,n_routers):

        n_pkts_crossing = n_in_set*float(n_routers-n_in_set)


        all_combos = list()
        all_combos += combinations(routers, n_in_set)

        # s_time = time.time()

        # all_connected_combos = [a for a in all_combos if is_connected_two(a)]
        # t_diff = time.time() - s_time

        # print(f'set size {n_in_set} => # connected = {len(all_connected_combos)} / # total {len(all_combos)}\t{t_diff}s')

        # quit()

        if verbose:
            print(f'working on cut of size {n_in_set}. # combos={len(all_combos)}')
            print(f'n_pkts_crossing = {n_pkts_crossing}')

        for combo in all_combos:
            (this_bw, this_left_bw) = half_bw(combo)

            # this_bottleneck = n_pkts_crossing / this_left_bw
            this_bottleneck = this_left_bw / n_pkts_crossing

            # add is_connected criteria
            if this_left_bw < least_left_bw and is_connected(combo):
                least_left_bw = this_left_bw
                least_left_combo = combo
                if verbose:
                    print(f'worst cut: lesser left bisection bw found: {this_left_bw} < {least_left_bw}')
                    (_,__) = half_bw(combo, vb=True)
                    print(f'worst cut: combo has worst_bottleneck={worst_bottleneck} from {worst_bottleneck_combo}')


            if this_bottleneck < worst_bottleneck and is_connected(combo):
                worst_bottleneck = this_bottleneck
                worst_bottleneck_combo = combo
                if verbose:
                    print(f'worst cut: worse bottleneck found: {this_bottleneck} < {worst_bottleneck} from left_bw {this_left_bw}')
                    (_,__) = half_bw(combo, vb=True)
                    print(f'worst cut: combo has worst_bottleneck={worst_bottleneck} from {worst_bottleneck_combo}')


    # print(f'worst cut:  bisection bandwidth={least_bw} from combo {least_combo}')
    # bisection_bw = least_bw
    # bisection_bw = least_bw

    worst_cut = worst_bottleneck
    worst_cut_combo = worst_bottleneck_combo
    print(f'worst cut: left bisection bandwidth={least_left_bw}, worst_cut={worst_cut}, from combo {least_left_combo}')
    print(f'worst cut: {round(time.time() - start_time,2)} seconds elapsed')

    return worst_cut_combo



def bi_bw():

    routers = range(0,n_routers)
    all_combos = list()
    half = int(n_routers / 2)
    all_combos += combinations(routers, half)

    least_combo = all_combos[0]
    least_bw, least_left = half_bw(least_combo, vb=verbose)
    if verbose:
        print(f'first combo has bisection bw={least_bw} from combo {least_combo}')

    for combo in all_combos:
        this_bw, this_left_bw = half_bw(combo)
        if this_bw < least_bw:
            if verbose:
                print(f'lesser bisection bw found: {this_bw} < {least_bw}')
                _cl , _ll = half_bw(combo, vb=True)
            least_bw = this_bw
            least_combo = combo

    print(f'bisection bandwidth={least_bw} from combo {least_combo}')
    bisection_bw = least_bw

    return least_combo


def is_connected(in_set):
    global r_map
    global n_routers

    graph = [[INF for item in row] for row in r_map]

    for n in in_set:
        for m in in_set:
            if r_map[n][m] >= 1:
                graph[n][m] = 1

    for i in range(0,n_routers):
        graph[i][i]=0

    #print(f'graph={graph}')
    #print(f'in_set={in_set}')
    #input('continue?')

    dists = floyd_ret_val(graph)


    for n in in_set:
        for m in in_set:
            if dists[n][m] >= INF:
                #print(f'unconected {n} -> {m} for in_set {in_set}')
                return False

    return True

def half_bw(routers, vb = False):

    global r_map

    half = len(routers)
    others = [ x for x in range(0,n_routers) if x not in routers  ]

    if vb:
        print(f'routers: {routers}')
        print(f'others: {others}')

    cross_links = 0
    left_links = 0
    for router in routers:
        for other in others:
            if r_map[router][other] == 1:
                cross_links += 1
                left_links += 1

                if vb:
                    print(f'r_map[{router}][{other}]==1')
    for router in others:
        for other in routers:
            if r_map[router][other] == 1:
                cross_links += 1

                if vb:
                    print(f'r_map[{router}][{other}]==1')

    if vb:
        print(f'routers->others: cross_links={cross_links}')

    return (cross_links, left_links)



def make_graph(out_name):

    global r_map

    pos = {}

    # n_routers = 20
    # n_rows = 4
    if n_routers == 128:
        n_rows = 8
    elif n_routers == 64:
        n_rows = 8
    elif n_routers == 30:
        n_rows = 6
    elif n_routers == 12:
        n_rows = 3
    elif n_routers == 48:
        n_rows = 6
    else:
        n_rows = 4
    n_per_row = int( n_routers // n_rows)
    print(n_per_row)
    index = 0
    for row in range(n_rows):
        for col in range(n_per_row):
            xpos= col #/ 5.0
            ypos = row #/ 5.0
            pos.update({index:(xpos,ypos)})
            index += 1

    # G = nx.Graph()
    # G = nx.Graph(edge_layout='curved')
    # G = nx.DiGraph(directed="False")
    G = nx.DiGraph()


    # G.set_options("""
    #     var options = {

    #         "edges": {
    #             "arrowStrikethrough": false,
    #             "color": {
    #             "inherit": false
    #             },
    #             "font": {
    #             "size": 10,
    #             "align": "top"
    #             },
    #             "smooth": false
    #         },

    #     }
    #     """)

    dir_map = [[0 for __ in range(n_routers)] for _ in range(n_routers)]

    for src in range(n_routers):
        for dest in range(n_routers):

            # # dest = r_map[src][dest]
            # G.add_edge(src,dest)
            # continue


            if(src == dest):
                continue
            if not directed and src > dest:
                continue
            if(r_map[src][dest] < 1):
                continue
            print(f'connecting {src} -> {dest}')

            G.add_edge(src,dest)

            lower = min(src,dest)
            upper = max(src,dest)


            dir_map[lower][upper]  += 0.5

    # print(dir_map)
    # quit()

    options = {
        "font_size": 12,
        "node_size": 300,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1
    }


    if highlight_bibw:
        in_group = bi_bw()
    elif highlight_sc:
        in_group = calc_worst_cut()
    else:
        in_group = [i for i in range(n_routers)]

    # out_group = [i for i in range(n_routers) if i not in in_group]

    color_a = 'red'
    color_b = 'blue'

    color_map = []
    for node in G:
        if node in in_group:
            color_map.append(color_a)
        else:
            color_map.append(color_b)





    # nx.draw_networkx_nodes(G, pos, node_color=color_map)
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=400)
    # nx.draw(G, pos, node_color=color_map)#, with_labels=True)
    # nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_labels(G, pos,font_family="sans-serif",font_weight="bold",font_color="whitesmoke")
    for edge in G.edges(data=True):

        # print(edge)
        # input('cont?')

        # long straights
        # input(f'{edge[0]}->{edge[1]}')
        thisrad=0.0
        use_ww = False

        # vertically adjacent
        if(abs(edge[0] - edge[1]) >= 2*n_per_row and \
            edge[0] % n_per_row == edge[1] % n_per_row ) :
            thisrad=0.2
            print(f'vert adj because abs(edge[0] - edge[1])=={edge[0]}-{edge[1]}={abs(edge[0] - edge[1])}')


        # horizontally adjeacent
        elif (abs(edge[0] - edge[1]) == 2) and \
            edge[0] // n_per_row == edge[1] // n_per_row:
            thisrad=0.2
            print(f'horiz adj because abs(edge[0] - edge[1])={edge[0]}-{edge[1]}={abs(edge[0] - edge[1])}')
        # nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], connectionstyle=f'arc3, rad =0.5')

        # wrap around
        elif(abs(edge[0] - edge[1])*abs(edge[1] - edge[0]) >= 3*3  and use_ww ):
            thisrad = -0.25
            print(f'wrap around adj because abs(edge[0] - edge[1])=={edge[0]}-{edge[1]}={abs(edge[0] - edge[1])}')



        if edge[0] > edge[1]:
            thisrad = thisrad*-1

        print(f'{edge[0]}->{edge[1]} rad = {thisrad}')

        astyle = '-'
        if directed:
            astyle = '->'


        edge_type = '--'

        lower = min(edge[0],edge[1])
        upper = max(edge[0],edge[1])
        if dir_map[lower][upper] == 1.0:
            edge_type = '-'

        base_thick = 1.4
        thickness = base_thick
        if r_map[edge[0]][edge[1]] > 1:
            thickness += 2*base_thick

        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])],
            width=thickness,
            style=edge_type
            ,connectionstyle=f'arc3, rad={thisrad}',
            arrowstyle=astyle ,arrowsize=15.0)



    # Produce the curves
    # print(G)

    # curves = curved_edges(G, pos)
    # lc = LineCollection(curves, color='w', alpha=0.05)

    # # Plot
    # plt.figure(figsize=(20,20))
    # nx.draw_networkx_nodes(G, pos, node_size=5, node_color='w', alpha=0.4)
    # plt.gca().add_collection(lc)
    # plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
    # plt.show()

    # nx.draw_networkx(G, pos, **options)
    # nx.draw_networkx_edges(G, pos, connectionstyle="arc3,rad=0.5",arrowsize=0.001 )

    # nx.draw(G,pos,connectionstyle='arc3, rad=0.1')

    ax = plt.gca()
    ax.margins(0.04)
    plt.axis("off")

    plt.draw()

    fig = plt.gcf()
    print(f'Saving png to {out_name}')
    # fig.savefig(out_name, dpi=1200)
    fig.savefig(out_name)

    # input('Continue?')

    if not no_show_graph:
        plt.show()

    # show also does this
    plt.clf()


def visualize_file(path):

    name = path.split('/')[-1]
    name = name.split('.')[0]

    out_name = './files/graphs/' + name + '.png'

    ingest(path)

    make_graph(out_name)

def visualize_all(dir, mask):
    for root, dirs, files, in os.walk(dir):
        print(f'root={root}, dirs={dirs}, files={files}')
        # quit()
        if dirs == []:
            for file in files:
                if '.map' not in file:
                    continue

                try:
                    if mask not in file:
                        # print('mask not in file')
                        continue

                # no mask
                except Exception as e:
                    pass
                    # print(e)
                    # continue

                this_path = root + '/' + file
                print(f'about to visualize {this_path}')
                visualize_file(this_path)

def main():

    parser = argparse.ArgumentParser(description='Verify topology values')
    parser.add_argument('--filename',type=str,help='.sol file to evaluate')
    parser.add_argument('--all_in_dir', type=str, help='directory to run visualizer for all files')
    parser.add_argument('--all_mask', type=str, help='only do for files with this str in filename')
    parser.add_argument('--no_show',action='store_true')
    parser.add_argument('--directed',action='store_true')
    parser.add_argument('--inverted',action='store_true')
    parser.add_argument('--highlight_bi_bw',action='store_true')
    parser.add_argument('--highlight_sc',action='store_true')
    args = parser.parse_args()

    print(args)

    global no_show_graph
    no_show_graph = args.no_show

    global directed
    directed = args.directed

    global inverted_map
    inverted_map = args.inverted

    global highlight_bibw
    highlight_bibw = args.highlight_bi_bw

    global highlight_sc
    highlight_sc = args.highlight_sc

    if args.all_in_dir is not None:
        visualize_all(args.all_in_dir, args.all_mask)

    if args.filename is not None:
        visualize_file(args.filename)



if __name__ == '__main__':
    main()
