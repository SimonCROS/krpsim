import copy
import math
import random
import time
import sys

from src.Chromosome import Chromosome
from src.generate_population import apply_node, get_doable_processes, is_doable
from src.Process import Process
from src.utils import cross_list, tup_add, tup_sub


def __select_chromosomes(population: list[Chromosome], population_size: int, opti_time: bool) -> list[Chromosome]:
    # we are performing elitism when sorting population and children obtained by crossover
    for chromosome in population:
        chromosome.calc_fitness()
        if opti_time and chromosome.duration > 0 and len(chromosome.process) > 0:
            chromosome.fitness *= Process.max_delay / (chromosome.duration / len(chromosome.process))

    return sorted(population, key=lambda chromosome: chromosome.fitness, reverse=True)[:population_size]


def __do_process(chromosome: Chromosome, new_stock: tuple, process: Process, process_nb):
    chromosome.process.append(process_nb)
    chromosome.stock = tup_add(new_stock, process.gain)
    chromosome.duration += process.delay

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


def __mutate(mutable: Chromosome, mutated: Chromosome, processes: list[Process], ratio: int, mutation_point) -> Chromosome:
    for i in range(0, mutation_point - 1):
        new_stock = tup_sub(mutated.stock, processes[mutable.process[i]].cost)
        __do_process(mutated, new_stock,
                     processes[mutable.process[i]], mutable.process[i])

    for i in range(mutation_point, mutation_point + ratio):
        doable = get_doable_processes(mutated, processes)
        if not doable:
            return mutable
        apply_node(mutated, random.choice(doable))

    for i in range(mutation_point + ratio, len(mutable.process)):
        new_stock = tup_sub(mutated.stock, processes[mutable.process[i]].cost)
        if not is_doable(new_stock):
            return mutable
        __do_process(mutated, new_stock,
                     processes[mutable.process[i]], mutable.process[i])
    return mutated


def __mutation(population: list[Chromosome], base: Chromosome, processes: list[Process], args) -> list[Chromosome]:
    for i, candidate in enumerate(population):
        ratio: int = math.floor(
            len(candidate.process) * (random.choice(range(1, args.ratio)) / 100))
        if ratio == 0:
            continue
        mutation_point: int = random.choice(
            range(0, len(candidate.process) - ratio - 1))
        mutated: Chromosome = copy.deepcopy(base)

        population[i] = __mutate(
            candidate, mutated, processes, ratio, mutation_point)


def evolve(population: list[Chromosome], base: Chromosome, processes: list[Process], start: float, opti_time: bool, args) -> list[Chromosome]:
    population = __select_chromosomes(population, args.population, opti_time)

    print(f"Starting generation, best {population[0].calc_fitness()}", file=sys.stderr)
    for i in range(args.generations):
        population = __cross(population, base, processes)
        __mutation(population, base, processes, args)
        population = __select_chromosomes(population, args.population, opti_time)
        print(f"Completed generation {i}, best {population[0].calc_fitness()}", file=sys.stderr)

        delta = time.time() - start
        if delta >= args.delay:
            break
    return population
