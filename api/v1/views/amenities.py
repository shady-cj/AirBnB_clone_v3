#!/usr/bin/python3
"""
Creating the view for the blueprint application
creating endpoints for amenities
"""
from flask import request, abort, jsonify
from . import app_views
from models import storage, storage_t
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET", "POST"])
def list_amenitys_view():
    """
    returns the list of amenitys
    and also accept new amenity
    """
    if request.method == "POST":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data.get("name"):
            abort(400, "Missing name")
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
    amenities = storage.all(Amenity).values()
    serialized_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(serialized_amenities), 200


@app_views.route("/amenities/<id>", methods=["GET", "DELETE", "PUT"])
def detail_amenitys_view(id):
    """
    retrieving amenity object based on amenity_id
    in the database and also allows
    updating, deleting.
    """
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    if request.method == "DELETE":
        storage.delete(amenity)
        return jsonify({}), 200
    elif request.method == "PUT":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        data["id"] = amenity.id
        data["created_at"] = amenity.created_at
        if "updated_at" in data:
            data.pop("updated_at")
        if storage_t == "db":
            storage.update(amenity, data)
            updated_amenity = storage.get(Amenity, amenity.id)
        else:
            updated_amenity = Amenity(**data)
            updated_amenity.save()
        return jsonify(updated_amenity.to_dict()), 200
    return jsonify(amenity.to_dict()), 200
