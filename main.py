import sys
import argparse as a

import src.parsing as parser

from src.generate_population import generate_population
from src.utils import print_population

if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("-f", "--file", help="file containing the optimization problem", required=True)
    argparse.add_argument("-p", "--population", default=25, type=int, help="chromosome number for the genetic algo")
    argparse.add_argument("-i", "--iterations", default=1000, type=int,
                          help="the maximum iterations number while generating a chromosome")
    args = argparse.parse_args()

    if int(args.population) < 1 or int(args.population) > 1000:
        argparse.error('[-p] has range(1, 1000)')
    elif int(args.iterations) < 1 or int(args.iterations) > 100000:
        argparse.error('[-p] has range(1, 1000000)')

    memoization: dict[tuple[int]: tuple[tuple[int, tuple[int]]]] = {}
    processes, start = parser.parse(args.file)

    population = generate_population(args, start, processes, memoization)
    print_population(population)
