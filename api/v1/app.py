#!/usr/bin/python3
"""
Creating an app from flask
"""
from flask import Flask
from models import storage
import os
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__.split(".")[0])
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def handle_404(e):
    """
    404 error handleer
    """
    return {
            "error": "Not found"
            }, 404


@app.teardown_appcontext
def teardown_context(exception):
    """
    Teardown context to close the session in case of db_storage
    and reload in case of file storage
    """
    storage.close()


if __name__ == "__main__":
    api_host = os.getenv("HBNB_API_HOST") or "0.0.0.0"
    api_port = os.getenv("HBNB_API_PORT") or "5000"
    app.run(host=api_host, port=api_port, threaded=True)
