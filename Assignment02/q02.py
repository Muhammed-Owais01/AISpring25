import random

task_times = [5, 8, 4, 7, 6, 3, 9] 
facility_capacities = [24, 30, 28]  

cost_matrix = [
    [10, 12,  9],  
    [15, 14, 16],  
    [ 8,  9,  7],  
    [12, 10, 13],  
    [14, 13, 12],  
    [ 9,  8, 10],  
    [11, 12, 13],  
]

POP_SIZE = 6
MAX_GENERATIONS = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2

def compute_fitness(chromosome):
    used_time = [0, 0, 0]
    total_cost = 0

    for task_id, facility_id in enumerate(chromosome):
        time = task_times[task_id]
        cost_per_hour = cost_matrix[task_id][facility_id]
        used_time[facility_id] += time
        total_cost += time * cost_per_hour

    penalty = 0
    for i in range(3):
        if used_time[i] > facility_capacities[i]:
            penalty += (used_time[i] - facility_capacities[i]) * 1000  

    return 1 / (total_cost + penalty)  


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(chromosome):
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]


def generate_initial_population():
    return [[random.randint(0, 2) for _ in range(7)] for _ in range(POP_SIZE)]


def roulette_wheel_selection(population, fitness_scores):
    total = sum(fitness_scores)
    probs = [f / total for f in fitness_scores]
    return random.choices(population, weights=probs, k=POP_SIZE)


def genetic_algorithm():
    population = generate_initial_population()

    for generation in range(MAX_GENERATIONS):
        fitness_scores = [compute_fitness(c) for c in population]
        population = roulette_wheel_selection(population, fitness_scores)

        next_generation = []

        for i in range(0, POP_SIZE, 2):
            parent1, parent2 = population[i], population[i + 1]
            if random.random() < CROSSOVER_RATE:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]
            next_generation.extend([child1, child2])

        for i in range(POP_SIZE):
            if random.random() < MUTATION_RATE:
                mutate(next_generation[i])

        population = next_generation

    fitness_scores = [compute_fitness(c) for c in population]
    best_index = fitness_scores.index(max(fitness_scores))
    best_solution = population[best_index]
    best_cost = 1 / fitness_scores[best_index]

    return best_solution, best_cost


best_assignment, min_cost = genetic_algorithm()

print("Best Assignment (Task → Facility):", best_assignment)
print("Minimum Total Cost:", round(min_cost, 2))