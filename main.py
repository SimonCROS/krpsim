import argparse as a

import src.parsing as parser

from src.Error import Error
from src.GeneticSolver import evolve
from src.generate_population import generate_population
from src.utils import print_collection, print_candidates_stock

if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("-f", "--file", help="file containing the optimization problem", required=True)
    argparse.add_argument("-p", "--population", default=26, type=int, help="chromosome number for the genetic algo")
    argparse.add_argument("-i", "--iterations", default=1000, type=int,
                          help="maximum iterations while generating a chromosome")
    argparse.add_argument("-g", "--generations", default=10, type=int, help="generations number")
    argparse.add_argument("-r", "--ratio", default=5, type=int, help="mutation ratio")
    args = argparse.parse_args()

    if int(args.population) < 1 or int(args.population) > 1000:
        argparse.error('[-p] has range(1, 1000)')
    elif int(args.population) % 2:
        argparse.error('[-p] has to be odd')
    elif int(args.iterations) < 1 or int(args.iterations) > 100_000_000:
        argparse.error('[-i] has range(1, 100 000 000)')
    elif int(args.generations) < 1 or int(args.generations) > 10_000:
        argparse.error('[-g] has range(1, 100)')
    elif int(args.ratio) < 2 or int(args.ratio) > 25:
        argparse.error('[-r] has range(1, 25)')

    memoization: dict[tuple[int]: tuple[tuple[int, tuple[int]]]] = {}
    processes, start = parser.parse(args.file)

    population = generate_population(args, start, processes, memoization)
    print_candidates_stock(population)
    # population = evolve(population, start, processes, args)
