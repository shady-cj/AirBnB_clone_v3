#!/usr/bin/python3
"""
Creating the view for the blueprint application
"""
from flask import request, abort, jsonify
from . import app_views
from models import storage, storage_t
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def list_states_view():
    """
    returns the list of states
    and also accept new state
    """
    if request.method == "POST":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data.get("name"):
            abort(400, "Missing name")
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    states = storage.all(State).values()
    serialized_states = [state.to_dict() for state in states]
    return jsonify(serialized_states), 200


@app_views.route("/states/<id>", methods=["GET", "DELETE", "PUT"])
def detail_states_view(id):
    """
    retrieving state object based on state_id
    in the database and also allows
    updating, deleting.
    """
    state = storage.get(State, id)
    if not state:
        abort(404)
    if request.method == "DELETE":
        storage.delete(state)
        return jsonify({}), 200
    elif request.method == "PUT":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        data["id"] = state.id
        data["created_at"] = state.created_at
        if "updated_at" in data:
            data.pop("updated_at")
        if storage_t == "db":
            storage.update(state, data)
            updated_state = storage.get(State, state.id)
        else:
            updated_state = State(**data)
            updated_state.save()
        return jsonify(updated_state.to_dict()), 200
    return jsonify(state.to_dict()), 200
