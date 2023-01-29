import copy
import math
import random
import time

from src.Candidate import Candidate
from src.generate_population import apply_node, get_doable_processes, is_doable
from src.Process import Process
from src.utils import cross_list, tup_add, tup_sub


def __fitness(chromosome: Candidate):
    chromosome.fitness = 0
    for i, x in enumerate(chromosome.stock):
        chromosome.fitness += Candidate.goal[i] * x
    return chromosome.fitness


def __select_chromosomes(population: list[Candidate], population_size: int) -> list[Candidate]:
    # we are performing elitism when sorting population and children obtained by crossover
    return sorted(population, key=lambda chromosome: __fitness(chromosome), reverse=True)[:population_size]


def __do_process(chromosome: Candidate, new_stock: tuple, process: Process, process_nb):
    chromosome.process.append(process_nb)
    chromosome.stock = tup_add(new_stock, process.gain)
    chromosome.duration += process.delay


def __apply_processes(chromosome: Candidate, processes_list: list[int], processes: list[Process]) -> Candidate:
    for p in processes_list:
        new_stock = tup_sub(chromosome.stock, processes[p].cost)
        if not is_doable(new_stock):
            return chromosome
        __do_process(chromosome, new_stock, processes[p], p)
    return chromosome


def __cross(population: list[Candidate], base: Candidate, processes: list[Process]):
    size: range = range(len(population) - 1)

    for i in size:
        parent_a: Candidate = population[i]
        parent_b: Candidate = population[i + 1]

        population.append(__apply_processes(copy.deepcopy(base), cross_list(
            parent_a.process, parent_b.process), processes))
        population.append(__apply_processes(copy.deepcopy(base), cross_list(
            parent_b.process, parent_a.process), processes))


def __mutate(mutable: Candidate, mutated: Candidate, processes: list[Process], ratio: int, mutation_point) -> Candidate:
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


def __mutation(population: list[Candidate], base: Candidate, processes: list[Process], args) -> list[Candidate]:
    for i, candidate in enumerate(population):
        ratio: int = math.floor(
            len(candidate.process) * (random.choice(range(1, args.ratio)) / 100))
        if ratio == 0:
            continue
        mutation_point: int = random.choice(
            range(0, len(candidate.process) - ratio - 1))
        mutated: Candidate = copy.deepcopy(base)

        population[i] = __mutate(
            candidate, mutated, processes, ratio, mutation_point)


def evolve(population: list[Candidate], base: Candidate, processes: list[Process], start: float, args) -> list[Candidate]:
    population = __select_chromosomes(population, args.population)

    for i in range(args.generations):
        __cross(population, base, processes)
        __mutation(population, base, processes, args)
        population = __select_chromosomes(population, args.population)

        delta = time.time() - start
        if delta >= args.delay:
            break
    return population
