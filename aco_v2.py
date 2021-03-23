import pandas as pd
import numpy as np

from n_puzzle_base import NPuzzleBase


N = 8


class ACOSolver(NPuzzleBase):
    actions = ["down", "up", "left", "right"]

    def __init__(self, n):
        super().__init__(n)
        self.phero_matrix = self.create_phero_matrix()

    def create_phero_matrix(self):
        df = pd.DataFrame(np.zeros((self.n_1, len(self.actions))),
                          columns=self.actions)

        return df

    @classmethod
    def move_tile(cls, action, data, to_find):
        if action == 'up':
            return cls.move_up(data, to_find)
        if action == 'down':
            return cls.move_down(data, to_find)
        if action == 'left':
            return cls.move_left(data, to_find)
        if action == 'right':
            return cls.move_right(data, to_find)
        else:
            return None

    def get_biggest_phero_matrix(self):
        max_value = self.phero_matrix.to_numpy().max()
        columns = self.phero_matrix.columns

        list_biggest = []
        for index, row in self.phero_matrix.iterrows():
            for column in columns:
                if row[column] == max_value:
                    list_biggest.append((index, column))
        return list_biggest

    def calculate_delta_phero(self, n):
        if n != 0:
            return self.n_1 / n
        return 0

    def apply_evaporation(self, phero, factor):
        return (1 - factor) * phero

    def update_phero(self, old_phero, delta_phero):
        return old_phero + delta_phero

    def get_diff_from_target(self, input_matrix):
        comparison = input_matrix == self.target_matrix
        diff_index_tuple = np.where(comparison == False)
        len_index_tuple = len(input_matrix[diff_index_tuple])
        return diff_index_tuple, len_index_tuple

    def solve(self, matrix):
        current_matrix = matrix
        diff_index, n = self.get_diff_from_target(current_matrix)

        counter = 0
        while n != 0:
            counter += 1
            print(current_matrix)

            for diff_num in current_matrix[diff_index]:
                print(diff_num)

                for move in self.actions:
                    temp_data = self.move_tile(move, current_matrix, diff_num)
                    if temp_data is not None:
                        print(move)
                        diff_index, n = self.get_diff_from_target(temp_data)
                        print("N:", n)

                        old_phero = self.phero_matrix[move][diff_num]
                        if old_phero == 0:
                            old_phero += 1
                        print('old:', old_phero)
                        phero_delta = self.calculate_delta_phero(n)
                        print('delta:', phero_delta)
                        phero_updated = self.update_phero(
                            old_phero, phero_delta)
                        print('updated:', phero_updated)
                        phero_evaporated = self.apply_evaporation(
                            phero_updated, 0.2)
                        print('phero_evaporated:', phero_evaporated)

                        self.phero_matrix[move][diff_num] = phero_evaporated

                        print('-------------')
            print(self.phero_matrix)
            list_biggest = self.get_biggest_phero_matrix()
            print(list_biggest)
            for tuple in list_biggest:

                num, move = tuple
                current_matrix = self.move_tile(move, current_matrix, num)
                if current_matrix is not None:
                    print(num, move)
                    print('-------------')
                    diff_index, n = self.get_diff_from_target(current_matrix)
                    break

            # PARADA
            if counter == 10:
                n = 0
            # n=0
        return self.phero_matrix


if __name__ == '__main__':
    aco = ACOSolver(N)
    matrix = aco.matrix
    print("Matriz de entrada\n", matrix)

    if aco.check_both_conditions():
        df_phero = aco.solve(matrix)
        # print('------------')
        # print(df_phero)
