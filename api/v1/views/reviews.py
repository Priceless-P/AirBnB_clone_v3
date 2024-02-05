#!/usr/bin/python3
"""review_views.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """Get reviews for a specified place."""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    reviews_data = [review.to_dict() for review in place_obj.reviews]
    return jsonify(reviews_data)


@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review_details(review_id):
    """Get review details for a specified review."""
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review based on its review_id."""
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    review_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review."""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_obj = storage.get("User", data['user_id'])
    if user_obj is None:
        abort(404)
    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review."""
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for attr, value in data.items():
        if attr not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review_obj, attr, value)
    review_obj.save()
    return jsonify(review_obj.to_dict())