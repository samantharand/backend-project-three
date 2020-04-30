from flask import Flask

DEBUG=True
PORT=8000

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
	print('hello_world')
	return "Hello, World" 

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)