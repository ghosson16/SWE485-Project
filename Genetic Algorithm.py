import time
from random import randint, shuffle

# City labels and genes
GENES = ['A', 'B', 'C', 'D', 'E']
GENE_LABELS = ['LA', 'NYC', 'Chicago', 'Las Vegas', 'Seattle']

# Distance matrix
mp = [
    [0, 2800, 800, 1800, 2500],  # LA
    [2800, 0, 2000, 1000, 300],  # NYC
    [800, 2000, 0, 1000, 1800],  # Chicago
    [1800, 1000, 1000, 0, 800],  # Las Vegas
    [2500, 300, 1800, 800, 0]  # Seattle
]


class Individual:
    def _init_(self):
        self.gnome = ""
        self.fitness = 0

    def _lt_(self, other):
        return self.fitness < other.fitness

    def _gt_(self, other):
        return self.fitness > other.fitness


def rand_num(start, end):
    return randint(start, end - 1)


def create_gnome():
    gnome = list(GENES)  # Start with a full set of genes
    shuffle(gnome)  # Shuffle the genes
    gnome.append(gnome[0])  # Create a round trip
    return ''.join(gnome)  # Convert list to string


def cal_fitness(gnome):
    f = 0
    for i in range(len(gnome) - 1):
        city1 = GENES.index(gnome[i])
        city2 = GENES.index(gnome[i + 1])
        f += mp[city1][city2]
    return f


def mutated_gene(gnome):
    # Swaps two random genes (excluding start/end)
    gnome = list(gnome)
    while True:
        r1, r2 = randint(1, len(GENES) - 1), randint(1, len(GENES) - 1)
        if r1 != r2:
            gnome[r1], gnome[r2] = gnome[r2], gnome[r1]
            break
    return ''.join(gnome)


def cooldown(temp):
    return (90 * temp) / 100


def TSPUtil():
    POP_SIZE = 10  # Define population size
    gen = 1
    gen_thres = 5
    population = []

    # Create initial population
    for i in range(POP_SIZE):
        individual = Individual()
        individual.gnome = create_gnome()
        individual.fitness = cal_fitness(individual.gnome)
        population.append(individual)

    print("Initial population: \nGNOME\tFITNESS VALUE")
    for individual in population:
        print(individual.gnome, individual.fitness)
    print()

    temperature = 10000  # Initial temperature

    # Simulated annealing with a genetic algorithm
    while temperature > 1000 and gen <= gen_thres:
        # Sort the population based on fitness
        population.sort()

        new_population = []

        for i in range(POP_SIZE):
            parent = population[i]

            # Attempt to mutate the gnome with a probability
            while True:
                new_gnome_str = mutated_gene(parent.gnome)
                new_gnome = Individual()
                new_gnome.gnome = new_gnome_str
                new_gnome.fitness = cal_fitness(new_gnome.gnome)

                if new_gnome.fitness <= parent.fitness:
                    new_population.append(new_gnome)
                    break
                else:
                    # Boltzmann distribution for simulated annealing
                    prob = pow(
                        2.7,
                        -1 * (float(new_gnome.fitness - parent.fitness) / temperature)
                    )
                    if prob > 0.5:
                        new_population.append(new_gnome)
                        break

        # Update population and decrease temperature
        temperature = cooldown(temperature)
        population = new_population

        # Display generation results
        print("Generation", gen)
        print("GNOME\tFITNESS VALUE")
        for individual in population:
            print(individual.gnome, individual.fitness)

        gen += 1


if _name_ == "_main_":
    start_time = time.time()
    TSPUtil()  # Pass the distance matrix
    end_time = time.time()
    computational_time = end_time - start_time
    print("Computational time:", computational_time, "seconds")
