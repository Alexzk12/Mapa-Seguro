import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(r'C:\Users\Alex\Desktop\Proyecto Maps\calles.csv')

g = nx.DiGraph()

for _, row in df.iterrows(): #creacion de aristas con ayuda de 
    distancia = row['distancia']
    peligrosidad = row['peligrosidad']
    peso_combinado = (distancia + peligrosidad) / 2  
    g.add_edge(row['origen'], row['destino'], weight=peso_combinado,
               distancia=distancia, peligrosidad=peligrosidad)


pos = {
    'PedroMoreno_EsqTorres': (0, 3), 'PedroMoreno_EsqFlores': (1, 3), 'PedroMoreno_Esq1Mayo': (2, 3), 'PedroMoreno_EsqMendoza': (3, 3),
    'DiazMiron_EsqTorres': (0, 2), 'DiazMiron_EsqFlores': (1, 2), 'DiazMiron_Esq1Mayo': (2, 2), 'DiazMiron_EsqMendoza': (3, 2),
    'MiguelHidalgo_EsqTorres': (0, 1), 'MiguelHidalgo_EsqFlores': (1, 1), 'MiguelHidalgo_Esq1Mayo': (2, 1), 'MiguelHidalgo_EsqMendoza': (3, 1),
}

plt.figure(figsize=(10, 7))
nx.draw(g, pos, with_labels=True, font_color='black', node_color='lightblue',
        node_size=2500, font_size=6, font_weight='bold', arrows=False)
edge_labels = { (u,v): f"{d['distancia']}m, P:{d['peligrosidad']}" for u,v,d in g.edges(data=True) }
nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
plt.title("Intersecciones con distancia y peligrosidad")
plt.show(block=False)

print("\nIntersecciones disponibles:")
for nodo in g.nodes:
    print("-", nodo)

origen_usuario = input("\n¿Dónde estás? Escribe el nombre exacto de la intersección: ")
destino_usuario = input("¿A dónde quieres ir? Escribe el nombre exacto de la intersección: ")

try:
    camino_encontrado = nx.dijkstra_path(g, origen_usuario, destino_usuario, weight='weight')
    print("\nRuta encontrada:")
    total_distancia = 0
    total_peligrosidad = 0
    total_peso = 0

    for i in range(len(camino_encontrado) - 1):
        nodo1 = camino_encontrado[i]
        nodo2 = camino_encontrado[i + 1]
        datos_arista = g[nodo1][nodo2]
        distancia = datos_arista['distancia']
        peligrosidad = datos_arista['peligrosidad']
        peso = datos_arista['weight']
        print(f"{nodo1} -> {nodo2}: Distancia={distancia}m, Peligrosidad={peligrosidad}, Peso combinado={peso:.2f}")
        total_distancia += distancia
        total_peligrosidad += peligrosidad
        total_peso += peso

    print(f"\nDistancia total: {total_distancia} metros")
    print(f"Peligrosidad total: {total_peligrosidad}")
    print(f"Peso combinado total: {total_peso:.2f}")

except nx.NetworkXNoPath:
    print("\nNo se encontró una ruta entre esos puntos.")
