from __future__ import annotations

import copy

from src.Chromosome import Chromosome
from src.Process import Process
from src.utils import tup_sub


def print_collection(collection: list[Chromosome | Process]):
    for elem in collection:
        print(elem)


def print_stock(stock: tuple[int]):
    print("\tStock:")
    for key, stock in sorted(zip(Chromosome.converter, stock), key=lambda x: x[0]):
        print(f"\t - {key} => {stock}")


def is_sustainable(chromosome: Chromosome) -> bool:
    reference = chromosome.stock
    current = copy.deepcopy(chromosome)

    while current.undo_last_process():
        if min(tup_sub(reference, current.stock)) >= 0:
            return True
    return False

def print_cycle(chromosome: Chromosome, processes: list[Process], timeout: int):
    duration = 0
    print(f"\n\t{len(processes)} processes, {len(chromosome.stock)} stocks, 1 to optimize\n")

    with open("output.txt", 'w') as f:
        for p in chromosome.processes:
            if not p:
                continue
            output = f"{duration}:{p.name}\n"
            f.write(output)
            print(f"\t{output}", end='')
            duration += p.delay
        f.write(f"{duration}:end")

    if timeout:
        message = f"Maximum execution time reached at time {duration}"
    else:
        message = f"Maximum amount of generations reached at time {duration}"
    
    if is_sustainable(chromosome):
        message += " (system is sustainable)"
    else:
        message += " (system is not sustainable)"

    print(f"\n\t{message}\n")
    print_stock(chromosome.stock)
    print(f"\n\tPoints: {chromosome.calc_fitness()}")
