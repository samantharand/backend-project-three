import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user


artworks = Blueprint('artworks', 'artworks')

# test route
@artworks.route('/', methods=['GET'])
def test_route():
	return 'test route'

# create
@artworks.route('/addart', methods=['POST'])
def create_art():
	payload = request.get_json()
	print(payload)
	print('current user', current_user)

	created_art = models.Artwork.create(
		title = payload['title'],
		inspiration = payload['inspiration'],
		medium = payload['medium'],
		date_made = payload['date_made'],
		artist = current_user.id
	)

	print("CREATED ART", create_art)
	created_art_dict = model_to_dict(created_art)
	print("CREATED ART DICT", created_art_dict)


	return jsonify(
		data = created_art_dict,
		message = f"Succeffully created {created_art_dict['title']}",
		status = 201
	), 201