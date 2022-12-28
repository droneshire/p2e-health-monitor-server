from http import HTTPStatus

from flask import Blueprint, jsonify, make_response
from flask.wrappers import Response

home_api = Blueprint("api", __name__)


@home_api.route("/")
def index() -> Response:
    return make_response(jsonify({"message": "Welcome to P2E server"}), HTTPStatus.OK.value)
