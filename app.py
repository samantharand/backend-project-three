from flask import Flask
import models

from resources.users import users
from flask_login import LoginManager

DEBUG=True
PORT=8000

app = Flask(__name__)

# configuring login manager
app.secret_key = "dont hack me pls"
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(users, url_prefix="/users")

@app.route('/', methods=['GET'])
def hello_world():
	print('hello_world')
	return "Hello, World" 

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)