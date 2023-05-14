#!/bin/bash

activate() {
  . .venv/bin/activate
}

run() {
  python3 manage.py runserver
}

if [ "$1" = "act" ]; then
  activate
elif [ "$1" = "run" ]; then 
  run
else
  echo "Invalid argument"
fi
