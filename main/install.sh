#!/usr/bin/env bash

# Install the easy-git command, run setup, and open the Git and GitHub menu.
set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$PWD" -ef "$HOME" ]]; then
    printf '%s\n' "Easy Fit can't run in your home directory."
    exit 1
fi

python3 "$SCRIPT_DIR/setup.py"

mkdir -p "$HOME/.local/bin"
ln -sfn "$SCRIPT_DIR/easy-git" "$HOME/.local/bin/easy-git"

python3 "$SCRIPT_DIR/easy-git"
