import regex

from src.error import Error
from src.task import Task

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


def __to_resources(item: str) -> dict[str, int]:
    if not item:
        return []
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
    return []

def __remove_comment(line) -> str:
    lhs = line.split('#')[0]
    lhs = lhs.removesuffix("\n")
    return lhs

def parse(file) -> tuple[dict[str, int], list[Task], list[str]]:
    content: list[str] = []

    content = __get_file_content(file)

    content = map(__remove_comment, content)
    content = filter(None, content)

    tasks: list[Task] = []

    for item in content:
        result = regex.search(r"^([^:]+):(\d+)$", item)
        if result:
            print("Pattern 1 found:", result.groups())
        else:
            result = regex.search(r"^([^:]+):((?:(?=\()[^)]*\))?):((?=\()[^)]*\)):(\d+)$", item)
            if result:
                tasks.append(Task(result.group(1), __to_resources(result.group(2)), __to_resources(result.group(3)), int(result.group(4))))
            else:
                result = regex.search(r"^([^:]+):((?=\()[^)]*\))$", item)
                if result:
                    print("Pattern 3 found:", result.groups())
                else:
                    Error.print(Error.FAIL, Error.FILE_FORMAT_ERROR,
                                f"file format error: unknown patterm : '{item}'")
