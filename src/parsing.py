import re

from src.error import Error


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


def remove_comment(line) -> str:
    lhs = line.split('#')[0]
    lhs = lhs.removesuffix("\n")
    return lhs

def parse(file) :#-> tuple[dict[str, int], list[Task], list[str]]:
    content: list[str] = []

    content = __get_file_content(file)

    content = map(remove_comment, content)
    content = filter(None, content)

    for item in content:
        result = re.search(r"^([^:]+):(\d+)$", item)
        if result:
            print("Pattern 1 found:", result.groups())
        else:
            result = re.search(r"^([^:]+):((?=\()[^)]*\)):((?=\()[^)]*\)):(\d+)$", item)
            if result:
                print("Pattern 2 found:", result.groups())
            else:
                result = re.search(r"^([^:]+):((?=\()[^)]*\))$", item)
                if result:
                    print("Pattern 3 found:", result.groups())
                else:
                    Error.throw(Error.FAIL, Error.FILE_FORMAT_ERROR,
                                f"file format error: unknown patterm : '{item}'")
