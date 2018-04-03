from heapq import heappush, heappop
from itertools import count
import networkx as nx
import matplotlib.pyplot as plt
import math

#Menerima input nama file, mengembalikan matriks ketetanggaan berbobot
def getMatriks(namafile):
    with open(namafile) as file:
        data = file.readlines()
        data = [x.strip() for x in data]
        matriks =[]
        for line in data:
            nums = line.split(" ")
            temp = []
            for string in nums:
                val = int(string)
                temp.append(val)
            matriks.append(temp)
            #print("Data yang diinput:\n")
            #print(nums)
    return matriks

#Menerima input nama file, mengembalikan matriks berisi koordinat simpul
def getLokasi(namafile):
    with open(namafile) as file:
        data = file.readlines()
        data = [x.strip() for x in data]
        matriks =[]
        for line in data:
            nums = line.split(" ")
            temp = []
            for string in nums:
                val = float(string)
                temp.append(val)
            matriks.append(temp)
            #print("Data yang diinput:\n")
            #print(nums)
    return matriks

#Menerima input matriks ketetanggan, mengembalikan graf
def getGraph(matriks, lokasi):
    G = nx.Graph()
    for i in range(0, len(matriks)):
        j = 0
        G.add_node(i+1, pos=lokasi[i])
        while j < len(matriks) and matriks[i][j] != 9999:
            if matriks [i][j] != 0:
                G.add_edge(i+1,j+1,weight=matriks[i][j])
            j += 1
    return G

#Menerima koordinat simpul terkini dan koordinat simpul tujuan, mengembalikan jarak heuristic
def euclid(now, dest):
    distance = math.sqrt( ((now[0]-dest[0])**2)+((now[1]-dest[1])**2) )
    return distance

#Menerima cost so far dan estimated heuristic cost to goal, mengembalikan total estimated cost
def cost(g, h):
    return g + h

#Algoritma shortest-pathfinding
def a_star_search(G, source, dest):
    # queue menyimpan priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    c = count()
    queue = [(0, next(c), source, 0, None)]
    # Maps explored nodes to parent closest to the source.
    explored = {}
    while queue:
        # Pop the smallest item dari queue
        _, __, curnode, dist, parent = heappop(queue)

        #Cek apakah sudah sampai ke simpul goal
        if curnode == dest:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            print("Jarak tempuh = ", dist)
            return path

        #Jika node sudah dikunjungi maka abaikan
        if curnode in explored:
            continue

        explored[curnode] = parent

        #Kunjungi semua tetangga dari simpul 
        for neighbor in [n for n in G.neighbors(curnode)]:
            if neighbor in explored:
                continue
            g = dist + G[curnode][neighbor]["weight"]
            h =  euclid(G.node[curnode]["pos"], G.node[dest]["pos"])
            heappush(queue, (cost(g, h), next(c), neighbor, g, curnode))

if __name__ == '__main__':
   #Test
    nf = input("Masukkan file matriks ketetanggaan: ")
    M = getMatriks(nf)
    #print(M)
    lok = input("Masukkan file koordinat node:")
    L = getLokasi(lok)
    #print(L)
    G = getGraph(M, L)
    
    pos=nx.get_node_attributes(G,'pos')
    arc_weight=nx.get_edge_attributes(G,'weight')
    nx.draw_networkx(G, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=arc_weight)
    plt.gca().invert_xaxis()
    plt.show()
    start = int(input("Masukkan titik start: ))
    end = int(input("Masukkan titik end: ))
    curnode = start
    #print(G.node[curnode]["pos"])
    print(a_star_search(G, start, end))