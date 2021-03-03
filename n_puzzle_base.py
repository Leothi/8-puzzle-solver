import random
import math
import numpy as np


class NPuzzleBase():
    def __init__(self, n):
        self.n = n
        self.n_1 = self.n + 1
        self.n_root = int(math.sqrt(self.n_1))
        self.matrix = self.create_input_matrix()

    # @staticmethod
    # def create_user_input_matrix() -> np.ndarray:
    #     print("Digite os números de cada linha da matriz, separando-os por espaço")

    #     print("Linha 1:", )
    #     a = [int(x) for x in input().split()]
    #     print("Linha 2:", )
    #     b = [int(x) for x in input().split()]
    #     print("Linha 3")
    #     c = [int(x) for x in input().split()]

    #     return np.vstack((a, b, c))

    def create_input_matrix(self) -> np.ndarray:
        random_numbers = random.sample(range(0, self.n_1), self.n_1)
        matrix = np.reshape(random_numbers, (self.n_root, self.n_root))

        return matrix

    def check_if_is_target_matrix(self) -> bool:
        target_matrix = list(np.arange(1, self.n_1))
        target_matrix.append(0)
        target_matrix = np.reshape(target_matrix, (self.n_root, self.n_root))

        comparison = self.matrix == target_matrix
        if comparison.all():
            return True
        return False

    def check_if_solvable(self) -> bool:
        flatten_matrix = list(i for j in self.matrix for i in j if i != 0)

        counter_inv = 0
        # Getting current number
        for i in range(len(flatten_matrix)):
            current_num = flatten_matrix[i]

            # Comparing following numbers with current number
            for j in range(i, len(flatten_matrix)):
                next_num = flatten_matrix[j]
                if next_num < current_num:
                    counter_inv += 1

        if (counter_inv % 2) == 0:
            return True
        return False

    def check_both_conditions(self) -> bool:
        if not self.check_if_is_target_matrix():
            if self.check_if_solvable():
                print("Matriz de entrada COM solução.")
                return True
            print("Matriz de entrada SEM solução.")
        return False

    @ classmethod
    def find_index(cls, matrix: np.ndarray) -> tuple:
        # Line and colummn where 0 (blank tile) is
        i, j = np.where(matrix == 0)

        return int(i), int(j)

    @ classmethod
    def move_left(cls, matrix: np.ndarray) -> np.ndarray:
        # Finding blank tile
        i, j = cls.find_index(matrix)

        # If blank tile is not in left column
        if j != 0:
            temp_arr = np.copy(matrix)
            # Swap blank tile with left tile
            temp_arr[i, j] = temp_arr[i, j-1]
            # Swapped tile = blank tile
            temp_arr[i, j-1] = 0

            return temp_arr
        return None

    @ classmethod
    def move_right(cls, matrix: np.ndarray) -> np.ndarray:
        # Finding blank tile
        i, j = cls.find_index(matrix)

        # If blank tile is not in right column
        if j != len(matrix) -1:
            temp_arr = np.copy(matrix)
            # Swap blank tile with right tile
            temp_arr[i, j] = temp_arr[i, j+1]
            # Swapped tile = blank tile
            temp_arr[i, j+1] = 0

            return temp_arr
        return None

    @ classmethod
    def move_up(cls, matrix: np.ndarray) -> np.ndarray:
        # Finding blank tile
        i, j = cls.find_index(matrix)

        # If blank tile is not in first line
        if i != 0:
            temp_arr = np.copy(matrix)
            # Swap blank tile with up tile
            temp_arr[i, j] = temp_arr[i-1, j]
            # Swapped tile = blank tile
            temp_arr[i-1, j] = 0

            return temp_arr
        return None

    @ classmethod
    def move_down(cls, matrix: np.ndarray) -> np.ndarray:
        # Finding blank tile
        i, j = cls.find_index(matrix)

        # If blank tile is not in last line
        if i != len(matrix)-1:
            temp_arr = np.copy(matrix)
            # Swap blank tile with down tile
            temp_arr[i, j] = temp_arr[i+1, j]
            # Swapped tile = blank tile
            temp_arr[i+1, j] = 0

            return temp_arr
        return None
