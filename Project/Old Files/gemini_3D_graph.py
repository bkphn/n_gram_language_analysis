import networkx as nx
import plotly.graph_objects as go
import numpy as np


def draw_interactive_3d(similarity_matrix, languages, threshold=0.90):
    # 1. Budujemy graf (tak jak wcześniej)
    G = nx.Graph()
    for i, lang in enumerate(languages):
        G.add_node(lang.capitalize())

    # Dodajemy krawędzie (metoda Najbliższych Sąsiadów + Próg)
    n = len(languages)
    for i in range(n):
        # Dodaj 2 najbliższych sąsiadów
        sorted_idx = similarity_matrix[i].argsort()
        for neighbor_idx in sorted_idx[-3:-1]:
            weight = similarity_matrix[i][neighbor_idx]
            G.add_edge(languages[i].capitalize(), languages[neighbor_idx].capitalize(), weight=weight)

        # Dodaj silne połączenia powyżej progu
        for j in range(i + 1, n):
            weight = similarity_matrix[i][j]
            if weight > threshold:
                G.add_edge(languages[i].capitalize(), languages[j].capitalize(), weight=weight)

    print("Obliczam layout 3D (to może chwilę potrwać)...")

    # 2. KLUCZOWY MOMENT: dim=3
    # Mówimy algorytmowi sprężynowemu, że ma 3 wymiary do dyspozycji!
    pos = nx.spring_layout(G, dim=3, seed=42, k=0.5)

    # 3. Wyciągamy współrzędne X, Y, Z dla węzłów
    x_nodes = [pos[k][0] for k in G.nodes]
    y_nodes = [pos[k][1] for k in G.nodes]
    z_nodes = [pos[k][2] for k in G.nodes]

    # 4. Tworzymy ślad węzłów (Nodes Trace)
    trace_nodes = go.Scatter3d(
        x=x_nodes, y=y_nodes, z=z_nodes,
        mode='markers+text',
        marker=dict(size=8, color='steelblue', line=dict(color='white', width=1)),
        text=list(G.nodes),
        textposition="top center",
        hoverinfo='text'
    )

    # 5. Tworzymy ślad krawędzi (Edges Trace)
    # W Plotly 3D rysujemy linie jako jeden długi ciąg z przerwami (None)
    edge_x = []
    edge_y = []
    edge_z = []

    for u, v in G.edges():
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    trace_edges = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='salmon', width=2),
        hoverinfo='none'
    )

    # 6. Składamy i rysujemy
    layout = go.Layout(
        title="Interaktywna Mapa Językowa 3D",
        width=1200,
        height=800,
        showlegend=False,
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            bgcolor='whitesmoke'
        ),
        margin=dict(t=50)  # mniejszy margines
    )

    fig = go.Figure(data=[trace_edges, trace_nodes], layout=layout)
    fig.show()