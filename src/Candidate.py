from __future__ import annotations

import random
from src.Process import Process
from src.utils import tup_add, tup_sub


class Candidate:
    process: list[int]
    stock: tuple[int]
    fitness: float
    duration: int

    converter: dict[str: int]
    goal: list[int]

    def cross(c1: Candidate, c2: Candidate, processes: list[Process]) -> list[int]:
        result = []
        max_fill = len(processes) - 1

        for a, b in zip(c1.process, c2.process):
            r = random.random()

            if r >= 0.90 or (a < 0 and b < 0):
                result.append(random.randint(0, max_fill))

            if r < 0.45 or b < 0:
                result.append(a)
            else:
                result.append(b)

        return result

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

    def calc_fitness(self):
        self.fitness = 0
        for i, x in enumerate(self.stock):
            self.fitness += Candidate.goal[i] * x
        return self.fitness

    def try_do_process(self, process: Process) -> bool:
        tmp = tup_sub(self.stock, process.cost)
        if min(tmp) < 0:
            self.process.append(-1)
            return False
        self.process.append(process.id)
        self.stock = tup_add(tmp, process.gain)
        self.duration += process.delay
        return True
