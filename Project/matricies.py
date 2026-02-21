from sklearn.metrics.pairwise import cosine_similarity

from utilities import raport


def generate_similarity_matrix(languages_list, language_vectors):
    language_amount = len(languages_list)
    similarity_matrix = [[None for _ in range(language_amount)] for _ in range(language_amount)]

    i = 0
    for language in languages_list:
        j = 0

        raport(f"\n{language}".upper() + " SIMILARITY:")
        vec_1 = language_vectors[language].reshape(1, -1)

        for l in languages_list:

            vec_2 = language_vectors[l].reshape(1, -1)
            cos_sim = cosine_similarity(vec_1, vec_2)[0][0]

            sim = cos_sim * 100
            raport(f"{l}: {sim:.3f}%")

            if i != j:
                similarity_matrix[i][j] = cos_sim
            else:
                similarity_matrix[i][j] = 0

            j += 1
        i += 1

    return similarity_matrix