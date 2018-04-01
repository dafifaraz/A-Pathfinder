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
        G.add_node(i+1, visited=False, pos=lokasi[i])
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