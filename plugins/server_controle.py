# coding: utf-8

from slackbot.bot import listen_to

from slackbot.bot import Bot
from slacker import Slacker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from run import Server

import re
import os



Base = declarative_base()
e = Server.engine
Base.metadata.create_all(e)
Session = sessionmaker(bind=e)
session = Session()

@listen_to(r'^add_server\s+\S.*')
def add_server(message):
	tmp, url = message.body['text'].split(None, 1)
	url = re.sub('<', '', url)
	url = re.sub('>', '', url)

	try:
		u = Server(url=url, status=0)
		session.add(u)
		session.commit()
		message.send('ok')
	except Exception as e:
		message.send('%r' % e)
                
@listen_to(r'^rm_server\s+\S.*')
def rm_server(message):
	tmp, url = message.body['text'].split(None, 1)
	url = re.sub('<', '', url)
	url = re.sub('>', '', url)

	try:
		db = session.query(Server).filter( Server.url == url ).delete()
		session.commit()
		message.send('ok')
	except Exception as e:
		message.send('%r' % e)
