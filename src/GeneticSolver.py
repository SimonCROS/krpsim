import random
import time

from src.Chromosome import Chromosome
from src.Process import Process

import sys

def __sort(population: list[Chromosome], opti_time: bool):
    # we are performing elitism when sorting population and children obtained by crossover
    for chromosome in population:
        chromosome.calc_fitness()
        if opti_time and chromosome.duration > 0 and len(chromosome.process) > 0:
            chromosome.fitness *= Process.max_delay / (chromosome.duration / chromosome.process_count)
    population.sort(key=lambda c: c.fitness, reverse=True)


def __cross(population: list[Chromosome], base: Chromosome, processes: list[Process]) -> list[Chromosome]:
    size = len(population)
    keep = max(round((10*size)/100), 1)

    new_generation = []
    new_generation.extend(population[:keep])

    middle = round(size / 2)
    for i in range(size - keep):
        parent_a: Chromosome = random.choice(population[:middle])
        parent_b: Chromosome = random.choice(population[:middle])

        new_chromosome = Chromosome.cross(base, parent_a, parent_b, processes)
        new_generation.append(new_chromosome)
    return new_generation


def evolve(population: list[Chromosome], base: Chromosome, processes: list[Process], start: float, opti_time: bool, args) -> list[Chromosome]:
    __sort(population, opti_time)

    for i in range(args.generations):
        population = __cross(population, base, processes)
        __sort(population, opti_time)
        print(f"Completed generation {i}, best {population[0].calc_fitness()}", file=sys.stderr)

        delta = time.time() - start
        if delta >= args.delay:
            break
    return population
