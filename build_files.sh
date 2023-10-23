echo "BUILD START"
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear --settings=food_kitchen.settings
echo "BUILD END"