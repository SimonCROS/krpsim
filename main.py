import argparse as a

import src.parsing as parser

from src.Error import Error
from src.GeneticSolver import evolve
from src.generate_population import generate_population
from src.utils import print_collection, print_cycle

if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("-f", "--file", help="file containing the optimization problem", required=True)
    argparse.add_argument("-p", "--population", default=26, type=int, help="population size")
    argparse.add_argument("-i", "--iterations", default=1000, type=int, help="maximum iterations while generating a chromosome")
    argparse.add_argument("-g", "--generations", default=10, type=int, help="generations number")
    argparse.add_argument("-r", "--ratio", default=5, type=int, help="mutation ratio")
    argparse.add_argument("-d", "--demo", action="store_true", default=False, help="show algo efficiency")

    args = argparse.parse_args()

    if args.population < 1 or args.population > 1000:
        argparse.error('[-p] has range(1, 1000)')
    elif args.population % 2:
        argparse.error('[-p] has to be odd')
    elif args.iterations < 1 or args.iterations > 1_000_000:
        argparse.error('[-i] has range(1, 1 000 000)')
    elif args.generations < 1 or args.generations > 100:
        argparse.error('[-g] has range(1, 100)')
    elif args.ratio < 2 or args.ratio > 25:
        argparse.error('[-r] has range(2, 25)')

    memoization: dict[tuple: tuple] = {}
    processes, start, pb_type = parser.parse(args.file)
    population = generate_population(args, start, processes, pb_type, memoization)
    population = evolve(population, start, processes, args)
    if args.demo:
        print_collection(population)
    print_cycle(population[0], processes, pb_type)

