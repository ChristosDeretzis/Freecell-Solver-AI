from Node import TreeNode
import time
import utils
import os
import sys

def search(queue, method, initial_game):
    root = TreeNode(initial_game, None, None, 0, 0, 0)

    if method == 'astar' or method == 'best':
        queue.put((0, root))
    else:
        queue.put(root)

    visited_states = set()
    start = time.time()

    while (not queue.empty()) and (time.time() - start <= 300):
        if method == 'astar' or method == 'best':
            curr_f, current = queue.get()
        else:
            current = queue.get()

        if current.is_goal():
            return current


        if str(current.game) in visited_states:
            continue

        current.find_children(method)
        visited_states.add(str(current.game))

        for child in current.children:
            if method == 'depth' or method == 'breadth':
                queue.put(child)
            elif method == 'astar' or method == 'best':
                queue.put((child.f, child))
            print(child.game)
        print("===============================")
    return None
    print(time.time() - start)

def main():
    start = time.time()
    os.system('cls' if os.name == 'nt' else 'clear')

    if len(sys.argv) == 3:
        method = sys.argv[1]
        input_file = sys.argv[2]
    elif len(sys.argv) == 4:
        method = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3]
    else:
        print(f'Usage: {sys.argv[0]} <search algorithm> <input file name> <output file name>')
        print('Search algorithm: depth (Depth First), breadth (Breadth First), best (Best First), astar (A*)')
        sys.exit()

    search_queue = utils.METHODS[method]

    data = utils.loadProblem(input_file)
    initial_game = utils.initializeProblem(data)

    print("######################## INITIAL PROBLEM ############" )

    solution_node = search(search_queue, method, initial_game)

    if solution_node is not None:
        print("################## SOLUTION FOUND ##################### \n")
        print("Number of moves: {}".format(solution_node.g))

        print("Time to solve: ", time.time() - start)

        number_of_solution_steps = solution_node.g
        solution_path = solution_node.extract_solution()

        if len(sys.argv) == 3:
            try:
                file_name = input_file.split("\\")[-1]
                output_file = ".\\solutions\\" + method + '-' + file_name
                utils.write_solution_to_file(output_file, number_of_solution_steps, solution_path)
            except FileNotFoundError:
                file_name = input_file.split("/")[-1]
                output_file = "./solutions/" + method + '-' + file_name
                utils.write_solution_to_file(output_file, number_of_solution_steps, solution_path)
        else:
            utils.write_solution_to_file(output_file, number_of_solution_steps, solution_path)
    else:
        print("Time : ", time.time() - start)
        print("##################### Five minutes have passed and no solution found #############")
        sys.exit()


if __name__ == '__main__':
    main()



