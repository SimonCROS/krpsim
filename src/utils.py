from __future__ import annotations

import random
from operator import add, sub

def cross_list(l1: list, l2: list):
    len_a = len(l1)
    len_b = len(l2)

    amount1 = random.randint(0, len_a)
    split_1_at = random.randint(0, amount1)
    split_2_b = random.randint(0, len_b)
    cross_len = len_a - amount1

    crossed = l1[:split_1_at]
    crossed += l2[max(0, min(split_2_b, len_b - cross_len))
                      :min(len_b, split_2_b + cross_len)]
    crossed += l1[split_1_at + cross_len:]

    return crossed

def tup_sub(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(sub, a, b))


def tup_add(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(add, a, b))
