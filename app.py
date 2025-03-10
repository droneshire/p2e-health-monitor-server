import argparse
import os
import threading

from flask import Flask

from api.route import health, home
from database.connect import db
from status_publisher import Publisher
from utils import log
from utils.file_util import make_sure_path_exists

DISCORD_WEBHOOK = {
    "TEST": "https://discordapp.com/api/webhooks/1058264841481097247/N6xn9gt48MzKCMokMzA-OhUVrfMuIfizGnADC0G4Zljd1syy8f15vlRB7e8_FVXl-v72",
    "HEALTH_MONITOR": "https://discordapp.com/api/webhooks/1058252579500457984/mzF0xp5YAJsINCkLqes1QmCFpUNGBt1KQ99b70DWIJyURsFkWjaOSWO7Ezx7aB1oxPgS",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    log_dir = log.get_logging_dir("server")
    make_sure_path_exists(log_dir)
    parser.add_argument("--log-level", choices=["INFO", "DEBUG", "ERROR", "NONE"], default="INFO")
    parser.add_argument("--log-dir", default=log_dir)
    parser.add_argument("--quiet", action="store_true", help="Disable alerts")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--hostname", default="0.0.0.0")
    parser.add_argument(
        "--webhook", choices=list(DISCORD_WEBHOOK.keys()), default="HEALTH_MONITOR", help="Webhooks"
    )
    return parser.parse_args()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    app.register_blueprint(health.health_api, url_prefix="/monitor")
    app.register_blueprint(home.home_api, url_prefix="/monitor")

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

    server_url = f"http://{host}:{port}/monitor"
    log.print_ok_blue_arrow(server_url)
    publisher = Publisher(server_url, DISCORD_WEBHOOK[args.webhook], args.quiet)

    publish_thread = threading.Thread(target=publisher.run, daemon=True)
    publish_thread.start()

    status_app.run(host=host, port=port, debug=False)
