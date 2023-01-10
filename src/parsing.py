import copy
import regex

from src.Error import Error
from src.Candidate import Candidate
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
            Error.print(Error.FAIL, Error.FILE_FORMAT_ERROR,
                        f"file format error: empty resource : '{part}' in '({item})'")
        kv = part.split(':')
        if len(kv) != 2 or not len(kv[0]) or not len(kv[1]):
            Error.print(Error.FAIL, Error.FILE_FORMAT_ERROR,
                        f"file format error: resource bad format (`key:value` required) : '{part}' in '({item})'")
        resources[kv[0]] = kv[1]
        stock.add(kv[0])
    return resources


def __remove_comment(line) -> str:
    lhs = line.split('#')[0]
    lhs = lhs.removesuffix("\n")
    return lhs


def __convert_resources(converter: dict[str: int], resources: dict[str: str] | None) -> tuple[int]:
    if resources:
        for k, v in resources.items():
            converter[k] = int(v)
    return tuple(converter.values())


def __get_resources_converter(goal: set[str], stock: set[str]) -> dict[str: int]:
    converter: dict[str: int] = {}
    optimize: str = goal.intersection(stock).pop()
    stock: list[str] = list(stock)
    stock.remove(optimize)

    for s in stock:
        converter[s] = 0
    converter[optimize] = 0

    return converter


def __get_processes(converter: dict[str: int], processes: list[dict]):
    Processes: list[Process] = []

    for process in processes:
        Processes.append(Process(
            name=process['name'],
            cost=__convert_resources(copy.deepcopy(converter), process['cost']),
            gain=__convert_resources(copy.deepcopy(converter), process['gain']),
            delay=int(process['delay'])
        ))
    return Processes


def parse(file) -> list[list[Process], Candidate]:
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
            result = regex.search(r"^([^:]+):((?:(?=\()[^)]*\))?):((?=\()[^)]*\))?:(\d+)$", item)
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
                    Error.print(Error.FAIL, Error.FILE_FORMAT_ERROR,
                                f"file format error: unknown patterm : '{item}'")

    converter = __get_resources_converter(goal, stock)
    processes = __get_processes(converter, processes)
    start = Candidate([], __convert_resources(converter, start), 0)

    return [processes, start]
