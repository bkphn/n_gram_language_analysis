import math
import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def edge_color(weight, THRESHOLD):
    threshold_diff = 1 - THRESHOLD


    if weight > THRESHOLD + (threshold_diff * 4 / 5):
        color = 'darkslategray'
    elif weight > THRESHOLD + (threshold_diff * 3 / 5):
        color = 'teal'
    elif weight > THRESHOLD + (threshold_diff * 2 / 5):
        color = 'darkturquoise'
    elif weight > THRESHOLD + (threshold_diff * 1 / 5):
        color = 'lightskyblue'
    else:
        color = 'paleturquoise'

    return color

def draw_graph(FRAME_WIDTH, FRAME_HEIGHT, similarity_matrix_np, languages_list, THRESHOLD, FORM):
    figure, ax = plt.subplots(figsize=[FRAME_WIDTH, FRAME_HEIGHT], facecolor='white')
    weighted_graph = nx.from_numpy_array(similarity_matrix_np)

    nodes_mapping = {i: lang.capitalize() for i, lang in enumerate(languages_list)}
    weighted_graph = nx.relabel_nodes(weighted_graph, nodes_mapping)

    layout_graph = weighted_graph.copy()

    edges_to_remove = []
    for node1, node2, d in layout_graph.edges(data=True):
        if d['weight'] < THRESHOLD:
            edges_to_remove.append((node1, node2))

    layout_graph.remove_edges_from(edges_to_remove)

    if FORM == 'spring':
        pos = nx.spring_layout(layout_graph, k=4.0, iterations=200, seed=7)

        min_dist = 0.3
        for _ in range(100):
            for n1 in pos:
                for n2 in pos:
                    if n1 != n2:
                        dx = pos[n1][0] - pos[n2][0]
                        dy = pos[n1][1] - pos[n2][1]
                        dist = math.sqrt(dx ** 2 + dy ** 2)

                        if dist < min_dist:
                            if dist == 0:
                                import numpy as np
                                dx, dy = np.random.rand() - 0.5, np.random.rand() - 0.5
                                dist = math.sqrt(dx ** 2 + dy ** 2)

                            push = (min_dist - dist) / 2
                            pos[n1][0] += (dx / dist) * push
                            pos[n1][1] += (dy / dist) * push
                            pos[n2][0] -= (dx / dist) * push
                            pos[n2][1] -= (dy / dist) * push
    elif FORM == 'kamada':
        pos = nx.kamada_kawai_layout(layout_graph)
    elif FORM == 'circular':
        pos = nx.circular_layout(weighted_graph)
    else:
        raise ValueError("Niepoprawny FORM. Wybierz 'spring', 'kamada' lub 'circular'.")

    nx.draw_networkx_nodes(weighted_graph, pos, node_size=1400, node_color='cadetblue')
    nx.draw_networkx_labels(weighted_graph, pos, font_size=7, font_family='serif', font_color='black')

    edges = [(u, v, d['weight']) for u, v, d in weighted_graph.edges(data=True) if d['weight'] >= THRESHOLD]

    for u, v, w in edges:
        norm_w = (w - THRESHOLD) / (1 - THRESHOLD) if (1 - THRESHOLD) > 0 else 1

        nx.draw_networkx_edges(weighted_graph, pos, edgelist=[(u, v)], width=1 + (norm_w * 8), alpha=0.2 + (norm_w * 0.6),
            edge_color=plt.cm.GnBu(norm_w), edge_cmap=plt.cm.GnBu)

    plt.axis('off')

    sm = plt.cm.ScalarMappable(cmap=plt.cm.GnBu, norm=mcolors.Normalize(vmin=THRESHOLD, vmax=1.0))
    sm.set_array([])

    cbar = plt.colorbar(sm, ax=ax, shrink=0.6, pad=0.02, aspect=30)
    cbar.set_label('Cosine similarity ($S_C$)', rotation=270, labelpad=20, fontsize=12, fontfamily='serif')

    plt.savefig(os.path.join("Raports", "graph.pdf"), format="pdf", bbox_inches="tight")
    print("Pomyślnie wygenerowano plik: graph.pdf")

    plt.show()