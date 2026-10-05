from pathlib import Path
import os
import runpy
import sys


ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "main"
VERSION_FILE = APP_DIR / "VERSION"


def run_script(filename):
    runpy.run_path(str(APP_DIR / filename), run_name="__main__")


def main():
    # Notes: read the displayed version from the VERSION file.
    if sys.argv[1:] == ["--version"] or sys.argv[1:] == ["-V"]:
        print(VERSION_FILE.read_text(encoding="utf-8").strip())
        return 0

    if sys.argv[1:] == ["setup"]:
        # Notes: run setup from the project folder regardless of the caller's folder.
        previous_directory = os.getcwd()
        try:
            os.chdir(ROOT)
            run_script("setup.py")
        finally:
            os.chdir(previous_directory)
        return 0

    if not sys.argv[1:]:
        run_script("main.py")
        return 0

    if sys.argv[1:] in (["--help"], ["-h"]):
        print("Usage: easy-git [setup | --version | --help]")
        print("Run easy-git with no options to open the Git and GitHub menu.")
        return 0

    print("Usage: easy-git [setup | --version | --help]")
    return 2


if __name__ == "__main__":
    sys.exit(main())
