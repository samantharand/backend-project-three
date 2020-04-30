from flask import Flask
import models

from resources.users import users

DEBUG=True
PORT=8000

app = Flask(__name__)

app.register_blueprint(users, url_prefix="/users")

@app.route('/', methods=['GET'])
def hello_world():
	print('hello_world')
	return "Hello, World" 

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)