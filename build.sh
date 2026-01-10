pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python manage.py compress
python3 manage.py collectstatic --noinput