from __future__ import annotations

import copy
import random

from src.Process import Process
from src.Candidate import Candidate
from src.utils import tup_sub, tup_add


def __is_doable(new_stock: tuple) -> bool:
    return min(new_stock) >= 0


def __get_doable_processes(candidate: Candidate, processes: list[Process],
                           memoization: dict[tuple[int]: tuple[tuple[int, tuple[int]]]]) -> tuple:
    if memoization.get(candidate.stock) is not None:
        return memoization[candidate.stock]

    doable: tuple[tuple[int]] = ()

    for i, process in enumerate(processes):
        new_stock = tup_sub(candidate.stock, process.cost)
        if __is_doable(new_stock):
            # here we stock the index of the process and the new value of the stock to not recalculate it in the future
            doable = (*doable, (i, tup_add(new_stock, process.gain), process.delay))
    memoization[candidate.stock] = doable
    return doable


def __do_process(chromosome: Candidate, process: tuple):
    chromosome.process.append(process[0])
    chromosome.stock = process[1]
    chromosome.duration += process[2]


def generate_population(args, start: Candidate, processes: list[Process],
                        memoization: dict[tuple[int]: tuple[tuple[int, tuple[int]]]]) -> list[Candidate]:
    population: list[Candidate] = []

    for p in range(args.population):
        chromosome = copy.deepcopy(start)
        for i in range(args.iterations):
            doable = __get_doable_processes(chromosome, processes, memoization)
            if not doable:
                break
            __do_process(chromosome, random.choice(doable))
        population.append(chromosome)

    return population
