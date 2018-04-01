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

def euclid(now, dest):
    distance = math.sqrt( ((now[0]-dest[0])**2)+((now[1]-dest[1])**2) )
    return distance

def cost(g, h):
    return g + h

"""class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

    Return a list of nodes in a shortest path between source and target
    using the A* ("A-star") algorithm. """
"""
def a_star_search(G, source, dest):
    # The queue stores priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    # Add a counter to the queue to prevent the underlying heap from
    # attempting to compare the nodes themselves. The hash breaks ties in the
    # priority and is guarenteed unique for all nodes in the graph.
    c = count()
    queue = [(0, next(c), source, 0, None)]
    # Maps explored nodes to parent closest to the source.
    explored = {}
    while queue:
        # Pop the smallest item from queue.
        _, __, curnode, dist, parent = heappop(queue)

        if curnode == dest:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            continue

        explored[curnode] = parent
       
        for neighbor in [n for n in G.neighbors(curnode)]:
            if neighbor in explored:
                continue
            g = dist + G.edge[curnode][neighbor]["weight"]
            h =  euclid(G.node[curnode]["pos"], G.node[dest]["pos"]))
            heappush(queue, (cost(g, h), next(c), neighbor, g, curnode)
"""   
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
    curnode = 1
    print(G.node[curnode]["pos"])
    """
    G = nx.Graph()
    G.add_node(1, pos=(0,0))
    G.add_node(2, pos=(1,5))
    G.add_node(3, pos=(2,5))
    G.add_node(4, pos=(2,7))
    G.add_node(5, pos=(3,5))

    G.add_edge(1,2)
    G.add_edge(2,3)
    G.add_edge(1,3)
    G.add_edge(4,5)
    G.add_edge(3,5)
    pos=nx.get_node_attributes(G,'pos')
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.show()
    """
