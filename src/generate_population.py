from __future__ import annotations

import copy
import random

from src.Node import Node
from src.Process import Process
from src.Candidate import Candidate
from src.utils import tup_sub, tup_add


def is_doable(new_stock: tuple) -> bool:
    return min(new_stock) >= 0


def get_doable_processes(candidate: Candidate, processes: list[Process], memoization: dict[tuple[int]: Node] = {}) -> tuple[Node]:
    if memoization.get(candidate.stock) is not None:
        return memoization[candidate.stock]

    doable: tuple[Node] = ()

    for i, process in enumerate(processes):
        new_stock = tup_sub(candidate.stock, process.cost)
        if is_doable(new_stock):
            # here we stock the index of the process and the new value of the stock to not recalculate it in the future
            doable = (
                *doable, Node(i, tup_add(new_stock, process.gain), process.delay))
    memoization[candidate.stock] = doable
    return doable


def apply_node(chromosome: Candidate, node: Node):
    chromosome.process.append(node.process)
    chromosome.stock = node.stock
    chromosome.duration += node.delay


def __rewind(chromosome: Candidate, processes: list[Process], memoization: dict[tuple[int]: Node]) -> tuple[int]:
    last_process_id = chromosome.process.pop()
    chromosome.stock = tup_add(
        tup_sub(chromosome.stock, processes[last_process_id].gain),
        processes[last_process_id].cost
    )
    chromosome.duration -= processes[last_process_id].delay
    doable_ids = list(node.process for node in memoization[chromosome.stock])
    last_process_index = doable_ids.index(last_process_id)
    memoization[chromosome.stock] = (
        *memoization[chromosome.stock][:last_process_index],
        *memoization[chromosome.stock][last_process_index + 1:]
    )
    return len(doable_ids) - 1


def __rollback(chromosome: Candidate, processes: list[Process], memoization: dict[tuple[int]: Node]) -> Node:
    doable_ids = __rewind(chromosome, processes, memoization)

    while not doable_ids:
        del memoization[chromosome.stock]
        doable_ids = __rewind(chromosome, processes, memoization)
    return memoization[chromosome.stock]


def generate_population(args, start: Candidate, processes: list[Process], pb_type: int, memoization: dict[tuple[int]: Node]) -> list[Candidate]:
    population: list[Candidate] = []

    for p in range(args.population):
        chromosome = copy.deepcopy(start)
        for i in range(args.iterations):
            doable = get_doable_processes(chromosome, processes, memoization)
            if not doable:
                if pb_type == 2:
                    break
                doable = __rollback(chromosome, processes, memoization)
            apply_node(chromosome, random.choice(doable))
        population.append(chromosome)

    return population
