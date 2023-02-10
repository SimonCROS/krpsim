from __future__ import annotations

import copy
import random
import time

from src.Chromosome import Chromosome
from src.Process import Process
from src.utils import tup_add, tup_sub


def is_doable(new_stock: tuple) -> bool:
    return min(new_stock) >= 0


def load_doable_processes(chromosome: Chromosome, processes: list[Process], memoization: dict[tuple[int]: list[Node]] = {}) -> list[Node]:
    if memoization.get(chromosome.stock) is not None:
        return memoization[chromosome.stock]
    doable: list[Node] = []

    for i, process in enumerate(processes):
        new_stock = tup_sub(chromosome.stock, process.cost)
        if is_doable(new_stock):
            doable.append(process)
    memoization[chromosome.stock] = doable
    return len(doable) > 0


"""
Rewind to the previous step for the chromosome, and returns if there are other possibilities avaliables.
"""


def __rewind(chromosome: Chromosome, memoization: dict[tuple[int]: list[Process]]) -> int:
    last_process = chromosome.undo_last_process()
    memoization[chromosome.stock].remove(last_process)
    return len(memoization[chromosome.stock])

import sys

def generate_population(args, base: Chromosome, processes: list[Process], memoization: dict[tuple[int]: list[Node]], start: float) -> list[Chromosome]:
    population: list[Chromosome] = []
    i = 0

    for _ in range(args.population):
        chromosome = copy.deepcopy(base)
        for _ in range(args.iterations):
            if not load_doable_processes(chromosome, processes, memoization):
                doable = __rewind(chromosome, memoization)
                while not doable:
                    del memoization[chromosome.stock]  
                    doable = __rewind(chromosome, memoization)
            chromosome.try_do_process(random.choice(memoization[chromosome.stock]))

            if i % 1000 == 0:
                delta = time.time() - start
                if delta >= args.delay:
                    return population

            i += 1
        population.append(chromosome)

    return population
