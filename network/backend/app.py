import os

from flask_cors import CORS
from han_flask import HanFlask
from han_sqlalchemy import create_database

from routes.v0.user_routes import USER_V0_BLUEPRINT
from stores.user_store import UserStore


def create_app() -> HanFlask:
    app = HanFlask(__name__)

    app.cors = CORS(app)

    app.db = create_database(
        dbname=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        password=os.environ["DB_PASSWORD"],
        port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"],
    )

    app.user_store = UserStore(db=app.db)

    app.register_blueprint(USER_V0_BLUEPRINT, url_prefix="/v0/auth")

    return app


app = create_app()
