from queue import Queue, LifoQueue, PriorityQueue

METHODS = {
    'breadth': Queue(), # Queue Data Structure for breadth first search
    'depth': LifoQueue(), # Stack Data Structure for depth first search
    'astar': PriorityQueue(), # Priority Queue for astar search
    'best': PriorityQueue() # Priority Queue for best search
}


# Loads the problem from .txt file and stores it into an array.
def loadProblem(fileName):
    with open(fileName, "r") as file:
        data = file.readlines()
    new_data = [item.replace('\n', '') for item in data]
    return new_data

# Initializes the initial problem of the game
def initializeProblem(data):
    # The game of the problem will
    game = {}

    # Pass the data of the initial read that we got to the stacks of the problem, where each one of them has an id from 1 to 8
    game["stack"] = {}
    i=1
    for line in data:
        formattedData = line.split(' ')
        game["stack"][i] = formattedData
        i = i + 1

    # Initialize the list of the freecells
    game["freecell"] = []
    for i in range(0,4):
        game["freecell"].append(None)

    # Initialize the lists of the foundations, with an id from 1 to 4 where each one of the id corresponds to a certain shape of the cards
    game["foundation"] = {}
    for j in range(0,4):
        game["foundation"][j] = []

    return game

def write_solution_to_file(file, solution_steps, solution_moves):

    # solution_moves.reverse()
    with open(file, "w") as file:
        file.write("{} \n".format(solution_steps))
        for move in solution_moves[::-1]:
            if len(move) == 3:
                move_card, card_1, card_2 = move
                file.write("{} {} {} \n".format(move_card, card_1, card_2))
            elif len(move) == 2:
                move_card, card = move
                file.write("{} {} \n".format(move_card, card))




