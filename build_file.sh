echo "BUILD START"

apt install libpq-dev
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
python3.9 makemigrations
python3.9 migrate