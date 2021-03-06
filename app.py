import os
from flask import Flask, jsonify, g
import models

from resources.users import users
from resources.artworks import artworks
from flask_login import LoginManager
from flask_cors import CORS

DEBUG=True
PORT=8000

app = Flask(__name__)

# configuring login manager
app.secret_key = "dont hack me pls"
login_manager = LoginManager()
login_manager.init_app(app)

# making the session ! 
@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get_by_id(user_id)
	except models.DoesNotExist:
		return None

# auth message
@login_manager.unauthorized_handler
def unauthoried():
	return jsonify(
		data = {
			'ERROR': 'user not logged in'
		},
		message = 'You have to be logged in to do that!',
		status = 404
	), 404

# CORS
CORS(artworks, origins=['http://localhost:3000', 'https://qu-art.herokuapp.com'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000', 'https://qu-art.herokuapp.com'], supports_credentials=True)

# blueprints
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(artworks, url_prefix='/artworks')

@app.before_request
def before_request():
	print('you should see this before each request')
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	print('you should see this after')
	g.db.close()
	return response


@app.route('/', methods=['GET'])
def hello_world():
	print('hello_world')
	return "Hello, World" 



if 'ON_HEROKU' in os.environ:
	print('\non heroku!! :)')
	models.initialize()

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)