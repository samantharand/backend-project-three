import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


artworks = Blueprint('artworks', 'artworks')

# test route
@artworks.route('/', methods=['GET'])
def test_route():
	return 'test route'

# create
@artworks.route('/add', methods=['POST'])
def create_art():
	payload = request.get_json()
	# print(payload)
	# print('current user', current_user)

	created_art = models.Artwork.create(
		title = payload['title'],
		inspiration = payload['inspiration'],
		medium = payload['medium'],
		image = payload['image'],
		date_made = payload['date_made'],
		artist = current_user.id
	)

	# print("CREATED ART", create_art)
	created_art_dict = model_to_dict(created_art)
	# print("CREATED ART DICT", created_art_dict)


	return jsonify(
		data = created_art_dict,
		message = f"Succeffully created {created_art_dict['title']}",
		status = 201
	), 201

# all artwork
@artworks.route('/all', methods=['GET'])
def display_all_art():
	artworks = models.Artwork.select()
	# artworks_dict = model_to_dict(artworks)
	# print("artworks_dict", artworks_dict)
	artwork_dicts = [ model_to_dict(artwork) for artwork in artworks]
	for artwork_dict in artwork_dicts:
		artwork_dict['artist'].pop('password')

	print("artwork_dict", artwork_dict)
	# artwork_dicts = 
	return jsonify(
		data = artwork_dicts,
		message = f'Found {len(artworks)} pieces of art :)',
		status = 200
	), 200

# show page
@artworks.route('/<id>', methods=['GET'])
def show_art(id):
	art = models.Artwork.get_by_id(id)
	
	art_dict = model_to_dict(art)
	art_dict['artist'].pop('password')
	print(art_dict)
	return jsonify(
		data = art_dict,
		message = f'Displaying {art_dict["title"]}, ID#{art_dict["id"]}',
		status = 200
	), 200

# edit artwork
@artworks.route('/<id>', methods=['PUT'])
@login_required
def edit_artwork(id):
	payload = request.get_json()
	artwork_to_edit = models.Artwork.get_by_id(id)


	if current_user.id == artwork_to_edit.artist.id:
		
		artwork_to_edit.title = payload['title']
		artwork_to_edit.inspiration = payload['inspiration']
		artwork_to_edit.medium = payload['medium']
		artwork_to_edit.image = payload['image']
		artwork_to_edit.date_made = payload['date_made']

		artwork_to_edit_dict = model_to_dict(artwork_to_edit)
		artwork_to_edit_dict['artist'].pop('password')

		return jsonify(
			data = artwork_to_edit_dict,
			message = 'Successfully edited your art',
			status = 201
		), 201

	else: 

		return jsonify(
			data = {},
			message = "That's not your artwork :(",
			status = 403
		), 403

	# return "check terminal"


# d e s t r o y artwork









