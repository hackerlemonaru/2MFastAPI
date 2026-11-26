#!/usr/bin/env bash
# usage: run-tests.sh [pytest args...]  (WSL; env from 2FastAPI/setup-wsl.sh; 2FastAPI checked out next to this repo)
export PATH="$HOME/.local/bin:/usr/bin:/bin"
. "$HOME/2fa-venv/bin/activate"
cd "$(dirname "$0")"
export PYTHONPATH="$PWD/src:$PWD/../2FastAPI/src"
python -m pytest -q -p no:cacheprovider "$@" 2>&1 | tail -${TAILN:-40}
