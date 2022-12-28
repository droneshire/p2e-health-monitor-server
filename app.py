import argparse
import os

from flask import Flask

from api.route import health, home
from database.connect import db
from utils import log
from utils.file_util import make_sure_path_exists


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    log_dir = log.get_logging_dir("server")
    make_sure_path_exists(log_dir)
    parser.add_argument("--log-level", choices=["INFO", "DEBUG", "ERROR", "NONE"], default="INFO")
    parser.add_argument("--log-dir", default=log_dir)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--hostname", default="0.0.0.0")
    return parser.parse_args()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    app.register_blueprint(health.health_api, url_prefix="/api")
    app.register_blueprint(home.home_api, url_prefix="/api")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    args = parse_args()
    log.setup_log(args.log_level, args.log_dir, str(os.getpid()))

    port = args.port
    host = args.hostname

    log.print_bold(f"Starting flask app. Port: {port}, Host: {host}")
    status_app = create_app()

    status_app.run(host=host, port=port, debug=False)
