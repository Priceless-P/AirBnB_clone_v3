#!/usr/bin/python3
"""
Place_Amenities API
Create a new view for the link between Place objects and
Amenity objects that handles all default RESTFul API actions
Endpoints:
    - GET /places/<place_id>/amenities: Retrieves the list of amenities
      associated with a place.
    - DELETE /places/<place_id>/amenities/<amenity_id>: Deletes an amenity
      from a place.
    - POST /places/<place_id>/amenities/<amenity_id>: Links an amenity to
      a place.
"""

from flask import abort, jsonify, make_response
from models.amenity import Amenity
from api.v1.views import app_views
from os import environ
from models.place import Place
from models import storage


@app_views.route("/places/<string:place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == "db":
        all_amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        all_amenities = [storage.get("Amenity", amenity_id).to_dict()
                         for amenity_id in place.amenity_ids]
    return make_response(jsonify(all_amenities))


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """"Link a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if environ.get("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
