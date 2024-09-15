import random
import copy

# Define the goal state of the puzzle
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# Fitness function (inverse of Manhattan distance)
def fitness(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                target_x, target_y = divmod(goal_state.index(state[i][j]), 3)
                distance += abs(target_x - i) + abs(target_y - j)
    return 1 / (1 + distance)

# Get possible moves
def get_neighbors(state):
    neighbors = []
    blank_x, blank_y = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for move in moves:
        new_x, new_y = blank_x + move[0], blank_y + move[1]
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = copy.deepcopy(state)
            new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
            neighbors.append(new_state)
    return neighbors

# Crossover (combine two states)
def crossover(parent1, parent2):
    child = copy.deepcopy(parent1)
    for i in range(3):
        for j in range(3):
            if random.random() < 0.5:
                child[i][j] = parent2[i][j]
    return child

# Mutation (random move)
def mutate(state):
    neighbors = get_neighbors(state)
    return random.choice(neighbors)

# Genetic Algorithm
def genetic_algorithm(population_size=10, generations=100, mutation_rate=0.1):
    population = [random.sample(range(9), 9) for _ in range(population_size)]
    population = [list(map(list, zip(*[iter(p)]*3))) for p in population]

    for generation in range(generations):
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        
        if population[0] == goal_state:
            return population[0]
        
        new_population = []
        
        # Selection and crossover
        for i in range(population_size // 2):
            parent1 = random.choice(population[:5])
            parent2 = random.choice(population[:5])
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.append(child1)
            new_population.append(child2)
        
        # Mutation
        for i in range(len(new_population)):
            if random.random() < mutation_rate:
                new_population[i] = mutate(new_population[i])
        
        population = new_population
    
    return sorted(population, key=lambda x: fitness(x), reverse=True)[0]

# Run Genetic Algorithm
solution = genetic_algorithm()
print("Final Solution:", solution)
