from __future__ import annotations

import copy
import random
import time

from src.Chromosome import Chromosome
from src.Process import Process
from src.utils import tup_sub


def is_doable(chromosome: Chromosome, process: Process) -> bool:
    return min(tup_sub(chromosome.stock, process.cost)) >= 0


def load_doable_processes(chromosome: Chromosome, processes: list[Process], memoization: dict[tuple[int]: list[Process]]) -> bool:
    if memoization.get(chromosome.stock) is None:
        memoization[chromosome.stock] = list(process for process in processes if is_doable(chromosome, process))
    return len(memoization[chromosome.stock]) > 0


def __rewind(chromosome: Chromosome, memoization: dict[tuple[int]: list[Process]]) -> int:
    last_process = chromosome.undo_last_process()

    if last_process == None:
        return True

    memoization[chromosome.stock].remove(last_process)
    return len(memoization[chromosome.stock])


def generate_population(base: Chromosome, processes: list[Process], start: float, args) -> list[Chromosome]:
    memoization: dict[tuple: tuple] = {}
    population: list[Chromosome] = []

    i = 0
    for _ in range(args.population):
        chromosome = copy.deepcopy(base)
        for _ in range(args.iterations):
            if not load_doable_processes(chromosome, processes, memoization):
                while not __rewind(chromosome, memoization):
                    del memoization[chromosome.stock]

            if memoization.get(chromosome.stock):
                chromosome.try_do_process(random.choice(memoization[chromosome.stock]))
            else:
                chromosome.try_do_process(None, insert_padding=True)

            if i % 1000 == 0:
                delta = time.time() - start
                if delta >= args.delay:
                    return population
            i += 1
        chromosome.fill_processes_to(args.iterations)
        population.append(chromosome)

    return population
