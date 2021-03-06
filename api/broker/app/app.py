import os

from flask_cors import CORS
from flagon import Flagon
from han_sqlalchemy import create_database

from routes.v0.user_routes import USERS_V0_BLUEPRINT
from routes.v0.superuser_routes import SUPERUSERS_V0_BLUEPRINT
from routes.v0.access_control_routes import ACCESS_CONTROLS_V0_BLUEPRINT
from stores.user_store import UserStore
from stores.superuser_store import SuperuserStore
from stores.access_control_store import AccessControlStore


def create_app() -> Flagon:
    app = Flagon(__name__)

    app.cors = CORS(app)

    app.db = create_database(
        dbname=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        password=os.environ["DB_PASSWORD"],
        port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"],
    )

    app.user_store = UserStore(db=app.db)
    app.superuser_store = SuperuserStore(db=app.db)
    app.access_control_store = AccessControlStore(db=app.db)

    app.register_blueprint(USERS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(SUPERUSERS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(ACCESS_CONTROLS_V0_BLUEPRINT, url_prefix="/v0")

    return app


app = create_app()
