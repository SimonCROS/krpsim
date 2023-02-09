from __future__ import annotations

import copy
import random
import time

from src.Chromosome import Chromosome
from src.Process import Process


def generate_population(base: Chromosome, processes: list[Process], start: float, args) -> list[Chromosome]:
    population: list[Chromosome] = []
    i = 0

    for _ in range(args.population):
        chromosome = copy.deepcopy(base)
        for _ in range(args.iterations):
            p = random.choice(processes)
            chromosome.try_do_process(p, insert_none=True)

            if i % 1000 == 0:
                delta = time.time() - start
                if delta >= args.delay:
                    return population

            i += 1
        population.append(chromosome)

    return population
