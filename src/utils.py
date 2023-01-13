from __future__ import annotations

from src.Candidate import Candidate
from src.Process import Process
from operator import sub, add


def print_collection(collection: list[Candidate | Process]):
    for elem in collection:
        print(elem)
    print("")


def print_stock(stock: tuple[int]):
    print("\tStock:")
    for key, stock in zip(Candidate.converter, stock):
        print(f"\t - {key} => {stock}")
    print("")


def print_cycle(chromosome: Candidate, processes: list[Process], pb_type: int, start: Candidate):
    duration = 0
    print(
        f"\n\t{len(processes)} processes, {len(chromosome.stock)} stocks, 1 to optimize\n")
    for i in chromosome.process:
        print(f"\t{duration}:{processes[i].name}")
        duration += processes[i].delay
    if pb_type == 1:
        if chromosome.stock[-1] <= start.stock[-1]:
            print(
                f"\n\tSustainable system not obtained, try to increase iterations [-i]. Stopped at time {duration + 1}\n")
        else:
            print(f"\n\tSustainable system stopped at time {duration + 1}\n")
    else:
        print(f"\n\tNo more process doable at time {duration + 1}\n")
    print_stock(chromosome.stock)


def tup_sub(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(sub, a, b))


def tup_add(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(add, a, b))
