import random
import math
import copy

# Define the goal state of the puzzle
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# Manhattan distance function (heuristic)
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                target_x, target_y = divmod(goal_state.index(state[i][j]), 3)
                distance += abs(target_x - i) + abs(target_y - j)
    return distance

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

# Simulated Annealing Algorithm
def simulated_annealing(state, max_temp=1000, min_temp=1, cooling_rate=0.003):
    current_state = state
    current_cost = manhattan_distance(current_state)
    temp = max_temp
    
    while temp > min_temp:
        neighbor_states = get_neighbors(current_state)
        next_state = random.choice(neighbor_states)
        next_cost = manhattan_distance(next_state)
        
        delta_cost = next_cost - current_cost
        
        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temp):
            current_state = next_state
            current_cost = next_cost
        
        if current_state == goal_state:
            return current_state, temp
        
        temp *= 1 - cooling_rate
    
    return current_state, temp

# Initial random state
initial_state = [[1, 2, 3],
                 [4, 0, 6],
                 [7, 5, 8]]

# Run Simulated Annealing
solution, final_temp = simulated_annealing(initial_state)
print("Final Solution:", solution)
