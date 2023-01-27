import copy
import math
import random

from src.Candidate import Candidate
from src.Process import Process
from src.utils import tup_sub, tup_add, cross_list
from src.generate_population import is_doable, get_doable_processes, apply_node


def __fitness(chromosome: Candidate):
    chromosome.fitness = 0
    for i,x in enumerate(chromosome.stock):
        chromosome.fitness += Candidate.goal[i] * x
    return chromosome.fitness


def __select_chromosomes(population: list[Candidate], population_size: int) -> list[Candidate]:
    # we are performing elitism when sorting population and children obtained by crossover
    return sorted(population, key=lambda chromosome: __fitness(chromosome), reverse=True)[:population_size]


def __do_process(chromosome: Candidate, new_stock: tuple, process: Process, process_nb):
    chromosome.process.append(process_nb)
    chromosome.stock = tup_add(new_stock, process.gain)
    chromosome.duration += process.delay


def __cross(chromosome: Candidate, processes_list: list[int], processes: list[Process]) -> Candidate:
    for p in processes_list:
        new_stock = tup_sub(chromosome.stock, processes[p].cost)
        if not is_doable(new_stock):
            return chromosome
        __do_process(chromosome, new_stock, processes[p], p)
    return chromosome


def __crossover(population: list[Candidate], base: Candidate, processes: list[Process]):
    size: range = range(int(len(population) / 2))

    for i in size:
        parent_a: Candidate = population[i]
        parent_b: Candidate = population[i + 1]

        population.append(__cross(copy.deepcopy(base), cross_list(parent_a.process, parent_b.process), processes))
        population.append(__cross(copy.deepcopy(base), cross_list(parent_b.process, parent_a.process), processes))

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
    for i in range(args.population, args.population * 2):
        ratio: int = math.floor(
            len(population[i].process) * (random.choice(range(1, args.ratio)) / 100))
        if ratio == 0:
            continue
        mutation_point: int = random.choice(
            range(0, len(population[i].process) - ratio - 1))
        mutated: Candidate = copy.deepcopy(base)

        population[i] = __mutate(
            population[i], mutated, processes, ratio, mutation_point)


def evolve(population: list[Candidate], base: Candidate, processes: list[Process], args) -> list[Candidate]:
    population = __select_chromosomes(population, args.population)

    for i in range(args.generations):
        __crossover(population, base, processes)
        __mutation(population, base, processes, args)
        population = __select_chromosomes(population, args.population)
    return population
