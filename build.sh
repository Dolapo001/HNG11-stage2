echo "  BUILD START"

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3.12 manage.py collectstatic --noinput --clear

echo "  BUILD END"