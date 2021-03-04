import random
import math
import numpy as np

from loguru import logger


class NPuzzleBase():
    def __init__(self, n):
        self.n = n
        self.n_1 = self.n + 1
        self.n_root = int(math.sqrt(self.n_1))
        self.matrix = self.create_input_matrix()
        self.target_matrix = self.create_target_matrix()

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

    def create_target_matrix(self) -> np.ndarray:
        target_matrix = list(np.arange(1, self.n_1))
        target_matrix.append(0)
        target_matrix = np.reshape(target_matrix, (self.n_root, self.n_root))

        return target_matrix

    def check_if_is_target_matrix(self) -> bool:
        comparison = self.matrix == self.target_matrix
        if comparison.all():
            return True
        return False

    @staticmethod
    def is_even(number: int) -> bool:
        if (number % 2) == 0:
            return True
        return False

    def check_if_solvable(self) -> bool:
        flatten_matrix = list(i for j in self.matrix for i in j if i != 0)

        # Counting number of inversions
        counter_inv = 0
        # Getting current number
        for i in range(len(flatten_matrix)):
            current_num = flatten_matrix[i]

            # Comparing following numbers with current number
            for j in range(i, len(flatten_matrix)):
                next_num = flatten_matrix[j]
                if next_num < current_num:
                    counter_inv += 1

        n_is_even = self.is_even(self.n)
        counter_inv_is_even = self.is_even(counter_inv)
        # If n is even, counter_inv needs to be even
        if n_is_even:
            if counter_inv_is_even:
                return True
        # If n is odd...
        else:
            i, _ = self.find_index(self.matrix)
            # Row starting from bottom and at 1
            row_blank_from_bottom = len(self.matrix) - i
            row_from_botton_is_even = self.is_even(row_blank_from_bottom)

            # If index from bottom is even, counter_inv needs to be odd
            if row_from_botton_is_even:
                if not counter_inv_is_even:
                    return True
            # If index from bottom is odd, counter_inv needs to be even
            else:
                if counter_inv_is_even:
                    return True
        return False

    def check_both_conditions(self) -> bool:
        if not self.check_if_is_target_matrix():
            if self.check_if_solvable():
                logger.debug("Matriz de entrada COM solução.")
                return True
            logger.warning("Matriz de entrada SEM solução.")
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
        if j != len(matrix) - 1:
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
