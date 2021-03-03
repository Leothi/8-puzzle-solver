import random
import numpy as np


class EightPuzzle:
    @staticmethod
    def create_user_input_matrix():
        print("Digite os números de cada linha da matriz, separando-os por espaço")
        print("Linha 1:", )
        a = [int(x) for x in input().split()]
        print("Linha 2:", )
        b = [int(x) for x in input().split()]
        print("Linha 3")
        c = [int(x) for x in input().split()]
        return (np.vstack((a, b, c)))

    @staticmethod
    def create_input_matrix() -> np.ndarray:
        random_numbers = random.sample(range(0, 9), 9)
        matrix = np.reshape(random_numbers, (3, 3))

        return matrix

    @staticmethod
    def check_if_is_target_matrix(matrix: np.ndarray) -> bool:
        target_matrix = list(np.arange(1, 9))
        target_matrix.append(0)
        target_matrix = np.reshape(target_matrix, (3, 3))

        comparison = matrix == target_matrix
        if comparison.all():
            return True
        return False

    @staticmethod
    def check_if_solvable(matrix: np.ndarray) -> bool:
        flatten_matrix = list(i for j in matrix for i in j if i != 0)

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

    @classmethod
    def check_both_conditions(cls, matrix: np.ndarray) -> bool:
        if cls.check_if_is_target_matrix(matrix):
            print("Matriz de entrada igual à objetivo.")
        elif cls.check_if_solvable(matrix):
            print("Matriz de entrada sem solução.")
        return False


if __name__ == '__main__':
    matrix = EightPuzzle.create_user_input_matrix()
    EightPuzzle.check_both_conditions(matrix)
