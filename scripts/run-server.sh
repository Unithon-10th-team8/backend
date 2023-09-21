#!/bin/bash

set -e

ARGS=$@
poetry install --sync
uvicorn app:app --host 0.0.0.0 --port 8000 $ARGS