import sys
import numpy as np
import time
import uuid

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
logger.add(f'./logs/{N}_puzzle_bfs.log', level=0, format=DEFAULT_FORMAT)
logger.add(f'./logs/{N}_puzzle_bfs_info.log', level=20, format=DEFAULT_FORMAT)
logger.add(f'./logs/{N}_puzzle_bfs_stats.log', level=38, format=DEFAULT_FORMAT)


# Criação de Levels
logger.level(f"STATISTICS", no=38, color="<light-green>")


class Node:
    def __init__(self, node_no, data, parent, act):
        self.node_no = node_no
        self.data = data
        self.parent = parent
        self.act = act


class BFSSolver(NPuzzleBase):
    @classmethod
    def move_tile(cls, action, data):
        if action == 'up':
            return cls.move_up(data)
        if action == 'down':
            return cls.move_down(data)
        if action == 'left':
            return cls.move_left(data)
        if action == 'right':
            return cls.move_right(data)
        else:
            return None

    def solve(self, node):
        logger.debug("Solucionando...")
        actions = ["down", "up", "left", "right"]
        goal_node = self.target_matrix
        node_q = [node]
        final_nodes = []
        visited = []

        # Only writing data of nodes in seen
        final_nodes.append(node_q[0].data.tolist())
        node_counter = 0  # To define a unique ID to all the nodes formed

        while node_q:
            current_root = node_q.pop(0)  # Pop the element 0 from the list
            if current_root.data.tolist() == goal_node.tolist():
                logger.success("Problema solucionado.")
                return current_root, final_nodes, visited

            for move in actions:
                temp_data = self.move_tile(move, current_root.data)
                if temp_data is not None:
                    node_counter += 1
                    child_node = Node(node_counter, np.array(temp_data),
                                      current_root, move)  # Create a child node

                    if child_node.data.tolist() not in final_nodes:
                        node_q.append(child_node)
                        # Add the child node data in final node list
                        final_nodes.append(child_node.data.tolist())
                        visited.append(child_node)
                        if child_node.data.tolist() == goal_node.tolist():
                            logger.success("Problema solucionado.")
                            return child_node, final_nodes, visited
        return None, None, None  # return statement if the goal node is not reached


if __name__ == '__main__':
    for _ in range(50):
        logger.info(f"Iniciando {N}-Puzzle BFS")

        bfs = BFSSolver(N)
        matrix = bfs.matrix
        flatten_matrix = list(i for j in matrix for i in j)
        flatten_matrix_str = str(flatten_matrix).replace('[', '')
        flatten_matrix_str = str(flatten_matrix_str).replace(']', '')
        
        with open('input_matrix.txt', 'w') as f:
            f.write(flatten_matrix_str)
            
        logger.debug(f"Matriz de entrada: \n{matrix}")

        if bfs.check_both_conditions():
                
            root = Node(0, matrix, None, None)
            start = time.time()
            goal, f_nodes, visited_nodes = bfs.solve(root)
            end = time.time()
            if goal:
                logger.log(
                    "STATISTICS",
                    f"Tempo: {end - start: <25} Número de passos: {len(visited_nodes): <8} UUID: {uuid.uuid4()}")
