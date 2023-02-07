from __future__ import annotations

from src.Candidate import Candidate
from src.Process import Process


def print_collection(collection: list[Candidate | Process]):
    for elem in collection:
        print(elem)


def print_stock(stock: tuple[int]):
    print("\tStock:")
    for key, stock in sorted(zip(Candidate.converter, stock), key=lambda x: x[0]):
        print(f"\t - {key} => {stock}")


def print_cycle(chromosome: Candidate, processes: list[Process], stop_type: int):
    duration = 0
    print(
        f"\n\t{len(processes)} processes, {len(chromosome.stock)} stocks, 1 to optimize\n")
    for i in chromosome.process:
        if i < 0:
            continue
        print(f"\t{duration}:{processes[i].name}")
        duration += processes[i].delay
    match stop_type:
        case 1:
            print(
                f"\n\tMaximum amount of generations reached at time {duration}\n")
        case 2:
            print(f"\n\tNo more process doable at time {duration}\n")
        case 3:
            print(f"\n\tMaximum execution time reached at time {duration}\n")
    print_stock(chromosome.stock)
    print(f"\n\tPoints: {chromosome.calc_fitness()}")
