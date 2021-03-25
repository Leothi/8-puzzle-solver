import logging
import sys 
import grid
import solver

logging.basicConfig(
    filename='./logs/ast_stats.log', filemode='a',
    format='%(name)s - %(levelname)s - %(message)s', 
    encoding='utf-8')


with open ('input_matrix.txt', 'r') as f:
    input_matrix= f.read()
    
input_list = input_matrix.split(',')
N = len(input_list)
N -= 1
input_list = map(int, input_list)

ordered_list = sorted(input_list)
for index, number in enumerate(ordered_list):
    if number != index:
        sys.stderr.write("Error: input list must contain all numbers from 0 to n^2 - 1\n")
        sys.exit()


# TODO: do we want to pass the input_grid to the solver, or just instantiate 
# a generic Solver and pass input_grid to the search method?
try:
    solver = solver.Solver(input_list)
except ValueError:
    print 'no solution exists'
    sys.exit()

search_method = sys.argv[1]

if search_method == 'ast':
    solution_metrics = solver.a_star_search() 
else:
    solution_metrics = solver.uninformed_search(search_method) 

string = "N: {}".format(str(N)) + " Tempo: {}".format(
    str(float(solution_metrics.search_time) / 1000)) +" Numero de passos: {}".format(
    str(solution_metrics.search_depth))
logging.warning(string)
# logging.warning("PASSOS: %s", str(solution_metrics.search_depth))
# print "path_to_goal: " + str(solution_metrics.path_to_goal)
# print "cost_of_path: " + str(solution_metrics.cost_of_path())
# print "nodes_expanded: " + str(solution_metrics.nodes_expanded)
# print "fringe_size: " + str(solution_metrics.fringe_size())
# print "max_fringe_size: " + str(solution_metrics.max_fringe_size)
print "search_depth: " + str(solution_metrics.search_depth)
# print "max_search_depth: " + str(solution_metrics.max_search_depth)
print "running_time: " + str(solution_metrics.search_time) + "ms"
# print "max_ram_useage: " + str(solution_metrics.max_ram_useage) + "MB"
