#!/bin/zsh
dir=$(dirname "$0")
cd "$dir"
source .venv/bin/activate

pip install -r requirements.txt
clear
python3 main.py