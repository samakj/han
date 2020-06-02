import os

from flask_cors import CORS
from flagon import Flagon
from han_sqlalchemy import create_database

from handlers.report_creation_handler import ReportCreationHandler
from routes.v0.humidity_value_routes import HUMIDITY_VALUES_V0_BLUEPRINT
from routes.v0.motion_value_routes import MOTION_VALUES_V0_BLUEPRINT
from routes.v0.metric_routes import REPORT_METRICS_V0_BLUEPRINT
from routes.v0.report_routes import REPORTS_V0_BLUEPRINT
from routes.v0.temperature_value_routes import TEMPERATURE_VALUES_V0_BLUEPRINT
from stores.metric_store import ReportMetricStore
from stores.temperature_value_store import TemperatureValueStore
from stores.humidity_value_store import HumidityValueStore
from stores.motion_value_store import MotionValueStore
from stores.report_store import ReportStore


def create_app() -> Flagon:
    app = Flagon(__name__)

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

    app.report_creation_handler = ReportCreationHandler(
        report_metric_store=app.report_metric_store,
        temperature_value_store=app.temperature_value_store,
        humidity_value_store=app.humidity_value_store,
        motion_value_store=app.motion_value_store,
        report_store=app.report_store,
    )

    app.register_blueprint(HUMIDITY_VALUES_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(MOTION_VALUES_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(REPORT_METRICS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(REPORTS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(TEMPERATURE_VALUES_V0_BLUEPRINT, url_prefix="/v0")

    return app


app = create_app()
