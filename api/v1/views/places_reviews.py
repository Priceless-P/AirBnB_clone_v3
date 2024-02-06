#!/usr/bin/python3
"""review_routes.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review as Rv
from models.user import User as Usr
from models.place import Place as Plc


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def fetch_reviews(place_id):
    """Retrieve reviews for a specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews_info = []
    for rvw in place.reviews:
        reviews_info.append(rvw.to_dict())
    return jsonify(reviews_info)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_review(review_id):
    """Retrieve information for a specified review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_review(review_id):
    """Remove a review based on its ID"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Add a new review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Data not in JSON format'}), 400)
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return make_response(jsonify({'error': 'User ID missing'}), 400)
    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(404)
    if 'text' not in kwargs:
        return make_response(jsonify({'error': 'Text field missing'}), 400)
    kwargs['place_id'] = place_id
    review = Rv(**kwargs)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update an existing review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Data not in JSON format'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict())
