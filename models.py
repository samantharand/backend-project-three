import os
from peewee import *
import datetime

from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
	DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
	DATABASE = SqliteDatabase('quart.sqlite', pragmas = {"foreign_keys": 1})

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


class Artwork(Model):
	title = CharField()
	artist = ForeignKeyField(User, backref='artworks', on_delete="CASCADE")
	inspiration = TextField()
	medium = CharField()
	image = TextField()
	date_made = DateField()
	date_posted = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Artwork], safe=True)
	print('Connected to database [models.py line 23]')

	DATABASE.close()