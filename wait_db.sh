#!/bin/sh

for i in `seq 0 9`
do
    PGPASSWORD=test psql -U test -p 5432 -h db -l;

    if [ $? = 0 ]; then
        echo 'ok'
        python /home/bot/run.py
		echo 'start'
        break
    else
        echo 'waitting...'
    fi
    sleep 5
done