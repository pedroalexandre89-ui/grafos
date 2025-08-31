import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.adjacencia = {}

    def adicionar_vertice(self, vertice):
        if vertice not in self.adjacencia:
            self.adjacencia[vertice] = []

    def adicionar_aresta(self, origem, destino, peso):
        if origem not in self.adjacencia:
            self.adicionar_vertice(origem)
        if destino not in self.adjacencia:
            self.adicionar_vertice(destino)
        self.adjacencia[origem].append((destino, peso))

    def dijkstra(self, inicio, fim):
        distancias = {vertice: float('inf') for vertice in self.adjacencia}
        distancias[inicio] = 0
        predecessores = {vertice: None for vertice in self.adjacencia}
        fila_prioridade = [(0, inicio)]

        while fila_prioridade:
            distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)

            if distancia_atual > distancias[vertice_atual]:
                continue

            for vizinho, peso in self.adjacencia[vertice_atual]:
                nova_distancia = distancia_atual + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = vertice_atual
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

        caminho = []
        atual = fim
        while atual is not None:
            caminho.insert(0, atual)
            atual = predecessores[atual]

        if distancias[fim] == float('inf'):
            return None, float('inf')

        return caminho, distancias[fim]

    def desenhar_grafo(self, caminho=None):
        G = nx.DiGraph()  # Grafo direcionado
        for origem, vizinhos in self.adjacencia.items():
            for destino, peso in vizinhos:
                G.add_edge(origem, destino, weight=peso)

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        if caminho:
            edges_destacados = list(zip(caminho, caminho[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges_destacados, edge_color='red', width=2)

        plt.title("Mapa de Rotas")
        plt.show()

def main() -> None:
    grafo = Grafo()

    arestas = [
        ('A', 'B', 4), ('A', 'C', 2),
        ('B', 'C', 5), ('B', 'D', 10),
        ('C', 'E', 3), ('D', 'E', 4),
        ('E', 'A', 7)
    ]

    for origem, destino, peso in arestas:
        grafo.adicionar_aresta(origem, destino, peso)

    inicio = input("Digite o ponto de partida: ").upper()
    fim = input("Digite o ponto de chegada: ").upper()

    caminho, custo = grafo.dijkstra(inicio, fim)

    if caminho and custo != float('inf'):
        print(f"\nCaminho mais curto: {' -> '.join(caminho)}")
        print(f"Custo total: {custo}")
        grafo.desenhar_grafo(caminho)
    else:
        print("\nNão existe caminho entre os pontos fornecidos.")
        grafo.desenhar_grafo()

if __name__ == "__main__":
    main()
