from operator import invert
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os

global n_noi_routers
global r_map
r_map = []
global noi_r_map
noi_r_map = []
global noi_rows
noi_rows = 4

global n_routers

global noc_r_map
noc_r_map = []

global n_noc_routers
n_noc_routers = 64
global noc_rows
noc_rows = 8

global directed
directed = False

global no_show_graph
no_show_graph = False

global verbose
verbose = False

def ingest_map(path_name):
    global n_noi_routers
    global noi_r_map

    noi_r_map = []

    file_name = path_name.split('/')[-1]

    print(f'filename = {file_name} ({path_name})')

    with open(path_name, 'r') as in_file:

        # for _router in range(0,n_routers):
        #     row = in_file.readline()
        for row in in_file:
            r_conns = row.split(" ")
            if '\n' in r_conns:
                r_conns.remove('\n')
            try:
                r_conns = [int(elem) for elem in r_conns]
            except:
                r_conns = [int(float(elem)) for elem in r_conns]
            noi_r_map.append(r_conns)

        #print(f'r_map({len(noi_r_map)})={noi_r_map}')
        #input('cont?')

    n_noi_routers = len(noi_r_map)

    for i in range(n_noi_routers):
        noi_r_map[i][i] = 0



def gen_construct_noc():

    global noc_r_map
    noc_r_map = [ [0 for _aa in range(n_noc_routers)] for _a in range(n_noc_routers)]

    noc_per_row = n_noc_routers // noc_rows
    noc_rows_per_chiplet = noc_rows // 2
    noc_per_row_per_chiplet = noc_per_row //2

    # print(f'noc_rows={noc_rows}. per_row={noc_per_row}')
    # quit()

    assert(n_noc_routers % noc_rows == 0)

    for row in range(noc_rows):
        for col in range(noc_per_row):
            # all are src is self
            r_src = col + row*noc_per_row
            if verbose:
                print(f'\trow={row}, col={col}. noc_router={r_src} (abs {n_noi_routers + r_src})')



            # east -> west
            # if not on right edge of a chiplet
            if not ((col + 1) % noc_per_row_per_chiplet ==0):
                # print(f'here')
                r_dest = (col + 1) + (row * noc_per_row)
                noc_r_map[r_src][r_dest] = 1


            # west -> east
            # if not on left edge of a chiplet
            if not (col  % noc_per_row_per_chiplet ==0):
                #print(f'here')
                r_dest = (col - 1) + (row * noc_per_row)
                noc_r_map[r_src][r_dest] = 1

            # north -> south
            # if not on bottom row or middle row
            if not ((row % noc_rows_per_chiplet) == 0 ):
                #print(f'here')
                r_dest = col  + (row - 1)* noc_per_row
                noc_r_map[r_src][r_dest] = 1

            # south -> north
            # if not on top row or middle row
            if not (((row + 1) % noc_rows_per_chiplet) == 0 ):
                #print(f'here')
                r_dest = col  + (row + 1)* noc_per_row
                noc_r_map[r_src][r_dest] = 1



