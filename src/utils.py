from src.Candidate import Candidate
from src.Process import Process
from operator import sub, add


def print_collection(collection: list[Candidate | Process]):
    for elem in collection:
        print(elem)


def print_candidates_stock(population: list[Candidate]):
    for chromosome in population:
        chromosome.show_stock()


def tup_sub(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(sub, a, b))


def tup_add(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(add, a, b))
