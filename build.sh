echo "BUILD START"
source venv/bin/activate
pip install --upgrade pip  # Ensure pip is up to date
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
echo "BUILD END"
