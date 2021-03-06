import os

from flask_cors import CORS
from flagon import Flagon
from han_sqlalchemy import create_database

from routes.v0.device_location_tag_routes import DEVICE_LOCATION_TAGS_V0_BLUEPRINT
from routes.v0.device_type_metric_routes import DEVICE_TYPE_METRICS_V0_BLUEPRINT
from routes.v0.device_type_routes import DEVICE_TYPES_V0_BLUEPRINT
from routes.v0.device_routes import DEVICES_V0_BLUEPRINT
from routes.v0.location_tag_routes import LOCATION_TAGS_V0_BLUEPRINT
from routes.v0.metric_routes import METRICS_V0_BLUEPRINT
from routes.v0.report_routes import REPORTS_V0_BLUEPRINT
from stores.device_store import DeviceStore
from stores.device_location_tag_store import DeviceLocationTagStore
from stores.device_type_metric_store import DeviceTypeMetricStore
from stores.device_type_store import DeviceTypeStore
from stores.location_tag_store import LocationTagStore
from stores.metric_store import MetricStore
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

    app.device_location_tag_store = DeviceLocationTagStore(db=app.db)
    app.device_type_metric_store = DeviceTypeMetricStore(db=app.db)
    app.location_tag_store = LocationTagStore(db=app.db)
    app.metric_store = MetricStore(db=app.db)
    app.device_type_store = DeviceTypeStore(
        db=app.db,
        device_type_metric_store=app.device_type_metric_store,
        metric_store=app.metric_store
    )
    app.device_store = DeviceStore(
        db=app.db,
        device_location_tag_store=app.device_location_tag_store,
        location_tag_store=app.location_tag_store,
        device_type_store=app.device_type_store,
    )
    app.report_store= ReportStore(
        db=app.db,
        device_store=app.device_store,
        device_type_metric_store=app.device_type_metric_store,
        metric_store=app.metric_store,
    )

    app.register_blueprint(DEVICE_LOCATION_TAGS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(DEVICE_TYPE_METRICS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(DEVICE_TYPES_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(DEVICES_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(LOCATION_TAGS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(METRICS_V0_BLUEPRINT, url_prefix="/v0")
    app.register_blueprint(REPORTS_V0_BLUEPRINT, url_prefix="/v0")

    return app


app = create_app()
