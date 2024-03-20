#!/bin/bash

# Cleanup
rm ./cache/* # Clear cache
find . -type d -name '__pycache__' -exec rm -r {} + # Remove all pycache directories

if [[ $1 == "--from-scratch" ]]; then
    # Setup virtual environment
    rm -rf .venv # Remove existing virtual environment
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

# Start app.py
python app.py
