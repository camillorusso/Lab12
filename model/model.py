import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._edges = None
        self._grafo = nx.Graph()
        self._idMap = {}
        self._idMapNome = {}

        self.solBest = 0
        self.path = []
        self.path_edge = []

    def buildGraph(self, year, country):
        lista1 = DAO.getAllRetailers()
        lista2 = []
        for element in lista1:
            if element.Country == country:
                lista2.append(element)
                self._idMap[element.Retailer_code] = element
                self._idMapNome[element.Retailer_name] = element
        self._grafo.add_nodes_from(lista2)
        self._edges = DAO.getAllEdges(year, country)
        for element in self._edges:
            a = self._idMap[element.Retailer1]
            b = self._idMap[element.Retailer2]
            self._grafo.add_edge(a, b, weight=element.peso)

    def getVolume(self, nodo):
        lista1 = self._grafo.neighbors(nodo)
        tot = 0
        for element in lista1:
            tot += self._grafo[nodo][element]['weight']
        return tot

    def computePath(self, N, lista3):
        self.path = []
        self.path_edge = []
        self.solBest = 0

        for r in lista3:
            partial = []
            partial.append(r)
            self.ricorsione(partial, N, [])

    def ricorsione(self, partial, N, partial_edge):
        r_last = partial[-1]
        r_first = partial[0]

        # terminazione
        if len(partial_edge) == (N - 1):
            if self._grafo.has_edge(r_last, r_first):
                partial_edge.append((r_last, r_first, self._grafo.get_edge_data(r_last, r_first)['weight']))
                partial.append(r_first)
                weight_path = self.computeWeightPath(partial_edge)
                if weight_path > self.solBest:
                    self.solBest = weight_path + 0.0
                    self.path = partial[:]
                    self.path_edge = partial_edge[:]
                partial.pop()
                partial_edge.pop()
            return

        neighbors = list(self._grafo.neighbors(r_last))
        neighbors = [i for i in neighbors if i not in partial]
        for n in neighbors:
            partial_edge.append((r_last, n, self._grafo.get_edge_data(r_last, n)['weight']))
            partial.append(n)

            self.ricorsione(partial, N, partial_edge)
            partial.pop()
            partial_edge.pop()
    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]
        return weight
    def getAllNations(self):
        lista1 = DAO.getAllRetailers()
        lista2 = []
        for element in lista1:
            if element.Country not in lista2:
                lista2.append(element.Country)
        return lista2

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
