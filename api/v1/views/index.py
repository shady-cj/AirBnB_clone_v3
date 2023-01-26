#!/usr/bin/python3
"""
Creating the view for the blueprint application
"""
from . import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def index():
    """
    return status
    """
    return {"status": "OK"}


@app_views.route("/stats")
def count():
    """
    returning the number of data
    in the database
    """
    return {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
