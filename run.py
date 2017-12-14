# coding: utf-8

from slackbot.bot import Bot
from slacker import Slacker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

import os
import subprocess
import time
import threading

import slackbot_settings



Base = declarative_base()


class Server(Base):
	__tablename__ = 'servers'

	id = Column(Integer, primary_key=True)
	url  = Column(Text, unique=True, nullable=False)
	status = Column(Integer, default=0, nullable=True)

	db_name = 'sqlite://' + slackbot_settings.DB_NAME
	engine = create_engine(db_name)


class WatchThread(threading.Thread):
	def __init__(self):
		super(WatchThread, self).__init__()

	def run(self):
		slack = Slacker(slackbot_settings.API_TOKEN)

		e = Server.engine
		Base.metadata.create_all(e)
		Session = sessionmaker(bind=e)
		session = Session()
		session.commit()

		slack.chat.post_message(
			'test_bot',
			'start',
			as_user=True
		)

		i = 0
		count = len(session.query(Server).all())
		while True:
			try:
				all = session.query(Server).all()
				for row in all:
					cmd = 'wget -q --delete-after ' + row.url
					result = subprocess.call( cmd.split(" ") )
					if result == 0 and row.status == 1:
						row.status = 0
						session.commit()

						slack.chat.post_message(
							'test_bot',
							'revive ' + row.url,
							as_user=True
						)
					elif result == 0 or row.status == 1:
						pass
					else:
						slack.chat.post_message(
							'test_bot',
							'error ' + row.url,
							as_user=True
						)
						row.status = 1
						session.commit()
			except Exception as e:
				slack.chat.post_message(
					'test_bot',
					'%r' % e,
					as_user=True
				)

			time.sleep(slackbot_settings.SLEEP_TIME)


def main():
	bot = Bot()
	bot.run()

if __name__ == "__main__":
	watch_thread = WatchThread()
	watch_thread.start()
	main()
