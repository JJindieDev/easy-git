#!/usr/bin/env bash

set -euo pipefail

# Resolve the project even when this script is invoked through the installed
# ~/.local/bin/easy-git symlink.
SCRIPT_PATH="$(readlink -f -- "${BASH_SOURCE[0]}")"
PROJECT_DIR="$(cd -- "$(dirname -- "$SCRIPT_PATH")" && pwd)"
COMMAND_NAME="$(basename -- "$0")"
PYTHON="${EASY_GIT_PYTHON:-$PROJECT_DIR/.venv/bin/python}"

if [[ ! -x "$PYTHON" ]]; then
    PYTHON="python3"
fi

if [[ "$COMMAND_NAME" == "easy-git" ]]; then
    case "${1:-}" in
        --version)
            exec "$PYTHON" "$PROJECT_DIR/version.py"
            ;;
        --setup)
            exec "$PYTHON" "$PROJECT_DIR/setup.py"
            ;;
        --help|-h)
            printf 'Usage: easy-git [--version|--setup]\n'
            exit 0
            ;;
        *)
            exec "$PYTHON" "$PROJECT_DIR/menu.py" "$@"
            ;;
    esac
fi

INSTALL_DIR="${EASY_GIT_INSTALL_DIR:-${HOME}/.local/bin}"
mkdir -p "$INSTALL_DIR"
ln -sfn "$PROJECT_DIR/install.sh" "$INSTALL_DIR/easy-git"

printf 'Installed easy-git at %s/easy-git\n' "$INSTALL_DIR"
if [[ ":${PATH}:" != *":${INSTALL_DIR}:"* ]]; then
    printf 'Add %s to PATH if it is not already included.\n' "$INSTALL_DIR"
fi