def connect_noci():

    # both
    global r_map
    global n_routers
    # r_map = noi_r_map + noc_r_map

    global n_noi_routers
    global noi_r_map
    global noc_r_map

    n_routers = n_noi_routers + n_noc_routers

    #print(f'n_routers={n_routers}')

    r_map = [[0 for _a in range(n_routers) ] for _aa in range(n_routers)]

    offset = 0
    for i, conns in enumerate(noi_r_map):
        for j, dest in enumerate(conns):
            r_map[i+offset][j+offset] = noi_r_map[i][j]
            # print(f'connecting noi {i} -> {j}')


    # print(f'r_map={r_map[:20][:20]}')
    # print(f'noirouters = {n_noi_routers}')
    # quit()


    offset = n_noi_routers
    for i, conns in enumerate(noc_r_map):
        for j, dest in enumerate(conns):
            r_map[i+offset][j+offset] = noc_r_map[i][j]

    #print_map(r_map)

    noc_per_row = n_noc_routers // noc_rows

    noi_per_row = n_noi_routers // noi_rows # 24/20 // 4 = 6/5

    for noc_row in range(noc_rows):
        for noc_col in range(noc_per_row):

            noc_r = noc_col + noc_row*noc_per_row
            abs_noc_r = n_noi_routers + noc_r

            if n_noi_routers == 24:
                noi_col = (noc_col // 2) + 1
                noi_row = noc_row // 2
            elif n_noi_routers == 64:
                noi_col = noc_col
                noi_row = noc_row
            else:
                noi_col = (noc_col +1) //2
                noi_row = noc_row // 2 # same lol

            noi_r = noi_col + noi_row*noi_per_row
            abs_noi_r = noi_r

            #print(f'connecting noc ({noc_col},{noc_row}) {noc_r}(abs {abs_noc_r}) <-> noi ({noi_col},{noi_row}) {noi_r} (abs {abs_noi_r})')
            r_map[abs_noc_r][abs_noi_r] = 1
            r_map[abs_noi_r][abs_noc_r] = 1

def print_map(m):

    #return

    skip = False

    for i,s in enumerate(m):
        if i == 20:
            skip = False
        if skip:
            continue

        if i > 10 and i < 20:
            print(f'...')
            #skip = True
            #continue
            pass

        if i > 30:
            # skip = True
            #continue
            pass

        print(f'{i} : {s}')

def output_map(ofn, map):

    with open(ofn,'w+') as of:
        for row in map:
            l = []
            for elem in row:
                l.append(f'{elem} ')
            l.append('\n')
            of.writelines(l)

    print(f'wrote to {ofn}')
    # quit()


def make_total_graph(out_name):

    pos = {}

    noi_per_row = n_noi_routers // noi_rows

    noc_per_row = n_noc_routers // noc_rows

    # noi
    index = 0
    for noi_row in range(noi_rows):
        for noi_col in range(noi_per_row):
            if n_noi_routers == 20:
                xpos = noi_col
                ypos = noi_row + 0.5

            elif n_noi_routers == 24:
                if (noi_col == 0):
                    xpos = 0.0


                elif ((noi_col + 1) % noi_per_row == 0):
                    xpos = 4.0
                else:
                    xpos = (noi_col - 1) + 0.5

                ypos = noi_row + 0.5

            elif n_noi_routers == 64:
                # print(f'found the 64 router case')
                xpos = ( noi_col / 2.0 )
                ypos = ( noi_row / 2.0 )
            else:
                print('uncompleted')
                quit()

            pos.update({index:(xpos,ypos)})
            index += 1

    for noc_row in range(noc_rows):
        for noc_col in range(noc_per_row):
            xpos = ( noc_col / 2.0 ) + .15
            ypos = ( noc_row / 2.0 ) + .15

            pos.update({index:(xpos,ypos)})
            index += 1

    G = nx.DiGraph()

    for src in range(n_routers):
        for dest in range(n_routers):
            if(src == dest):
                continue
            if not directed and src > dest:
                continue
            if(r_map[src][dest] != 1):
                continue
            G.add_edge(src,dest)

    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)

    index = 0
    for edge in G.edges(data=True):

        # print(edge)
        # input('cont?')

        # long straights
        #print(f'{edge[0]}->{edge[1]}')
        thisrad=0.0

        # noi
        if index < n_noi_routers:

            # vertically adjacent
            if(abs(edge[0] - edge[1]) >= 2*noi_per_row):
                thisrad=0.2
                # print(f'abs(edge[0] - edge[1])={abs(edge[0] - edge[1])}')


            # horizontally adjeacent
            if (abs(edge[0] - edge[1]) >= 2):
                thisrad=0.2
                # print(f'abs(edge[0] - edge[1])={abs(edge[0] - edge[1])}')
            # nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], connectionstyle=f'arc3, rad =0.5')

        # noc
        else:

            # vertically adjacent
            if(abs(edge[0] - edge[1]) >= 2*noc_per_row):
                thisrad=0.2
                # print(f'abs(edge[0] - edge[1])={abs(edge[0] - edge[1])}')


            # horizontally adjeacent
            if (abs(edge[0] - edge[1]) >= 2):
                thisrad=0.2
                # print(f'abs(edge[0] - edge[1])={abs(edge[0] - edge[1])}')


        if abs(edge[0] - edge[1]) >= n_noi_routers-1:

            this_rad=0.0
            # print(f'rad={this_rad}')


        astyle = '-'
        if directed:
            astyle = '->'
        nx.draw_networkx_edges(G, pos,
            edgelist=[(edge[0],edge[1])],
            connectionstyle=f'arc3, rad={thisrad}',
            arrowstyle=astyle
            )#,arrowsize=0.001)

        index += 1

    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")

    plt.draw()

    fig = plt.gcf()
    print(f'Saving png to {out_name}')
    fig.savefig(out_name)

    # input('Continue?')

    if not no_show_graph:
        plt.show()

    # show also does this
    plt.clf()

