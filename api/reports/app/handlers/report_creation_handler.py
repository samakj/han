import os
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

import requests

from models.temperature_report_model import TemperatureReport
from models.humidity_report_model import HumidityReport
from models.motion_report_model import MotionReport
from stores.report_metric_store import ReportMetricStore
from stores.temperature_value_store import TemperatureValueStore
from stores.humidity_value_store import HumidityValueStore
from stores.motion_value_store import MotionValueStore
from stores.report_store import ReportStore


class ReportCreationHandler:
    def __init__(
        self,
        report_store: ReportStore,
        report_metric_store: ReportMetricStore,
        temperature_value_store: TemperatureValueStore,
        humidity_value_store: HumidityValueStore,
        motion_value_store: MotionValueStore,
    ):
        self.report_store = report_store
        self.report_metric_store = report_metric_store
        self.temperature_value_store = temperature_value_store
        self.humidity_value_store = humidity_value_store
        self.motion_value_store = motion_value_store

    def create_report(
        self,
        device_id: str,
        value: Union[bool, Decimal],
        reported_at: datetime,
        report_metric_id: Optional[int] = None,
        report_metric_name: Optional[str] = None,
        report_metric_abbreviation: Optional[str] = None,
    ) -> Optional[Union[TemperatureReport, HumidityReport, MotionReport]]:
        _report_metric_id = report_metric_id
        report_metric = None

        if _report_metric_id is None:
            if report_metric_name is not None:
                report_metric = self.report_metric_store.get_report_metric_by_name(
                    name=report_metric_name
                )
                _report_metric_id = report_metric.report_metric_id
            elif report_metric_abbreviation is not None:
                report_metric = self.report_metric_store.get_report_metric_by_abbreviation(
                    abbreviation=report_metric_abbreviation
                )
                _report_metric_id = report_metric.report_metric_id
            else:
                raise Exception

        last_reports = self.report_store.get_reports(
            fields={
                "report_id",
                "report_metric_id",
                "reported_at",
                "device_id",
                "value",
            },
            device_id=device_id,
            report_metric_id=_report_metric_id,
            order_by="reported_at",
            order_by_direction="DESC",
            limit=1,
        )

        device = requests.get(
            f"{os.environ['DEVICE_API_ENDPOINT']}/v0/devices/{device_id}/",
            params={"fields": ["device_id", "device_type"]}
        ).json()["device"]

        # This is to stop someone injecting unwanted info.
        if (
            _report_metric_id not in
            {report_metric["report_metric_id"] for report_metric in device["device_types"]["report_metrics"]}
        ):
            raise Exception

        # We only want to add a new row when the value changes to save space in the db.
        if last_reports and last_reports[0].value == value:
            return last_reports[0]

        report = self.report_store.create_report(
            report_metric_id=_report_metric_id,
            reported_at=reported_at,
            device_id=device_id,
        )

        if report_metric is None:
            report_metric = self.report_metric_store.get_report_metric(report_metric_id=_report_metric_id)

        report.report_metric = report_metric

        if report.report_metric.name == "temperature":
            value_row = self.temperature_value_store.get_temperature_value_by_report_id(report_id=report.report_id)
            report = TemperatureReport(**asdict(report), value=value_row.value)
        if report.report_metric.name == "humidity":
            value_row = self.humidity_value_store.get_humidity_value_by_report_id(report_id=report.report_id)
            report = HumidityReport(**asdict(report), value=value_row.value)
        if report.report_metric.name == "motion":
            value_row = self.motion_value_store.get_motion_value_by_report_id(report_id=report.report_id)
            report = MotionReport(**asdict(report), value=value_row.value)

        return report
