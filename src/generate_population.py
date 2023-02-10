from __future__ import annotations

import copy
import random
import time

from src.Chromosome import Chromosome
from src.Node import Node
from src.Process import Process
from src.utils import tup_add, tup_sub


def is_doable(new_stock: tuple) -> bool:
    return min(new_stock) >= 0


def get_doable_processes(candidate: Chromosome, processes: list[Process], memoization: dict[tuple[int]: list[Node]] = {}) -> list[Node]:
    if memoization.get(candidate.stock) is not None:
        return memoization[candidate.stock]
    doable: list[Node] = []

    for i, process in enumerate(processes):
        new_stock = tup_sub(candidate.stock, process.cost)
        if is_doable(new_stock):
            # here we stock the index of the process and the new value of the stock to not recalculate it in the future
            doable.append(
                Node(i, tup_add(new_stock, process.gain), process.delay))
    memoization[candidate.stock] = doable
    return doable


def apply_node(chromosome: Chromosome, node: Node):
    chromosome.process.append(node.process)
    chromosome.stock = node.stock
    chromosome.duration += node.delay


"""
Rewind to the previous step for the chromosome, and returns if there are other possibilities avaliables.
"""


def __rewind(chromosome: Chromosome, processes: list[Process], memoization: dict[tuple[int]: list[Node]]) -> int:
    last_process_id = chromosome.process.pop()
    chromosome.stock = tup_add(
        tup_sub(chromosome.stock, processes[last_process_id].gain),
        processes[last_process_id].cost
    )
    chromosome.duration -= processes[last_process_id].delay
    doable_ids = list(node.process for node in memoization[chromosome.stock])
    last_process_index = doable_ids.index(last_process_id)
    del memoization[chromosome.stock][last_process_index]
    return len(doable_ids) - 1


def __rollback(chromosome: Chromosome, processes: list[Process], memoization: dict[tuple[int]: list[Node]]) -> Node:
    doable_ids = __rewind(chromosome, processes, memoization)

    while not doable_ids:
        del memoization[chromosome.stock]
        doable_ids = __rewind(chromosome, processes, memoization)
    return memoization[chromosome.stock]


def generate_population(args, base: Chromosome, processes: list[Process], memoization: dict[tuple[int]: list[Node]], start: float) -> list[Chromosome]:
    population: list[Chromosome] = []
    i = 0

    for _ in range(args.population):
        chromosome = copy.deepcopy(base)
        for _ in range(args.iterations):
            doable = get_doable_processes(chromosome, processes, memoization)
            if not doable:
                doable = __rollback(chromosome, processes, memoization)
            app: Node = random.choice(doable)
            apply_node(chromosome, app)

            if i % 1000 == 0:
                delta = time.time() - start
                if delta >= args.delay:
                    return population

            i += 1
        population.append(chromosome)

    return population
