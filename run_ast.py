from n_puzzle_base import NPuzzleBase

N = 15

n_puzzle = NPuzzleBase(N)
matrix = n_puzzle.matrix
flatten_matrix = list(i for j in matrix for i in j)
flatten_matrix_str = str(flatten_matrix).replace('[', '')
flatten_matrix_str = str(flatten_matrix_str).replace(']', '')


with open('input_matrix.txt', 'w') as f:
    f.write(flatten_matrix_str)
