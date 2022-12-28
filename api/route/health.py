from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response
from sqlalchemy import exc

from database.connect import db
from database.user import User
from util import log

health_api = Blueprint("health", __name__)


@health_api.route("/health", methods=["POST"])
def new_account() -> Response:
    """
    health a new user and store in the db
    """
    data = request.get_json()
    if not data:
        log.print_fail(f"Failed to add new user!")
        return make_response(
            jsonify({"status": "error", "message": "failed to add user"}),
            HTTPStatus.BAD_REQUEST.value,
        )

    email = data.get("email", "")
    password = data.get("password", "")
    plus_18 = data.get("plus_18", None)

    log.print_normal(f"POST: health, email {email}, password {password}, 18+ {plus_18}")

    if not email or not password or plus_18 is None:
        log.print_fail(f"Failed to add new user!")
        return make_response(
            jsonify({"status": "error", "message": "failed to add user"}),
            HTTPStatus.BAD_REQUEST.value,
        )

    db_user = User.query.filter_by(email=email).first()

    if db_user is not None:
        log.print_warn(f"User with email {email} already in db")
        return make_response(
            jsonify({"status": "error", "message": "duplicate user"}),
            HTTPStatus.BAD_REQUEST.value,
        )

    user = User(email=email, password=password, used=False, plus_18=plus_18, disabled=False)

    try:
        db.session.add(user)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return make_response(
            jsonify({"status": "error", "message": "failed to update health"}),
            HTTPStatus.BAD_REQUEST.value,
        )

    log.print_ok_arrow(f"Succeeded!")
    return make_response(
        jsonify({"status": "success", "message": "health updated"}), HTTPStatus.OK.value
    )
