#!/bin/bash

# Clear cache
rm ./cache/*

# Remove all pycache directories
find . -type d -name '__pycache__' -exec rm -r {} +