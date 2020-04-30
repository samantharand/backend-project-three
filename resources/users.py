import models

from flask import Blueprint, request

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def users_test_route():
	print('users_test_route')
	return 'users_test_route'