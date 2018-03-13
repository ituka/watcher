FROM python:3.6

WORKDIR /home
ADD bot /home/bot
ADD wait_db.sh /home/wait_db.sh
RUN apt-get update
RUN apt-get install -y \
  postgresql-9.4
RUN pip3 install \
  slackbot slacker sqlalchemy wget psycopg2 psycopg2-binary

RUN chmod a+x /home/wait_db.sh
CMD ["sh","/home/wait_db.sh"]