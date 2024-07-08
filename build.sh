#!/bin/bash
echo "BUILD START"

# Ensure pip is installed
python3 -m ensurepip --upgrade

# Install virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
