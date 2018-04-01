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
    
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def astar_path(G, source, target, heuristic=None, weight='weight'):
    """Return a list of nodes in a shortest path between source and target
    using the A* ("A-star") algorithm.

    There may be more than one shortest path.  This returns only one.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path

    target : node
       Ending node for path

    heuristic : function
       A function to evaluate the estimate of the distance
       from the a node to the target.  The function takes
       two nodes arguments and must return a number.

    weight: string, optional (default='weight')
       Edge data key corresponding to the edge weight.

    Raises
    ------
    NetworkXNoPath
        If no path exists between source and target.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> print(nx.astar_path(G, 0, 4))
    [0, 1, 2, 3, 4]
    >>> G = nx.grid_graph(dim=[3, 3])  # nodes are two-tuples (x,y)
    >>> nx.set_edge_attributes(G, {e: e[1][0]*2 for e in G.edges()}, 'cost')
    >>> def dist(a, b):
    ...    (x1, y1) = a
    ...    (x2, y2) = b
    ...    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    >>> print(nx.astar_path(G, (0, 0), (2, 2), heuristic=dist, weight='cost'))
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]


    See Also
    --------
    shortest_path, dijkstra_path

    """
    if source not in G or target not in G:
        msg = 'Either source {} or target {} is not in G'
        raise nx.NodeNotFound(msg.format(source, target))

    if heuristic is None:
        # The default heuristic is h=0 - same as Dijkstra's algorithm
        def heuristic(u, v):
            return 0

    push = heappush
    pop = heappop

    # The queue stores priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    # Add a counter to the queue to prevent the underlying heap from
    # attempting to compare the nodes themselves. The hash breaks ties in the
    # priority and is guarenteed unique for all nodes in the graph.
    c = count()
    queue = [(0, next(c), source, 0, None)]

    # Maps enqueued nodes to distance of discovered paths and the
    # computed heuristics to target. We avoid computing the heuristics
    # more than once and inserting the node into the queue too many times.
    enqueued = {}
    # Maps explored nodes to parent closest to the source.
    explored = {}

    while queue:
        # Pop the smallest item from queue.
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
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

        for neighbor, w in G[curnode].items():
            if neighbor in explored:
                continue
            ncost = dist + w.get(weight, 1)
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                # if qcost < ncost, a longer path to neighbor remains
                # enqueued. Removing it would need to filter the whole
                # queue, it's better just to leave it there and ignore
                # it when we visit the node a second time.
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far
#Test
nf = input("Masukkan file matriks ketetanggaan: ")    
print(getMatriks(nf))
lok = input("Masukkan file koordinat node:")
print(getLokasi(lok))
pos=nx.get_node_attributes(getGraph(getMatriks(nf), getLokasi(lok)),'pos')
nx.draw_networkx(getGraph(getMatriks(nf), getLokasi(lok)), pos, with_labels=True, font_weight='bold')
plt.show()

if __name__ == '__main__':
    #Test
    nf = input("Masukkan file matriks ketetanggaan: ")    
    print(getMatriks(nf))
    lok = input("Masukkan file koordinat node:")
    print(getLokasi(lok))
    pos=nx.get_node_attributes(getGraph(getMatriks(nf), getLokasi(lok)),'pos')
    nx.draw(getGraph(getMatriks(nf), getLokasi(lok)), pos, with_labels=True, font_weight='bold')
    plt.show()

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