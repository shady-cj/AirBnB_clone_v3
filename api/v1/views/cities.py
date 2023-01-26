#!/usr/bin/python3
"""
Creating the view for the blueprint application
This module defines all the endpoint for
the city model
"""
from flask import request, abort, jsonify
from . import app_views
from models import storage, storage_t
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def list_cities_view(state_id):
    """
    returns the list of cities in a state
    and also accept new cities associated to a state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "POST":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data.get("name"):
            abort(400, "Missing name")
        data["state_id"] = state.id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    cities = state.cities
    serialized_cities = [city.to_dict() for city in cities]
    return jsonify(serialized_cities), 200


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def detail_cities_view(city_id):
    """
    returning the detail of city based on city_id
    in the database and also allows
    updating, deleting.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "DELETE":
        storage.delete(city)
        return jsonify({}), 200
    elif request.method == "PUT":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        data["id"] = city.id
        data["created_at"] = city.created_at
        if "updated_at" in data:
            data.pop("updated_at")
        if "state_id" in data:
            data.pop("state_id")
        if storage_t == "db":
            storage.update(city, data)
            updated_city = storage.get(City, city.id)
        else:
            updated_city = City(**data)
            updated_city.save()
        return jsonify(updated_city.to_dict()), 200
    return jsonify(city.to_dict()), 200
