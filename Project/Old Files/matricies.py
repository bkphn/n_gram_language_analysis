import numpy as np

def generate_adjacency_matrix(matrix, threshold):
    matrix_np = np.array(matrix)

    adj_matrix = (matrix_np >= threshold).astype(int)
    np.fill_diagonal(adj_matrix, 0)

    return adj_matrix

def generate_degree_matrix(matrix):
    degrees = np.sum(matrix, axis=1)
    return np.diag(degrees)
