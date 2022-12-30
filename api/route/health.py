import datetime
import json
from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from flask.wrappers import Response

from database.connect import ManagedSession
from database.health import Health, HealthSchema
from database.user import User
from utils import log

health_api = Blueprint("health", __name__)


@health_api.route("/health", methods=["GET"])
def health_all() -> Response:
    log.print_normal(f"GET: health")

    bots = Health.query.all()

    log.print_ok_arrow("Succeeded!")
    data = {"result": [HealthSchema().dump(bot) for bot in bots]}
    log.print_normal(f"All bots status: {json.dumps(data, indent=4)}")
    return make_response(jsonify(data), HTTPStatus.OK.value)


@health_api.route("/health/<botname>", methods=["GET", "POST"])
def health(botname) -> Response:
    """
    Get or update the status of a bot
    """
    bot = Health.query.filter_by(name=botname).first()

    if request.method == "POST":
        log.print_normal(f"POST: health/{botname}")

        data = request.get_json()
        if not data:
            log.print_fail("Missing data for bot")
            return make_response(
                jsonify({"status": "error", "message": "missing data from bot status"}),
                HTTPStatus.BAD_REQUEST.value,
            )

        missing_fields = [i for i in data.keys() if i not in ["name", "num_users", "users"]]
        if any(missing_fields):
            log.print_fail("Missing fields for bot")
            return make_response(
                jsonify({"status": "error", "message": f"missing data fields {missing_fields}"}),
                HTTPStatus.PARTIAL_CONTENT.value,
            )

        if botname != data["name"]:
            log.print_warn(f"User specified name {data['name']} doesn't match endpoint {botname}")

        if bot is None:
            bot = Health(name=botname, num_users=data["num_users"])
        else:
            bot.num_users = data["num_users"]

        bot.last_ping = datetime.datetime.now()

        with ManagedSession() as session:
            session.add(bot)  # pylint: disable=no-member

        for user in data["users"]:
            missing_fields = [i for i in user.keys() if i not in ["username", "wallets"]]
            if any(missing_fields):
                log.print_fail("Missing fields for users")
                return make_response(
                    jsonify(
                        {
                            "status": "error",
                            "message": f"missing user info fields {missing_fields}",
                        }
                    ),
                    HTTPStatus.PARTIAL_CONTENT.value,
                )
            botter = (
                User.query.filter_by(health_id=bot.id).filter_by(username=user["username"]).first()
            )
            if botter is None:
                botter = User(username=user["username"], health_id=bot.id)
            botter.wallets = user["wallets"]

            with ManagedSession() as session:
                session.add(botter)  # pylint: disable=no-member

        log.print_normal(f"Updated bot status: {json.dumps(data, indent=4)}")

        log.print_ok_arrow("Succeeded!")

        return make_response(jsonify(HealthSchema().dump(bot)), HTTPStatus.OK.value)

    if request.method == "GET":
        log.print_normal(f"GET: health/{botname}")

        if bot is None:
            log.print_fail_arrow("Failed!")
            return make_response(
                jsonify({"status": "error", "message": f"No status for {botname}"}),
                HTTPStatus.NOT_FOUND.value,
            )

        log.print_ok_arrow("Succeeded!")
        return make_response(jsonify(HealthSchema().dump(bot)), HTTPStatus.OK.value)

    return make_response(
        jsonify({"status": "error", "message": "unsupported request type"}),
        HTTPStatus.BAD_REQUEST.value,
    )
