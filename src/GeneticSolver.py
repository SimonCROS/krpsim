import random
import time
import sys

from src.Chromosome import Chromosome
from src.Process import Process


def __select_chromosomes(population: list[Chromosome], population_size: int, opti_time: bool) -> list[Chromosome]:
    # we are performing elitism when sorting population and children obtained by crossover
    for chromosome in population:
        chromosome.calc_fitness()
        if opti_time and chromosome.duration > 0 and len(chromosome.processes) > 0:
            chromosome.fitness *= Process.max_delay / (chromosome.duration / len(chromosome.processes))

    return sorted(population, key=lambda chromosome: chromosome.fitness, reverse=True)[:population_size]

def __cross(population: list[Chromosome], base: Chromosome, processes: list[Process]) -> list[Chromosome]:
    size = len(population)
    keep = max(round((10*size)/100), 1)

    new_generation = []
    new_generation.extend(population[:keep])

    middle = round(size / 2)
    for _ in range(size - keep):
        parent_a: Chromosome = random.choice(population[:middle])
        parent_b: Chromosome = random.choice(population[:middle])

        new_chromosome = Chromosome.cross(base, parent_a, parent_b, processes)
        new_generation.append(new_chromosome)
    return new_generation

def evolve(population: list[Chromosome], base: Chromosome, processes: list[Process], start: float, opti_time: bool, args) -> list[Chromosome]:
    population = __select_chromosomes(population, args.population, opti_time)

    print(f"Starting generation, best {population[0].calc_fitness()}", file=sys.stderr)
    for i in range(args.generations):
        population = __cross(population, base, processes)
        population = __select_chromosomes(population, args.population, opti_time)
        print(f"Completed generation {i}, best {population[0].calc_fitness()}", file=sys.stderr)

        delta = time.time() - start
        if delta >= args.delay:
            break
    return population
