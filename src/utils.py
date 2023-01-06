from src.Candidate import Candidate
from operator import sub, add


def print_population(population: list[Candidate]):
    for chromosome in population:
        print(chromosome)


def tup_sub(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(sub, a, b))


def tup_add(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(add, a, b))
