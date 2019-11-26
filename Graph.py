from operator import itemgetter,xor
import numpy as np

class Graph():
        def __init__(self,filename='content.txt'):
            self._vectorized_text = np.vectorize(self._convert_text, excluded='self')

            self._load_txt(filename)
            self._greatest_node()
            self.prim = []
            self.kruskal = []
            self.prim_cost = 0
            self.kruskal_cost = 0

        def _convert_text(self,x):
            return ord(x) - 65

        def _load_txt(self,filename):
            with open(filename, 'r') as file:
                content = [c.replace('\n', '') for c in file]
                content = [c.split(' ') for c in content[1:]]
                content = np.array(content)
                content[:, :2] = self._vectorized_text(content[:, :2])
                content = content.astype(int)

                self.nodes = content

        def _greatest_node(self):
            greatest = -1
            for row in self.nodes:
                if greatest < max(row[:2]):
                    greatest = max(row[:2])
            greatest += 1
            self.n_nodes = greatest

        def _sort_nodes(self):
            nodes = list(self.nodes)
            self.nodes = np.array(sorted(nodes, key=itemgetter(2)))

        def show_prim(self):
            print('prim: ')
            print(self.prim)

        def show_kruskal(self):
            print('kruskal:')
            print(self.kruskal)

        def find_prim(self):
            visited = np.zeros(self.n_nodes, dtype=int)
            visited[self.nodes[0][0]] = 1

            prims = []
            min_dist = []

            i = 0
            while i < self.n_nodes:
                for node_idx in range(len(self.nodes)):
                    node = self.nodes[node_idx]
                    if xor(visited[node[0]] == 1, visited[node[1]] == 1):
                        if len(min_dist) == 0:
                            min_dist = node
                        elif node[2] < min_dist[2]:
                            min_dist = node

                if len(min_dist) > 0:
                    prims.append(min_dist)
                    for idx in range(2):
                        if visited[min_dist[idx]] == 0:
                            visited[min_dist[idx]] = 1
                    min_dist = []
                i += 1

            self.prim = np.array(prims)
            self.prim_cost = self.prim[:,2].sum()

        def find_kruskal(self):
            self._sort_nodes()
            visited = np.zeros(self.n_nodes, dtype=int)
            visited[self.nodes[0][0]] = 1

            #SORT

            krusk = []
            for node in self.nodes:
                if xor(visited[node[0]] == 1, visited[node[1]] == 1):
                    krusk.append([v for v in node])

                    for idx in range(2):
                        if visited[node[idx]] == 0:
                            visited[node[idx]] = 1

            self.kruskal = np.array(krusk)
            self.kruskal_cost = self.kruskal[:,2].sum()


g = Graph()
g.find_prim()
g.show_prim()
g.find_kruskal()
g.show_kruskal()
print('prim cost: {}\nkrusk cost: {}'.format(g.prim_cost,g.kruskal_cost))