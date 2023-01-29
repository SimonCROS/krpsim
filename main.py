import argparse as a
import random
import time

import src.parsing as parser
from src.Candidate import Candidate
from src.generate_population import generate_population
from src.GeneticSolver import evolve
from src.utils import print_collection, print_cycle

random.seed(10)


if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument(
        "file", help="file containing the optimization problem")
    argparse.add_argument("delay", type=int, help="maximum execution duration")
    argparse.add_argument("-p", "--population", default=20,
                          type=int, help="population size")
    argparse.add_argument("-i", "--iterations", default=1000, type=int,
                          help="maximum iterations while generating a chromosome")
    argparse.add_argument("-g", "--generations", default=10,
                          type=int, help="generations number")
    argparse.add_argument("-r", "--ratio", default=5,
                          type=int, help="mutation ratio")
    argparse.add_argument("-d", "--demo", action="store_true",
                          default=False, help="show algo efficiency")

    args = argparse.parse_args()

    if args.population < 2 or args.population > 1000:
        argparse.error('[-p] has range(2, 1000)')
    elif args.iterations < 2 or args.iterations > 1_000_000:
        argparse.error('[-i] has range(2, 1 000 000)')
    elif args.generations < 1 or args.generations > 100:
        argparse.error('[-g] has range(1, 100)')
    elif args.ratio < 2 or args.ratio > 25:
        argparse.error('[-r] has range(2, 25)')
    elif args.delay < 1:
        argparse.error('[-r] must be greater or equal than 1')

    start = time.time()

    memoization: dict[tuple: tuple] = {}
    processes, base, goal = parser.parse(args.file)
    population = generate_population(args, base, processes, memoization, start)
    population = evolve(population, base, processes, start, args)

    if args.demo:
        print_collection(population)
        print("")

    stop_type = 1

    # todo STOP_TIME 2

    delta = time.time() - start
    if delta >= args.delay:
        stop_type = 3

    print_cycle(population[0], processes, stop_type)
