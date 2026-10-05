from pathlib import Path

# Note: keep the setup flag beside this file, so status works from any
# directory the program is launched in.
SETUP_FLAG = Path(__file__).with_name("setup_done.flag")


def is_configured():
    return SETUP_FLAG.is_file()


# Note: expose the current state for callers that prefer a simple boolean.
setup_done = is_configured()
