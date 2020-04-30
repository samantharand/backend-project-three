from peewee import *
import datetime

from flask_login import UserMixin

DATABASE = SqliteDatabase('quart.sqlite')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()
	age = IntegerField()
	location = CharField()
	bio = TextField()
	date_registered = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)
	print('Connected to database [models.py line 23]')

	DATABASE.close()