def make_graph(out_name, map, n_per_row):

    pos = {}

    # n_routers = 20
    # n_rows = 4

    n_routers = len(map)

    if n_routers == 64:
        n_rows = 8
    else:
        n_rows = 4
    n_per_row = int( n_routers / n_rows)
    # print(n_per_row)
    index = 0
    for row in range(n_rows):
        for col in range(n_per_row):
            xpos= col #/ 5.0
            ypos = row #/ 5.0
            pos.update({index:(xpos,ypos)})
            index += 1


    G = nx.DiGraph()

    for src in range(n_routers):
        for dest in range(n_routers):
            if(src == dest):
                continue
            if not directed and src > dest:
                continue
            if(map[src][dest] != 1):
                continue
            G.add_edge(src,dest)

    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)

    for edge in G.edges(data=True):

        # print(edge)
        # input('cont?')

        # long straights
        # print(f'{edge[0]}->{edge[1]}')
        thisrad=0.0

        # vertically adjacent
        if(abs(edge[0] - edge[1]) >= 2*n_per_row):
            thisrad=0.2
            # print(f'abs(edge[0] - edge[1])={abs(edge[0] - edge[1])}')


        # horizontally adjeacent
        if (abs(edge[0] - edge[1]) >= 2):
            thisrad=0.2
            # print(f'abs(edge[0] - edge[1])={abs(edge[0] - edge[1])}')
        # nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], connectionstyle=f'arc3, rad =0.5')
        astyle = '-'
        if directed:
            astyle = '->'
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])],connectionstyle=f'arc3, rad={thisrad}',arrowstyle=astyle )#,arrowsize=0.001)


    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")

    plt.draw()

    fig = plt.gcf()
    print(f'Saving png to {out_name}')
    fig.savefig(out_name)

    # input('Continue?')

    if not no_show_graph:
        plt.show()

    # show also does this
    plt.clf()

def main():


    parser = argparse.ArgumentParser(description='Verify topology values')
    parser.add_argument('--filename',type=str,help='.sol file to evaluate')
    parser.add_argument('--verbose',action='store_true',help='debug prints')
    parser.add_argument('--all_in_dir', type=str, help='directory to run visualizer for all files')
    parser.add_argument('--out_file_name', type=str, help='only do for files with this str in filename')
    parser.add_argument('--all_mask', type=str, help='only do for files with this str in filename')
    parser.add_argument('--no_show',action='store_true')
    parser.add_argument('--directed',action='store_true')


    args = parser.parse_args()

    global no_show_graph
    no_show_graph = args.no_show

    global directed
    directed = args.directed

    global verbose
    verbose = args.verbose


    if args.all_in_dir is not None:
        gen_all_in_dir(args.all_in_dir, mask=args.all_mask)

    elif args.filename is not None:
        gen_one_file(args.filename)

def gen_all_in_dir(dir, mask = None):
    for root, dirs, files, in os.walk(dir):
        print(f'root={root}, dirs={dirs}, files={files}')
        # quit()
        for file in files:

            try:
                if mask not in file:
                    print('mask not in file')
                    continue

            # no mask
            except Exception as e:
                pass
                # print(e)
                # continue

            this_path = root + file
            gen_one_file(this_path)


def gen_one_file(path_name):

    filename = path_name.split('/')[-1]
    topo = filename.split('.')[0]

    ingest_map(path_name)

    gen_construct_noc()

    connect_noci()

    #print_map(r_map)

    make_total_graph(f'files/graphs/{topo}_noci.png')

    output_map(f'./topologies_and_routing/topo_maps/noci/{topo}_noci.map', r_map)



if __name__ == '__main__':
    main()
