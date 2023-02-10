import os
import re
import argparse as a

import src.parsing as parser
from src.Error import Error
from src.Candidate import Candidate
from src.utils import tup_add, tup_sub, print_stock

PROCESS_PATTERN = '^\d+:[a-z|A-Z|\d|_]+\n$'
END_PATTERN = '^\d+:end$'


def parse_output(file_name: str, processes_names: list[str]) -> list[list[int], list[str], int]:
    if not os.path.exists(file_name):
        Error.throw(Error.FAIL, Error.FILE_NOT_FOUND_ERROR, f"no such file: {file_name}")
    with open("output.txt", 'r') as f:
        cycles: list[int] = []
        processes: list[str] = []
        lines: list[str] = f.readlines()
        end: str = lines.pop()

        if not re.match(END_PATTERN, end):
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"invalid syntax: {end}")
        for line in lines:
            if re.match(PROCESS_PATTERN, line):
                cycle, process = line.removesuffix('\n').split(':')
                cycles.append(int(cycle))
                processes.append(process)
            else:
                Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR, f"invalid syntax: {line}")
            if processes[-1] not in processes_names:
                processes_names = [f'"{process}"' for process in processes_names]
                Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                            f'invalid process name: "{processes[-1]}" must be present in {", ".join(processes_names)}')

    end_cycle: int = int(end.split(':')[0])

    return [cycles, processes, end_cycle]


def calcul_stock(base: Candidate, processes, processes_names):
    for process_name in processes_names:
        base.stock = tup_sub(base.stock, processes[process_name].cost)
        base.stock = tup_add(base.stock, processes[process_name].gain)


def verify_output(processes_verif: dict[str: int], cycles_output: list[int], processes_output: list[str],
                  end_cycle: int):
    cycles_verif: list[int] = [0]
    for i, process in enumerate(processes_output):
        cycles_verif.append(processes_verif[process] + cycles_verif[-1])
        if cycles_verif[i] != cycles_output[i]:
            Error.throw(Error.FAIL, Error.OUTPUT_ERROR,
                        f"error in output when {process} at cycle {cycles_output[i]}, should be {cycles_verif[i]}")
    if cycles_verif[-1] != end_cycle:
        Error.throw(Error.FAIL, Error.OUTPUT_ERROR,
                    f"error at end, cycle {end_cycle}, should be {cycles_verif[-1]}")


if __name__ == '__main__':
    argparse = a.ArgumentParser()
    argparse.add_argument("file", help="file containing the optimization problem")
    argparse.add_argument("result_to_verify", help="file containing the result to verify")

    args = argparse.parse_args()
    processes, base, goal = parser.parse(args.file)

    processes_verif = {process.name: process.delay for process in processes}
    cycles_output, processes_output, end_cycle = parse_output(args.result_to_verify, list(processes_verif.keys()))
    verify_output(processes_verif, cycles_output, processes_output, end_cycle)

    processes_verif = {process.name: process for process in processes}
    calcul_stock(base, processes_verif, processes_output)
    print_stock(base.stock)

    print(f"\n\tProcesses stop at time {end_cycle}\n")