from time import gmtime, strftime
import os
import sys

import numpy as np
from gensim.models import Word2Vec

from preprocessing import bound_words, generate_datasets, generate_ngrams
from generate_vectors import words_centroids, language_centroids
from utilities import raport, clear_raport, raport_only
from files_normalization import normalize
from graphs import draw_graph
from matricies import generate_similarity_matrix
from clusters import affinity_propagation
from characteristics import characterise_clusters

# ----- MODEL SETTINGS -----
N_GRAM_SIZE = 3
NORMALIZATION = False
EPOCHS = 60
VECTOR_SIZE = 300
TRAIN_MODEL = True
MODEL_VERSION = "language_ngrams_v4_n3_e60"

# ----- GRAPH SETTINGS -----
THRESHOLD = 0.96
FORM = 'spring' # (circular/spring/kamada)
FRAME_WIDTH = 15
FRAME_HEIGHT = 15
SHOW_GRAPH = True

# ----- CLUSTER SETTINGS -----
CLUSTER_PREFERENCE = 90
SEPARATE_LANGUAGES = False
SKIP_SINGLE_LANGUAGES = False

# ----- CMD COLOR SETTINGS -----
RED = '\033[91m \x1B[3m'
YELLOW = '\033[93m \x1B[3m'
GREEN = '\033[92m \x1B[3m'
RESET = '\033[0m \x1B[0m'

# ----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    clear_raport()
    date = strftime("%d.%m.%Y %H:%M:%S", gmtime())
    raport_only(f"---- RAPORT Z DNIA {date} ----")

    languages_list = ["albanian", "basque", "bosnian","catalan", "croatian", "czech",
                      "danish", "dutch", "english", "estonian", "finnish",
                      "french", "galician", "german", "hungarian", "icelandic",
                      "indonesian", "italian", "latvian", "lithuanian", "malay",
                      "norwegian", "polish", "portuguese", "serbian",
                      "slovak", "spanish", "swedish", "turkish"]
    datasets = {}

    model_path = os.path.join("Models", MODEL_VERSION + ".model")

    if NORMALIZATION:
        for language in languages_list:
            normalize(language)

    generate_datasets(languages_list, datasets)
    training_data = []

    print(f"\n{GREEN}Trwa preprocessing słów...{RESET}")
    for language in languages_list:
        bound_words(datasets[language])
    print(f"{GREEN}Preprocessing zakończony sukcesem.{RESET}\n")

    if TRAIN_MODEL:

        print(f"{GREEN}Przygotowywanie danych treningowych...{RESET}")
        for language in languages_list:
            training_data += (generate_ngrams(datasets[language], n=N_GRAM_SIZE))
        print(f"{GREEN}Przygotowanie zakończone sukcesem.{RESET}\n")

        print(f"{GREEN}Trwa trenowanie modelu...{RESET}")
        model = Word2Vec(sentences=training_data, vector_size=VECTOR_SIZE, window=N_GRAM_SIZE, min_count=1, sg=1, workers=4, epochs=EPOCHS)
        model.save(model_path)
        print(f"{GREEN}Trening {MODEL_VERSION}.model zakończony sukcesem.{RESET}\n")

    else:
        if os.path.exists(model_path):
            print(f"{GREEN}Wczytuję model z pliku...{RESET}")
            model = Word2Vec.load(model_path)
            print(f"{GREEN}Model wczytany poprawnie.{RESET}")
        else:
            print(f"{RED}BŁĄD: Model '{model_path}' nie istnieje!{RESET}")
            sys.exit()

    print(f"{GREEN}\nGeneruję wektory językowe...{RESET}")
    words_vectors = {}
    language_vectors = {}
    for language in languages_list:
        words_vectors[language] = words_centroids(language, model, datasets, n=N_GRAM_SIZE)
        language_vectors[language] = language_centroids(words_vectors[language], model)
    print(f"{GREEN}Pomyślnie wygenerowano wektory językowe.{RESET}")

    print(f"{GREEN}\nGeneruję macierz podobieństwa...{RESET}")
    similarity_matrix = generate_similarity_matrix(languages_list, language_vectors)
    similarity_matrix_np = np.array(similarity_matrix)
    print(f"{GREEN}Macierz wygenerowana pomyślnie.{RESET}")

    if SHOW_GRAPH:
        print(f"\n{GREEN}Generuję graf...{RESET}")
        draw_graph(FRAME_WIDTH, FRAME_HEIGHT, similarity_matrix_np, languages_list, THRESHOLD, FORM)
        print(f"{GREEN}Graf wygenerowany pomyślnie.{RESET}\n")
    else:
        print(f"{YELLOW}Pomijam generowanie grafu.{RESET}")

    print(f"\n{GREEN}Dzielę języki na klastry...{RESET}\n")
    clusters = affinity_propagation(similarity_matrix_np, languages_list, CLUSTER_PREFERENCE, SEPARATE_LANGUAGES)
    print(f"{GREEN}Pomyślnie utworzono klastry.{RESET}")

    print(f"\n{GREEN}Szukam charakterystyk dla grup językowych...{RESET}")
    characterise_clusters(clusters, datasets, SKIP_SINGLE_LANGUAGES)
    print(f"{GREEN}Pomyślnie scharakteryzowano grupy językowe.{RESET}")