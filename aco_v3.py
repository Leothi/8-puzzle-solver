import sys
import random
import pandas as pd
import numpy as np

from logger import DEFAULT_FORMAT
from loguru import logger

from n_puzzle_base import NPuzzleBase

# Configuração do Logger
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": 10,
            "format": DEFAULT_FORMAT
        }
    ]
)


N = 8
# Saída para arquivo logger
logger.add(f'./logs/{N}_puzzle_aco.log', level=0, format=DEFAULT_FORMAT)
logger.add(f'./logs/{N}_puzzle_aco_info.log', level=20, format=DEFAULT_FORMAT)
logger.add(f'./logs/{N}_puzzle_aco_stats.log', level=38, format=DEFAULT_FORMAT)


# Criação de Levels
logger.level(f"STATISTICS", no=38, color="<light-green>")

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

    def get_index_from_list(self, matrix, to_find):
        flatten_matrix = list(i for j in matrix for i in j)
        index = flatten_matrix.index(to_find)

        return index

    def get_value_from_index(self, matrix, index):
        flatten_matrix = list(i for j in matrix for i in j)
        value = flatten_matrix[index]

        return value

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

    def update_phero(self, old_phero, delta_phero):
        return old_phero + delta_phero

    def apply_evaporation(self, phero, factor):
        return (1 - factor) * phero

    def get_diff_from_target(self, input_matrix):
        comparison = input_matrix == self.target_matrix
        diff_index_tuple = np.where(comparison == False)
        len_index_tuple = len(input_matrix[diff_index_tuple])
        return diff_index_tuple, len_index_tuple

    @classmethod
    def solve(cls, self, matrix):
        current_matrix = matrix
        diff_index, n = self.get_diff_from_target(current_matrix)

        counter = 0
        while n != 0:
            counter += 1
            logger.debug(current_matrix)

            diff_nums = current_matrix[diff_index]
            logger.debug(diff_nums)
            for diff_num in diff_nums:
                logger.debug(f"Num: {diff_num}")
                index = self.get_index_from_list(current_matrix, diff_num)

                for move in self.actions:
                    temp_data = self.move_tile(move, current_matrix, diff_num)
                    if temp_data is not None:
                        logger.debug(f'index: {index}')
                        logger.debug(move)
                        diff_index, n = self.get_diff_from_target(temp_data)
                        logger.debug(f"N: {n}")

                        old_phero = self.phero_matrix[move][index]
                        if old_phero == 0:
                            old_phero += 1
                        logger.debug(f"old: {old_phero}")
                        phero_delta = self.calculate_delta_phero(n)
                        logger.debug(f'delta: {phero_delta}')
                        phero_updated = self.update_phero(
                            old_phero, phero_delta)
                        logger.debug(f'updated: {phero_updated}')
                        phero_evaporated = self.apply_evaporation(
                            phero_updated, 0.2)
                        logger.debug(f'phero_evaporated: {phero_evaporated}')

                        self.phero_matrix[move][index] = phero_evaporated
                        logger.debug(self.phero_matrix)
                        logger.debug('-------------')

            # logger.debug('-------------')
            list_biggest = self.get_biggest_phero_matrix()
            logger.debug(list_biggest)
            logger.debug(current_matrix)
            while current_matrix is not None:
                random_num = random.randint(0, len(list_biggest)-1)
                num, move = list_biggest[random_num]

                logger.debug(f"{num}, {move}")
                value = self.get_value_from_index(current_matrix, num)
                logger.debug(value)
                current_matrix = self.move_tile(move, current_matrix, value)
                if current_matrix is not None:
                    logger.debug('ok')
                    logger.debug('-------------')
                    diff_index, n = self.get_diff_from_target(current_matrix)
                    break

            # PARADA
            if counter == 5:
                n = 0
            # n=0
        return self.phero_matrix


if __name__ == '__main__':
    aco = ACOSolver(N)
    matrix = aco.matrix
    print("Matriz de entrada\n", matrix)
    print("Matriz target\n", aco.target_matrix)

    # if aco.check_both_conditions():
    df_phero = aco.solve(aco, matrix)
