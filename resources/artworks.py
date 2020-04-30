import models

from flask import Blueprint, request, jsonify

artworks = Blueprint('artworks', 'artworks')

# test route
@artworks.route('/', methods=['GET'])
def test_route():
	return 'test route'