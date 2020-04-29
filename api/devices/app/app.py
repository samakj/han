import os

from flask_cors import CORS
from han_flask import HanFlask
from han_sqlalchemy import create_database


def create_app() -> HanFlask:
    app = HanFlask(__name__)

    app.config['SECRET_KEY'] = 'notsosecret'

    app.cors = CORS(app)

    app.db = create_database(
        dbname=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        password=os.environ["DB_PASSWORD"],
        port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"],
    )

    return app


app = create_app()
