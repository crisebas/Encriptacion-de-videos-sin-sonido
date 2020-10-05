import numpy as np

def permutation(row_list, column_list, matrix):
    row, column = matrix.shape

    matrix = rotate_rows(row_list, matrix)
    matrix = rotate_columns(column_list, matrix)

    return matrix

def rotate_rows(row_list, matrix):
    result = np.empty_like(matrix)
    row, column = matrix.shape
    for i in range(row):
        step = row_list[i+2] % column
        for j in range(step, step+column):
            result[i][j%column] = matrix[i][j-step]
    
    return result

def rotate_columns(column_list, matrix):
    result = np.empty_like(matrix)
    row, column = matrix.shape
    for j in range(column):
        step = column_list[j+2] % row
        for i in range(step, step+row):
            result[i%row][j] = matrix[i-step][j]

    return result
