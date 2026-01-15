import random
import math

# -------- Objective Function --------
def sphere(solution):
    return sum(x ** 2 for x in solution)

# -------- ABC Parameters --------
NUM_BEES = 20          # Number of food sources
DIM = 2                # Problem dimension
LOWER_BOUND = -5
UPPER_BOUND = 5
LIMIT = 5              # Scout limit
MAX_ITER = 50

# -------- Initialization --------
def random_solution():
    return [random.uniform(LOWER_BOUND, UPPER_BOUND) for _ in range(DIM)]

solutions = [random_solution() for _ in range(NUM_BEES)]
fitness = [sphere(sol) for sol in solutions]
trial = [0] * NUM_BEES

best_solution = solutions[0]
best_fitness = fitness[0]

# -------- Main ABC Loop --------
for iteration in range(MAX_ITER):

    # --- Employed Bee Phase ---
    for i in range(NUM_BEES):
        k = random.choice([x for x in range(NUM_BEES) if x != i])
        phi = random.uniform(-1, 1)

        new_solution = solutions[i][:]
        d = random.randint(0, DIM - 1)
        new_solution[d] = solutions[i][d] + phi * (solutions[i][d] - solutions[k][d])

        # Keep inside bounds
        new_solution[d] = max(LOWER_BOUND, min(UPPER_BOUND, new_solution[d]))

        new_fitness = sphere(new_solution)

        if new_fitness < fitness[i]:
            solutions[i] = new_solution
            fitness[i] = new_fitness
            trial[i] = 0
        else:
            trial[i] += 1

    # --- Onlooker Bee Phase ---
    total_fitness = sum(1 / (1 + f) for f in fitness)
    probs = [(1 / (1 + f)) / total_fitness for f in fitness]

    for _ in range(NUM_BEES):
        i = random.choices(range(NUM_BEES), probs)[0]
        k = random.choice([x for x in range(NUM_BEES) if x != i])
        phi = random.uniform(-1, 1)

        new_solution = solutions[i][:]
        d = random.randint(0, DIM - 1)
        new_solution[d] = solutions[i][d] + phi * (solutions[i][d] - solutions[k][d])
        new_solution[d] = max(LOWER_BOUND, min(UPPER_BOUND, new_solution[d]))

        new_fitness = sphere(new_solution)

        if new_fitness < fitness[i]:
            solutions[i] = new_solution
            fitness[i] = new_fitness
            trial[i] = 0
        else:
            trial[i] += 1

    # --- Scout Bee Phase ---
    for i in range(NUM_BEES):
        if trial[i] > LIMIT:
            solutions[i] = random_solution()
            fitness[i] = sphere(solutions[i])
            trial[i] = 0

    # --- Best Solution Update ---
    for i in range(NUM_BEES):
        if fitness[i] < best_fitness:
            best_fitness = fitness[i]
            best_solution = solutions[i]

    print(f"Iteration {iteration + 1}: Best Fitness = {best_fitness:.6f}")

print("\nBest Solution Found:", best_solution)
print("Best Fitness:", best_fitness)
