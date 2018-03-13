# coding: utf-8

from slackbot.bot import respond_to

from slackbot.bot import Bot
from slacker import Slacker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from run import Server
import slackbot_settings

import re
import os



@respond_to(r'^add_server\s+\S.*')
def add_server(message):
        Base = declarative_base()
        e = Server.engine
        Base.metadata.create_all(e)
        Session = sessionmaker(bind=e)
        session = Session()

        tmp, url = message.body['text'].split(None, 1)
        url = re.sub('<', '', url)
        url = re.sub('>', '', url)

        try:
                adder = Server(url=url, status=0)
                session.add(adder)

                session.commit()
                message.send(slackbot_settings.ADD_SERVER)
        except Exception as e:
                message.send('%r' % e)

        session.close()

@respond_to(r'^rm_server\s+\S.*')
def rm_server(message):
        Base = declarative_base()
        e = Server.engine
        Base.metadata.create_all(e)
        Session = sessionmaker(bind=e)
        session = Session()

        tmp, url = message.body['text'].split(None, 1)
        url = re.sub('<', '', url)
        url = re.sub('>', '', url)

        try:
                session.query(Server).filter(Server.url == url).delete()
                session.commit()
                message.send(slackbot_settings.RM_SERVER)
        except Exception as e:
                message.send('%r' % e)

        session.close()