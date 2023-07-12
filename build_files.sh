# build_files.sh
pip list
pip install -r requirements.txt
py manage.py collectstatic --noinput
pip list