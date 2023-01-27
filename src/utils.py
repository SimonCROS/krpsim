from __future__ import annotations

import random
from operator import add, sub

from src.Candidate import Candidate
from src.Process import Process


def cross_list(l1: list, l2: list):
    len_a = len(l1)
    len_b = len(l2)

    amount1 = random.randint(0, len_a)
    split_1_at = random.randint(0, amount1)
    split_2_b = random.randint(0, len_b)
    cross_len = len_a - amount1

    crossed = l1[:split_1_at];
    crossed += l2[max(0, min(split_2_b, len_b - cross_len)):min(len_b, split_2_b + cross_len)]
    crossed += l1[split_1_at + cross_len:]

    return crossed


def print_collection(collection: list[Candidate | Process]):
    for elem in collection:
        print(elem)


def print_stock(stock: tuple[int]):
    print("\tStock:")
    for key, stock in sorted(zip(Candidate.converter, stock), key=lambda x: x[0]):
        print(f"\t - {key} => {stock}")


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
