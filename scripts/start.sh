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
uwsgi --ini ./uwsgi.ini &
celery -A travel worker -P threads -c 3 -l INFO -f ./media/celery.txt &
wait
