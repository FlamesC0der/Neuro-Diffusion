#!/bin/zsh
dir=$(dirname "$0")
cd "$dir"
source .venv/bin/activate
pip install -r requirements.txt
pip install torch torchvision torchaudio
clear
python3 main.py