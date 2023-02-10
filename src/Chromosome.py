from __future__ import annotations

import copy
import random
from src.Process import Process
from src.utils import tup_add, tup_sub

import sys

CHANGE_RATIO = 0.1

class Chromosome:
    processes: list[Process | None]
    stock: tuple[int]
    fitness: float
    duration: int
    process_count: int

    converter: dict[str: int]
    goal: list[int]

    def cross(base: Chromosome, c1: Chromosome, c2: Chromosome, processes: list[Process]) -> list[int]:
        global CHANGE_RATIO

        max_fill = len(processes) - 1
        result = copy.deepcopy(base)

        for a, b in zip(c1.processes, c2.processes):
            r = random.random()

            if r >= 1 - CHANGE_RATIO:
                process = processes[random.randint(0, max_fill)]
            elif r < (1 - CHANGE_RATIO) / 2:
                process = a
            else:
                process = b
            result.try_do_process(process, insert_padding=True)

        return result

    def __init__(self, process: list[int], stock: tuple[int], fitness: int):
        self.processes = process
        self.stock = stock
        self.fitness = fitness
        self.duration = 0
        self.process_count = 0

    def __str__(self):
        s: list[str] = []
        for key, stock in zip(Chromosome.converter, self.stock):
            s.append(f"{key}:{stock}")
        return f"{len(self.processes)} - ({';'.join(s)}) - {self.fitness} - {self.duration}"

    def calc_fitness(self):
        self.fitness = 0
        for i, x in enumerate(self.stock):
            self.fitness += Chromosome.goal[i] * x
        return self.fitness

    def try_do_process(self, process: Process | None, insert_padding: bool = False) -> bool:
        if not process:
            if insert_padding:
                self.processes.append(None)
            return False

        tmp = tup_sub(self.stock, process.cost)
        if min(tmp) < 0:
            if insert_padding:
                self.processes.append(None)
            return False

        self.processes.append(process)
        self.stock = tup_add(tmp, process.gain)
        self.duration += process.delay
        self.process_count += 1

        return True

    def undo_last_process(self) -> Process:
        last_process = self.processes.pop()
        tmp = tup_sub(self.stock, last_process.gain)

        self.stock = tup_add(tmp, last_process.cost)
        self.duration -= last_process.delay
        self.process_count -= 1

        return last_process
