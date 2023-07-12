pip install -r requirements.txt
pip install psycopg2-binary==2.9.6
python3.9 manage.py collectstatic --noinput
pip list