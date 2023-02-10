import argparse as a
import time

import src.parsing as parser
from src.generate_population import generate_population
from src.GeneticSolver import evolve
from src.print import print_collection, print_cycle


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
    argparse.add_argument("-d", "--demo", action="store_true",
                          default=False, help="show algo efficiency")

    args = argparse.parse_args()

    if args.population < 2:
        argparse.error('[-p] must be greater or equal than 2')
    elif args.iterations < 2:
        argparse.error('[-i] must be greater or equal than 2')
    elif args.generations < 1:
        argparse.error('[-g] must be greater or equal than 1')
    elif args.delay < 1:
        argparse.error('[-r] must be greater or equal than 1')

    start = time.time()

    processes, base, goal = parser.parse(args.file)
    population = generate_population(base, processes, start, args)
    population = evolve(population, base, processes, start, "time" in goal, args)

    if args.demo:
        print_collection(population)
        print("")

    delta = time.time() - start
    print_cycle(population[0], processes, delta >= args.delay)
