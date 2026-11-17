"""PEÇONHA+ · aplicação Flask."""
from flask import Flask

from app import db


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(DATABASE=str(db.DEFAULT_DB_PATH), JSON_AS_ASCII=False)
    app.json.ensure_ascii = False
    if config:
        app.config.update(config)

    app.teardown_appcontext(db.close_db)

    from app.api import api
    from app.pages import pages

    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(pages)
    return app
