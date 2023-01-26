#!/usr/bin/python3
"""
Creating the view for the blueprint application
This module defines all the endpoint for
the review model
"""
from flask import request, abort, jsonify
from . import app_views
from models import storage, storage_t
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def list_reviews_view(place_id):
    """
    returns the list of reviews in a place
    and also accept new reviews associated to a place
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
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    reviews = place.reviews
    serialized_reviews = [review.to_dict() for review in reviews]
    return jsonify(serialized_reviews), 200


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def detail_reviews_view(review_id):
    """
    returning the detail of review based on review_id
    in the database and also allows
    updating, deleting.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == "DELETE":
        storage.delete(review)
        return jsonify({}), 200
    elif request.method == "PUT":
        if request.environ.get("CONTENT_TYPE") != "application/json":
            abort(400, "Not a JSON")
        data = request.get_json()
        data["id"] = review.id
        data["created_at"] = review.created_at
        if "updated_at" in data:
            data.pop("updated_at")
        if "place_id" in data:
            data.pop("place_id")
        if "user_id" in data:
            data.pop("user_id")
        if storage_t == "db":
            storage.update(review, data)
            updated_review = storage.get(Review, review.id)
        else:
            updated_review = Review(**data)
            updated_review.save()
        return jsonify(updated_review.to_dict()), 200
    return jsonify(review.to_dict()), 200
