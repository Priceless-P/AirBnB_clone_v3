#!/usr/bin/python3
"""This file creates a user view"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get all users information."""
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get information for the specified user."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user based on user_id."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new user."""
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Update user information."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in data.items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())
