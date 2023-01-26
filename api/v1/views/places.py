#!/usr/bin/python3
"""
Creating the view for the blueprint application
This module defines all the endpoint for
the city model
"""
from flask import request, abort, jsonify
from . import app_views
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def list_places_view(city_id):
    """
    returns the list of places in a city
    and also accept new places associated to a city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "POST":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")

        data = request.get_json()
        if not data.get("user_id"):
            abort(400, "Missing user_id")
        get_user = storage.get(User, data["user_id"])
        if not get_user:
            abort(404)
        if not data.get("name"):
            abort(400, "Missing name")
        data["city_id"] = city.id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    places = city.places
    serialized_places = [place.to_dict() for place in places]
    return jsonify(serialized_places), 200


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def detail_places_view(place_id):
    """
    returning the detail of place based on place_id
    in the database and also allows
    updating, deleting.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "DELETE":
        storage.delete(place)
        return jsonify({}), 200
    elif request.method == "PUT":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        data["id"] = place.id
        data["created_at"] = place.created_at
        if "updated_at" in data:
            data.pop("updated_at")
        if "city_id" in data:
            data.pop("city_id")
        if "user_id" in data:
            data.pop("user_id")
        if storage_t == "db":
            storage.update(place, data)
            updated_place = storage.get(Place, place.id)
        else:
            updated_place = Place(**data)
            updated_place.save()
        return jsonify(updated_place.to_dict()), 200
    return jsonify(place.to_dict()), 200
