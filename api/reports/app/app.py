import os

from flask_cors import CORS
from han_flask import HanFlask
from han_sqlalchemy import create_database

from stores.report_metric_store import ReportMetricStore
from stores.temperature_value_store import TemperatureValueStore
from stores.humidity_value_store import HumidityValueStore
from stores.motion_value_store import MotionValueStore
from stores.report_store import ReportStore


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

    app.report_metric_store = ReportMetricStore(db=app.db)
    app.temperature_value_store = TemperatureValueStore(db=app.db)
    app.humidity_value_store = HumidityValueStore(db=app.db)
    app.motion_value_store = MotionValueStore(db=app.db)
    app.report_store = ReportStore(
        db=app.db,
        report_metric_store=app.report_metric_store,
        temperature_value_store=app.temperature_value_store,
        humidity_value_store=app.humidity_value_store,
        motion_value_store=app.motion_value_store,
    )

    return app


app = create_app()
