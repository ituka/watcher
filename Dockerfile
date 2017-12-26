FROM python:3.6

ADD bot /bot/
WORKDIR /bot/
RUN pip3 install slackbot
RUN pip3 install slacker
RUN /bin/sh -c pip3 install sqlite3
RUN pip3 install sqlalchemy
RUN pip3 install wget
RUN cd /bot

CMD ["python","run.py"]


