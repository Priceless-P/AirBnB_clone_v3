#!/usr/bin/python3
"""
Contains main entrance
"""

from flask import Flask
from flask import jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
from flask import make_response
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origin": '0.0.0.0'}})


with app.app_context():
    app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handles Not found error"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(exception):
    """Handles teardown"""
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True, debug=True)
