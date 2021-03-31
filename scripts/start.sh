#!/bin/bash
if [ x$1 != x ]
then
    dir=$1
else
    dir=..
fi
cd $dir
rm ./media/log.txt &
rm ./media/celery.txt &
/usr/bin/python3 manage.py runserver 0.0.0.0:8000 &
celery -A travel worker -c 2 -l INFO -f ./media/celery.txt &
wait
