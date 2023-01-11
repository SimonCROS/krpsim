from src.Candidate import Candidate
from src.Process import Process
from operator import sub, add


def print_collection(collection: list[Candidate | Process]):
    for elem in collection:
        print(elem)
    print("")


def print_cycle(chromosome: Candidate, processes: list[Process]):
    duration = 0
    for i in chromosome.process:
        print(f"{duration}:{processes[i].name}")
        duration += processes[i].delay
    print(f"No more process doable at time {duration + 1}")


def tup_sub(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(sub, a, b))


def tup_add(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(map(add, a, b))
