import matplotlib.pyplot as plt
import networkx as nx
from scipy.cluster.hierarchy import dendrogram, linkage

# ... (Twoja pętla generująca similarity_matrix_np) ...

# =========================================================
# WIZUALIZACJA 1: DENDROGRAM (HIERARCHIA RODZIN)
# =========================================================
plt.figure(figsize=(15, 10), facecolor='whitesmoke')
plt.title("Hierarchiczne Klastrowanie Języków Europejskich (i nie tylko)", fontsize=16)

# Metoda 'ward' minimalizuje wariancję w klastrach - daje najładniejsze "drzewka"
# Używamy 1 - similarity, bo linkage wymaga "dystansu" (im mniej tym bliżej),
# a my mamy "podobieństwo" (im więcej tym bliżej).
linked = linkage(1 - similarity_matrix_np, 'ward')

dendrogram(linked,
           orientation='right',
           labels=[l.capitalize() for l in languages_list],
           distance_sort='descending',
           show_leaf_counts=True,
           leaf_font_size=12)

plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# =========================================================
# WIZUALIZACJA 2: GRAF SIECIOWY (KNN - Nearest Neighbors)
# =========================================================
plt.figure(figsize=(18, 16), facecolor='#f0f0f0')

G = nx.Graph()

# Dodajemy węzły
for lang in languages_list:
    G.add_node(lang.capitalize())

# LOGIKA RYSOWANIA KRAWĘDZI:
# Zamiast sztywnego progu (bo wszystko jest > 90%),
# łączymy każdy język TYLKO z jego 2 najbliższymi sąsiadami.
# To stworzy czystą mapę powiązań.

edges = []
for i, lang_a in enumerate(languages_list):
    # Sortujemy podobieństwa dla danego języka
    # argsort() daje indeksy od najmniejszego do największego
    # [-1] to on sam (100%), [-2] to 1. sąsiad, [-3] to 2. sąsiad
    sorted_indices = similarity_matrix_np[i].argsort()

    # Bierzemy 2 najlepszych przyjaciół (możesz zmienić na 3, jeśli graf będzie zbyt rzadki)
    best_friends = sorted_indices[-3:-1]

    for neighbor_idx in best_friends:
        lang_b = languages_list[neighbor_idx]
        weight = similarity_matrix_np[i][neighbor_idx]

        # Dodajemy krawędź (NetworkX sam usunie duplikaty A->B i B->A)
        edges.append((lang_a.capitalize(), lang_b.capitalize(), weight))

# Dodajemy krawędzie do grafu
G.add_weighted_edges_from(edges)

# Obliczamy układ (Kamada-Kawai jest świetny do takich struktur)
pos = nx.kamada_kawai_layout(G)

# Rysowanie
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='steelblue', edgecolors='white')
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='white')

# Rysujemy krawędzie z dynamicznym kolorem
all_weights = [data['weight'] for u, v, data in G.edges(data=True)]

nx.draw_networkx_edges(G, pos,
                       width=2,
                       edge_color=all_weights,
                       edge_cmap=plt.cm.Reds,  # Kolor od jasnego do czerwonego
                       edge_vmax=1.0,
                       edge_vmin=0.90)  # Skalujemy kolory w zakresie 90-100%

plt.title("Sieć Najbliższych Sąsiadów (k-NN Graph)", fontsize=16)
plt.axis('off')
plt.show()