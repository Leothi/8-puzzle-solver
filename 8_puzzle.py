from n_puzzle_base import NPuzzleBase

if __name__ == '__main__':
    eight_puzzle = NPuzzleBase(15)
    matrix = eight_puzzle.matrix
    print(matrix)
    
    if eight_puzzle.check_both_conditions():
        print(eight_puzzle.move_down(matrix))
