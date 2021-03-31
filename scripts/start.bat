cd ..
del .\media\log.txt
del .\media\celery.txt
start python manage.py runserver 0.0.0.0:8000
start celery -A travel worker  -c 2  -l INFO 