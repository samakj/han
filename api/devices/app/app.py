import os

from flask_cors import CORS
from han_flask import HanFlask
from han_sqlalchemy import create_database

from stores.device_store import DeviceStore
from stores.device_location_tag_store import DeviceLocationTagStore
from stores.device_report_metric_store import DeviceReportMetricStore
from stores.location_tag_store import LocationTagStore
from stores.report_metric_store import ReportMetricStore


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

    app.device_location_tag_store = DeviceLocationTagStore(db=app.db)
    app.device_report_metric_store = DeviceReportMetricStore(db=app.db)
    app.location_tag_store = LocationTagStore(db=app.db)
    app.report_metric_store = ReportMetricStore(db=app.db)
    app.device_store = DeviceStore(
        db=app.db,
        device_location_tag_store=app.device_location_tag_store,
        device_report_metric_store=app.device_report_metric_store,
        location_tag_store=app.location_tag_store,
        report_metric_store=app.report_metric_store,
    )

    return app


app = create_app()
