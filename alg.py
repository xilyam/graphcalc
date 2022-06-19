import networkx as nx
import pylab

def hamilton(G):
    F = [(G,[list(G.nodes())[0]])]
    n = G.number_of_nodes()
    while F:
        graph,path = F.pop()
        confs = []
        neighbors = (node for node in graph.neighbors(path[-1])
                     if node != path[-1]) #exclude self loops
        for neighbor in neighbors:
            conf_p = path[:]
            conf_p.append(neighbor)
            conf_g = nx.Graph(graph)
            conf_g.remove_node(path[-1])
            confs.append((conf_g,conf_p))
        for g,p in confs:
            if len(p)==n:
                return p
            else:
                F.append((g,p))
    return None

G = nx.Graph()



for i in range(1,9):
    G.add_node(i)

edges = {
                (1, 2, 1),
                (1, 3, 2),
                (1, 4, 1),
                (1, 7, 3),
                (2, 3, 1),
                (2, 5, 1),
                (3, 5, 5),
                (3, 6, 3),
                (3, 7, 2),
                (4, 7, 4),
                (4, 8, 1),
                (5, 8, 1),
                (6, 7, 2),
                (6, 8, 4),
}
G.add_weighted_edges_from(edges)


# Основной граф

pos = {1: (0, 2),
       	2: (1, 3),
       	3: (1, 2),
       	4: (1, 1),
       	5: (2, 3),
       	6: (2, 2),
       	7: (2, 1),
        8: (3, 1.5)}


pylab.subplot(2, 2, 1)
pylab.title("Исходный граф")

nx.draw(G,pos, with_labels=True,node_color='yellow',node_size=600)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)


# 1-2)Матрицы смежности и инцидентности
adjacency = nx.adjacency_matrix(G).todense()
print("Матрица смежности:")
print(adjacency)
print()

incidence = nx.incidence_matrix(G).todense()
print("Матрица инцидентности:")
print("Рёбра:",list(G.edges))
print(incidence)
print()


# 3) Алгоритм Прима
tree_Kruskal = list(nx.minimum_spanning_edges(G, algorithm='prim', data=False))

pylab.subplot(2, 2, 2)
pylab.title("Алгоритм Прима")

nx.draw(G,pos,edgelist=tree_Kruskal, with_labels=True,node_color='yellow',node_size=600)


# 3) Алгоритм Краскала
pylab.subplot(2, 2, 3)
pylab.title("Алгоритм Краскала")

tree_Prim = list(nx.minimum_spanning_edges(G, algorithm='kruskal', data=False))

nx.draw(G,pos,edgelist=tree_Prim, with_labels=True,node_color='yellow',node_size=600)


#  4) Дерево кратчайших расстояний из точки 1

shortest_path_from = nx.single_source_dijkstra(G,1)
print(shortest_path_from)
shortest_path_from = list(shortest_path_from[1].values())[1:]
edges = [[(a,b) for a,b in zip(i,i[1:])] for i in shortest_path_from]
edges = [element for sub_list in edges for element in sub_list]
print("Дерево кратчайших расстояний из точки 1")
print(edges)
print()

G1 = nx.Graph()
G1.add_nodes_from(G)
for (a,b) in edges:
    G1.add_edge(a,b,weight=G.edges[a,b]['weight'])

pylab.subplot(2, 2, 4)
pylab.title("Дерево кратчайших расстояний из точки 1")

nx.draw(G1,pos, with_labels=True,node_color='yellow',node_size=600)
edge_labels = nx.get_edge_attributes(G1, "weight")
nx.draw_networkx_edge_labels(G1, pos, edge_labels)

#  5) Матрица кратчайших расстояний
shortest_paths = list(nx.all_pairs_dijkstra_path_length(G))
shortest_paths = [[sorted(shortest_paths[i][1].items())[j][1] for j in range(8)] for i in range(8)]


d = max(max(i) for i in shortest_paths)
r = min(max(i) for i in shortest_paths)

print("Матрица кратчайщих расстояний:")
for i in shortest_paths:
    print(i)
print('Диаметр графа:',d)
print('Радиус графа:',r)
print()


#  6) Проверка на Эйлеров граф
print('G Эйлеров граф?', nx.is_eulerian(G))
G2 = nx.eulerize(G)
print('G2 эйлеров граф?', nx.is_eulerian(G2))

print("Эйлеров цикл:")
eulerian_circuit = list(nx.eulerian_circuit(G2))
print(eulerian_circuit)
print()


# 7) Гамильтоновы цикл
print("Гамильтоновы цикл:")
hp = hamilton(G)
print(hp)


pylab.show()

