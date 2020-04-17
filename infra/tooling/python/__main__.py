import sys
from argparse import ArgumentParser, ArgumentTypeError
from subprocess import call

DEFAULT_PATH_ROOT = "."


class ReturnError(Exception):
    pass


def shell(command: str) -> None:
    print(">>> " + command)
    return_code = call(command, shell=True)
    if return_code:
        sys.tracebacklimit = 0
        raise ReturnError(f"Command returned code: {return_code}")


class FormatTasks:
    @staticmethod
    def black(path: str) -> None:
        command = (
            f"find {path} -name \\*.py | "
            f"xargs black --line-length 90 --target-version py37"
        )
        shell(command)

    @staticmethod
    def isort(path: str) -> None:
        command = f"find {path} -name \\*.py | " f"xargs isort --dont-skip __init__.py"
        shell(command)

    @staticmethod
    def run(path: str) -> None:
        FormatTasks.isort(path=path)
        FormatTasks.black(path=path)


class LintTasks:
    @staticmethod
    def flake8(path: str) -> None:
        command = f"find {path} -name \\*.py | " f"xargs flake8"
        shell(command)

    @staticmethod
    def pylint(path: str) -> None:
        command = f"find {path} -name \\*.py | " f"xargs pylint --jobs=2"
        shell(command)

    @staticmethod
    def mypy(path: str) -> None:
        command = (
            f"find {path} -name \\*.py | "
            f"xargs mypy --ignore-missing-imports --disallow-untyped-defs"
        )
        shell(command)

    @staticmethod
    def run(path: str) -> None:
        LintTasks.flake8(path=path)
        LintTasks.pylint(path=path)
        LintTasks.mypy(path=path)


def parse_boolean(value: str) -> bool:
    if value.lower() in {"yes", "true", "t", "y", "1"}:
        return True
    elif value.lower() in {"no", "false", "f", "n", "0"}:
        return False
    else:
        raise ArgumentTypeError(f"Couldn't infer boolean value from '{value}'")


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-f",
        "--format",
        help="Run all format tasks",
        type=parse_boolean,
        const=True,
        default=False,
        required=False,
        nargs="?",
    )
    parser.add_argument(
        "-l",
        "--lint",
        help="Run all lint tasks",
        type=parse_boolean,
        const=True,
        default=False,
        required=False,
        nargs="?",
    )
    parser.add_argument(
        "-p",
        "--path",
        help="The path to run the tasks on",
        default=DEFAULT_PATH_ROOT,
        required=False,
    )

    args = parser.parse_args()

    if args.format:
        FormatTasks.run(path=args.path)
    if args.lint:
        LintTasks.run(path=args.path)
