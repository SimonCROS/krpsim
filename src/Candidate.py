import sys


class Candidate:
    process: list[int]
    stock: tuple[int]
    fitness: int
    duration: int

    converter: dict[str: int]
    goal: list[int]

    def __init__(self, process: list[int], stock: tuple[int], fitness: int):
        self.process = process
        self.stock = stock
        self.fitness = fitness
        self.duration = 0

    def __str__(self):
        s: list[str] = []
        for key, stock in zip(Candidate.converter, self.stock):
            s.append(f"{key}:{stock}")
        return f"{len(self.process)} - ({';'.join(s)}) - {self.fitness} - {self.duration}"
