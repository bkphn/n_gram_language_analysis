from preprocessing import generate_ngrams
from numpy import mean, zeros
from pyexpat import model


def words_centroids(language, model, datasets, n):
    dataset = datasets[language]

    language_vectors = []
    for word in dataset:
        ngrams = generate_ngrams([word], n)[0]
        word_vectors = []

        for ngram in ngrams:
            if ngram in model.wv:
                word_vectors.append(model.wv[ngram])

        if len(word_vectors) > 0:
            centroid = mean(word_vectors, axis=0)

        else:
            centroid = zeros(model.vector_size)

        language_vectors.append(centroid)

    return language_vectors

def language_centroids(words_vec, model):
    if len(words_vec) > 0:
        centroid = mean(words_vec, axis=0)
    else:
        centroid = zeros(model.vector_size)

    return centroid