#!/usr/bin/python3
"""
Creating the view for the blueprint application
creating endpoints for users
"""
from flask import request, abort, jsonify
from . import app_views
from models import storage, storage_t
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def list_users_view():
    """
    returns the list of users
    and also accept new user
    """
    if request.method == "POST":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")

        data = request.get_json()
        if not data.get("email"):
            return abort(400, "Missing email")
        if not data.get("password"):
            return abort(400, "Missing password")
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    users = storage.all(User).values()
    serialized_users = [user.to_dict() for user in users]
    return jsonify(serialized_users), 200


@app_views.route("/users/<id>", methods=["GET", "DELETE", "PUT"])
def detail_users_view(id):
    """
    retrieving user object based on user_id
    in the database and also allows
    updating, deleting.
    """
    user = storage.get(User, id)
    if not user:
        abort(404)
    if request.method == "DELETE":
        storage.delete(user)
        return jsonify({}), 200
    elif request.method == "PUT":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        data["id"] = user.id
        data["created_at"] = user.created_at
        if "updated_at" in data:
            data.pop("updated_at")
        if "email" in data:
            data.pop("email")
        if storage_t == "db":
            storage.update(user, data)
            updated_user = storage.get(User, user.id)
        else:
            updated_user = User(**data)
            updated_user.save()
        return jsonify(updated_user.to_dict()), 200
    return jsonify(user.to_dict()), 200
