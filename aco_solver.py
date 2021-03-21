import numpy as np

from n_puzzle_base import NPuzzleBase


N = 8

class ACOSolver(NPuzzleBase):
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
        
    def calculate_delta_phero(self, n):
        if n != 0:
            return self.n_1 / n
        return 0
    
    def apply_evaporation(self, phero, factor):
        return (1 - factor) * phero
        
    def get_diff_from_target(self, input_matrix):
        comparison = input_matrix == self.target_matrix
        diff_index_tuple = np.where(comparison == False)
        len_index_tuple = len(input_matrix[diff_index_tuple])
        return diff_index_tuple, len_index_tuple
    
    
    def solve(self, matrix):
        ant_num = 0
        actions = ["down", "up", "left", "right"]
        
        current_matrix = matrix
        diff_index_from_target, n = self.get_diff_from_target(current_matrix)
        
        counter = 0
        while n != 0:
            counter += 1
            biggest_phero = 0
            biggest_data = 0
            
            for diff_num in current_matrix[diff_index_from_target]:
                print(diff_num)
                
                for move in actions:
                    temp_data = self.move_tile(move, current_matrix, diff_num)
                    if temp_data is not None:
                        print(move)
                        print(temp_data)
                        ant_num += 1
                        diff_index_from_target, n = self.get_diff_from_target(temp_data)
                        print("N =", n)
                        
                        delta_phero = self.calculate_delta_phero(n)
                        phero_evaporated = self.apply_evaporation(delta_phero, 0.2)
                        print("Phero", phero_evaporated)
                        if phero_evaporated > biggest_phero:
                            biggest_phero = phero_evaporated
                            biggest_data=temp_data
                        print('--------')
                            
                print('----------------------')
            
                print(biggest_data)
                print(biggest_phero)
                print('--------------------------------------------')
            print(
                '--------------------------------------------------------------------------------')
            print(biggest_data)
            print(biggest_phero)
            current_matrix = biggest_data
            diff_index_from_target, n = self.get_diff_from_target(current_matrix)
            
            # PARADA
            if counter == 50000:
                n=0
            # n=0
        return diff_index_from_target, n
    
if __name__ == '__main__':
        aco = ACOSolver(N)
        matrix = aco.matrix
        print("Matriz de entrada\n", matrix)
        
        if aco.check_both_conditions():
            tupla, len_ = aco.solve(matrix)
            # print(tupla, len_)
