import networkx as nx
from matplotlib import pyplot as plt

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
    plt.figure(figsize=[FRAME_WIDTH, FRAME_HEIGHT], facecolor='whitesmoke')
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
        pos = nx.spring_layout(layout_graph, k=2.5, iterations=150, seed=7)
    elif FORM == 'kamada':
        pos = nx.kamada_kawai_layout(layout_graph)
    elif FORM == 'circular':
        pos = nx.circular_layout(weighted_graph)
    else:
        raise ValueError("Niepoprawny FORM. Wybierz 'spring', 'kamada' lub 'circular'.")

    nx.draw_networkx_nodes(weighted_graph, pos, node_size=1300, node_color='cadetblue')
    nx.draw_networkx_labels(weighted_graph, pos, font_size=7, font_weight='bold', font_family='Arial', font_color='white')

    edges = [(u, v, d['weight']) for u, v, d in weighted_graph.edges(data=True) if d['weight'] >= THRESHOLD]

    for u, v, w in edges:
        norm_w = (w - THRESHOLD) / (1 - THRESHOLD) if (1 - THRESHOLD) > 0 else 1

        nx.draw_networkx_edges(weighted_graph, pos, edgelist=[(u, v)], width=1 + (norm_w * 8), alpha=0.2 + (norm_w * 0.6),
            edge_color=plt.cm.GnBu(norm_w), edge_cmap=plt.cm.GnBu)

    plt.axis('off')
    plt.show()