import models

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def users_test_route():
	print('users_test_route')
	return 'users_test_route'

# create new user (register)
@users.route('/', methods=['POST'])
def register():
	## get things adding to db - BUILD OUT THE REST OF THE REgISTER/NEW USER ROUTE 
	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	payload['email'] = payload['email'].lower()
	print(payload)

	# see if username is already registered
	try:
		models.User.get(models.User.username == payload['username'])
		
		return jsonify(
			data = {},
			message = "Sorry, that username is already registered :(",
			status = 401
		), 401

	except models.DoesNotExist:
		# see if email is already registered
		try:
			models.User.get(models.User.email == payload['email'])

			return jsonify(
				data = {},
				message = "Sorry, that email is already registered :(",
				status = 401
			), 401

		except models.DoesNotExist:
			#create account
			created_user = models.User.create(
				username=payload['username'],
				email=payload['email'],
				password=generate_password_hash(payload['password']),
				age=payload['age'],
				location=payload['location'],
				bio=payload['bio'],
			)

			print('CREATED_USER, users.py line 53', created_user)

			login_user(created_user)

			created_user_dict = model_to_dict(created_user)
			created_user_dict.pop('password')
			print('CREATED_USER_DICT, users.py line 60', created_user_dict)

			return jsonify(
				data = created_user_dict,
				message = "User created :)",
				status = 201
			), 201

@users.route('/login', methods=['POST'])
def login_artist():

	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	print("Login route, here's payload", payload)

	# look up username to see if it exists
	try:
		user = models.User.get(models.User.username == payload['username'])
		# check password !! remember hash! 

		user_dict = model_to_dict(user)
		print("USER DICT from line 83 in users", user_dict)
		good_password = check_password_hash(user_dict['password'], payload['password'])

		if good_password:

			login_user(user)

			user_dict.pop('password')
			
			return jsonify(
				data = user_dict,
				message = f'Hey {user_dict["username"]}!',
				status = 201
			), 201

		else:

			print("bad password")

			return jsonify(
				data = {},
				message = "Wrong username or password :(",
				status = 401
			), 401

	except models.DoesNotExist:

		print("bad username")

		return jsonify(
			data = {},
			message = "Wrong username or password :(",
			status = 401
		), 401

# logout
@users.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data = {},
		message = "Successfully logged out. Goodbye :)",
		status = 200
	), 200
	
# user index page
@users.route('/all', methods=['GET'])
def display_all_users():
	users = models.User.select()
	user_dicts = [ model_to_dict(user) for user in users]

	for user_dict in user_dicts:
		user_dict.pop('password')

	# print("USER_DICTS in display_all_users()", user_dicts)
	# print("CURRENT USER in display_all_users()", current_user)
	return jsonify(
		data = user_dicts,
		message = f"{len(user_dicts)} users found!")

# user show route
@users.route('/<id>', methods=['GET'])
def show_user(id):
	user = models.User.get(models.User.id == id)
	user_dict = model_to_dict(user)
	user_dict.pop('password')
	print(user_dict)
	return jsonify(
		data = user_dict,
		message = f'Displaying info for {user_dict["username"]}, ID#{user_dict["id"]}',
		status = 200
	), 200

# edit user
@users.route('/<id>', methods=['PUT'])
@login_required
def edit_user(id):
	payload = request.get_json()
	user_to_edit = models.User.get_by_id(id)

	if current_user.id == user_to_edit.id:

		user_to_edit.username = payload['username']
		user_to_edit.email = payload['email']
		user_to_edit.age = payload['age']
		user_to_edit.location = payload['location']
		user_to_edit.bio = payload['bio']

		user_to_edit.save()

		user_to_edit_dict = model_to_dict(user_to_edit)

		return jsonify(
			data = user_to_edit_dict,
			message = 'Successfully edited your profile',
			status = 201
		), 201

	else:

		return jsonify(
			data = {},
			message = "That's not your account :(",
			status = 403
		), 403


# destroy user
@users.route('/<id>', methods=['DELETE'])
@login_required
def delete_account(id):
	user_to_delete = models.User.get_by_id(id)

	if current_user.id == user_to_delete.id:
		user_to_delete.delete_instance()

		return jsonify(
			data = {},
			message = "account successfully deleted",
			status = 200
		), 200

	else:

		return jsonify(
			data = {},
			message = "That's not your account :(",
			status = 403
		), 403

	return "check term - delete route"

