import networkx as nx
import matplotlib.pyplot as plt

#Menerima input nama file, mengembalikan matriks ketetanggaan berbobot
def getMatriks(namafile):
    with open(namafile) as file:
        data = file.readlines()
        matriks = []
        for line in data:
            nums = line.split(" ")
            matriks.append(nums)
            #print("Data yang diinput:\n")
            #print(nums)
    return matriks

def getGraph(matriks):
    G = nx.Graph()
    


nf = input("Enter file: ")    
print(getMatriks(nf))

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