import numpy as np
from math import ceil, floor

def diffusion_process(row_list, column_list, matrix, A):
    row, column = matrix.shape
    d = ceil(column/2)
    v = floor(column/2)

    D = np.array([[(matrix[i][j] + A[row-1-i][d-1-j]) % 256 for j in range(d)] for i in range(row)])
    E = np.array([[(D[i][j] + A[i][column-1-j]) % 256 for j in range(d)] for i in range(row)])
    F = np.array([[(E[i][j] + matrix[row-1-i][column-1-j]) % 256 for j in range(v)] for i in range(row)])

    C = np.concatenate((E, F), axis=1)
   
    return C

def diffusion_matrix(row_list, column_list, row, column):
    row_matrix, column_matrix = [], []

    for i in range(2, column+2):
        row_matrix.append(row_list[i])
    
    for i in range(2, row+2):
        column_matrix.append(column_list[i])
    
    column_matrix = np.array(column_matrix).reshape(row, 1)
    row_matrix = np.array(row_matrix).reshape(1, column)

    return column_matrix*row_matrix
