from __future__ import annotations

import copy

import regex

from src.Candidate import Candidate
from src.Error import Error
from src.Process import Process


def __get_file_content(file: str) -> list[str]:
    lines: list[str] = []

    try:
        f = open(file, 'r')
        lines = f.readlines()
    except FileNotFoundError:
        Error.throw(Error.FAIL, Error.FILE_NOT_FOUND_ERROR,
                    f"no such file: {file}")
    except IsADirectoryError:
        Error.throw(Error.FAIL, Error.IS_A_DIRECTORY_ERROR,
                    f"is a directory: {file}")
    except PermissionError:
        Error.throw(Error.FAIL, Error.PERMISSION_ERROR,
                    f"permission denied: {file}")
    except UnicodeDecodeError:
        Error.throw(Error.FAIL, Error.UNICODE_DECODE_ERROR,
                    f"'utf-8' codec can't decode byte: {file}")
    return lines


def __to_resources(item: str, stock: set) -> dict[str: int]:
    if not item:
        return []
    resources: dict[str: int] = {}
    item = item.removeprefix('(').removesuffix(')')
    parts = item.split(';')
    for part in parts:
        if not part:
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                        f"file format error: empty resource : '{part}' in '({item})'")
        kv = part.split(':')
        if len(kv) != 2 or not len(kv[0]) or not len(kv[1]):
            Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                        f"file format error: resource bad format (`key:value` required) : '{part}' in '({item})'")
        resources[kv[0]] = kv[1]
        stock.add(kv[0])
    return resources


def __remove_comment(line) -> str:
    lhs = line.split('#')[0]
    lhs = lhs.removesuffix("\n")
    return lhs


def __convert_resources(resources: dict[str: str] | None) -> tuple[int]:
    converter = copy.deepcopy(Candidate.converter)

    if resources:
        for k, v in resources.items():
            converter[k] = int(v)
    return tuple(converter.values())


def __set_candidate_converter(goal_keys: set[str], stock_keys: set[str]):
    size: int = len(goal_keys)
    converter: dict[str: int] = {}

    for s in stock_keys:
        converter[s] = 0

    Candidate.converter = converter

    goal: list[int] = list(converter.values())
    for i, k in enumerate(converter.keys()):
        if k in goal_keys:
            goal[i] = size
            size -= 1
    Candidate.goal = goal


def __get_processes(data: list[dict]):
    processes: list[Process] = []

    for process in data:
        processes.append(Process(
            name=process['name'],
            cost=__convert_resources(process['cost']),
            gain=__convert_resources(process['gain']),
            delay=int(process['delay'])
        ))
    return processes


def parse(file) -> list[list[Process], Candidate, tuple[int]]:
    content = __get_file_content(file)
    content = map(__remove_comment, content)
    content = filter(None, content)

    stock: set[str] = set()
    goal: set[str] = set()
    start: dict[str: str] = {}
    processes: list[dict] = []

    for item in content:
        result = regex.search(r"^([^:]+):(\d+)$", item)
        if result:
            stock.add(result.group(1))
            start[result.group(1)] = result.group(2)
        else:
            result = regex.search(
                r"^([^:]+):((?:(?=\()[^)]*\))?):((?=\()[^)]*\))?:(\d+)$", item)
            if result:
                processes.append({
                    'name': result.group(1),
                    'cost': __to_resources(result.group(2), stock),
                    'gain': __to_resources(result.group(3), stock),
                    'delay': result.group(4)
                })
            else:
                result = regex.search(r"^([^:]+):((?=\()[^)]*\))$", item)
                if result:
                    goal.update(result.group(2)[1:-1].split(';'))
                else:
                    Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                                f"file format error: unknown patterm : '{item}'")

    __set_candidate_converter(goal, stock)
    processes = __get_processes(processes)
    start = Candidate([], __convert_resources(start), 0)

    return [processes, start, goal]
