import numpy as np
from sklearn.cluster import AffinityPropagation
from collections import defaultdict

PURPLE = '\033[95m'
BLUE = '\033[94m'
RESET = '\033[0m'

def affinity_propagation(similarity_matrix_np, languages_list, cluster_preference=90, separate_languages=False):
    if separate_languages:
        cluster_preference = 100

    preference = np.percentile(similarity_matrix_np, cluster_preference)

    cluster = AffinityPropagation(affinity='precomputed', preference=preference, random_state=13)
    labels = cluster.fit_predict(similarity_matrix_np)
    cluster_centers_indices = cluster.cluster_centers_indices_

    groups = defaultdict(list)
    for lang, label in zip(languages_list, labels):
        groups[label].append(lang.capitalize())

    for cluster_id, langs in sorted(groups.items()):
        exemplar = languages_list[cluster_centers_indices[cluster_id]].capitalize()
        members = [lang for lang in sorted(langs)]

        if len(members) == 1:
            print(f"{PURPLE}LIDER GRUPY: {exemplar.upper()}{RESET}")
            print(f"{PURPLE}Język izolowany{RESET}")
        else:
            print(f"{BLUE}LIDER GRUPY: {exemplar.upper()}")
            print("Członkowie grupy: " + ", ".join(members) + f"{RESET}")
        print("-" * 100)

    return groups