#!/usr/bin/python3
"""
Creating the view for the blueprint application
This module defines all the endpoint for
the amenity model
"""
from flask import request, abort, jsonify
from . import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from models.user import User


@app_views.route("/places/<place_id>/amenities", methods=["GET", "POST"])
def list_amenities_view(place_id):
    """
    returns the list of amenities in a place
    and also accept new amenities associated to a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "POST":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data.get("user_id"):
            abort(400, "Missing user_id")
        user = storage.get(User, data.get("user_id"))
        if not user:
            abort(404)
        if not data.get("text"):
            abort(400, "Missing text")
        data["place_id"] = place.id
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
    amenities = place.amenities
    serialized_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(serialized_amenities), 200


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE", "POST"])
def place_amenities_detail(place_id, amenity_id):
    """
    This endpoint adds and remove amenities to a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    place_amenity_ids = [am.id for am in place.amenities]
    if storage_t != "db":
        place_amenity_ids = place.amenity_ids
    if request.method == "DELETE":
        if amenity.id not in place_amenity_ids:
            abort(404)
        if storage_t != "db":
            place.amenity_ids.remove(amenity.id)
        else:
            place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        if amenity.id in place_amenity_ids:
            return jsonify(amenity.to_dict()), 200
        if storage_t != "db":
            place.amenity_ids.append(amenity.id)
        else:
            place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
