#!/bin/sh

case $1 in
  "dev")
    echo "Running dev environment ..."
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;

  "prod")
    echo "Running prod environment ..."
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    ;;

  *)
    echo "Running $@ ..."
    exec "$@"
    ;;
esac
