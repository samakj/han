from datetime import datetime
from dataclasses import asdict
from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.report_model import Report
from models.temperature_report_model import TemperatureReport
from models.humidity_report_model import HumidityReport
from models.motion_report_model import MotionReport
from stores.metric_store import ReportMetricStore
from stores.temperature_value_store import TemperatureValueStore
from stores.humidity_value_store import HumidityValueStore
from stores.motion_value_store import MotionValueStore
from stores.queries.report_queries import (
    CREATE_REPORT_QUERY,
    DELETE_REPORT_QUERY,
    GET_REPORT_QUERY_TEMPLATE,
    GET_REPORTS_QUERY_TEMPLATE,
    UPDATE_REPORT_QUERY,
    BACKUP_REPORTS,
    LOAD_REPORTS_FROM_BACKUP,
)

ALL_FIELDS = {"report_id", "report_metric_id", "reported_at", "device_id"}
DEFAULT_LIMIT = 1000


class ReportStore:
    def __init__(
        self,
        db: Engine,
        report_metric_store: ReportMetricStore,
        temperature_value_store: TemperatureValueStore,
        humidity_value_store: HumidityValueStore,
        motion_value_store: MotionValueStore,
    ):
        self.db = db
        self.report_metric_store = report_metric_store
        self.temperature_value_store = temperature_value_store
        self.humidity_value_store = humidity_value_store
        self.motion_value_store = motion_value_store

    def create_report(
        self,
        report_metric_id: int,
        reported_at: datetime,
        device_id: str,
    ) -> Report:
        db_response = self.db.execute(
            text(CREATE_REPORT_QUERY),
            report_metric_id=report_metric_id,
            reported_at=reported_at,
            device_id=device_id,
        ).fetchone()

        return Report(
            report_id=db_response["report_id"],
            report_metric_id=db_response["report_metric_id"],
            reported_at=db_response["reported_at"],
            device_id=db_response["device_id"],
        )

    def get_report(
        self,
        report_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[Report]:
        db_response = self.db.execute(
            text(
                GET_REPORT_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            report_id=report_id,
        ).fetchone()

        report = Report(**dict(db_response)) if db_response else None

        if report and fields and "report_metric" in fields:
            report.report_metric = self.report_metric_store.get_report_metric(report_metric_id=report.report_metric_id)
        if report and fields and "value" in fields:
            if report.report_metric.name == "temperature":
                value_row = self.temperature_value_store.get_temperature_value_by_report_id(report_id=report_id)
                report = TemperatureReport(**asdict(report), value=value_row.value)
            if report.report_metric.name == "humidity":
                value_row = self.humidity_value_store.get_humidity_value_by_report_id(report_id=report_id)
                report = HumidityReport(**asdict(report), value=value_row.value)
            if report.report_metric.name == "motion":
                value_row = self.motion_value_store.get_motion_value_by_report_id(report_id=report_id)
                report = MotionReport(**asdict(report), value=value_row.value)

        return report

    def get_reports(
        self,
        fields: Optional[Set[str]] = None,
        report_id: Optional[Union[Set[int], int]] = None,
        report_metric_id: Optional[Union[Set[int], int]] = None,
        device_id: Optional[Union[Set[str], str]] = None,
        reported_at_gte: Optional[datetime] = None,
        reported_at_lte: Optional[datetime] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Report]:
        where_conditions: Set[str] = set()

        if report_id:
            where_conditions.add(
                f"report_id = "
                f"{'ANY(:report_id)' if isinstance(report_id, set) else ':report_id'}"
            )
        if report_metric_id:
            where_conditions.add(
                f"report_metric_id = "
                f"{'ANY(:report_metric_id)' if isinstance(report_metric_id, set) else ':report_metric_id'}"
            )
        if device_id:
            where_conditions.add(
                f"abbreviation = "
                f"{'ANY(:device_id)' if isinstance(device_id, set) else ':device_id'}"
            )
        if reported_at_gte:
            where_conditions.add("reported_at >= :reported_at_gte")
        if reported_at_lte:
            where_conditions.add("reported_at <= :reported_at_gte")

        db_response = self.db.execute(
            text(
                GET_REPORTS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'reported_at'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    ),
                    limit=limit or DEFAULT_LIMIT
                ),
            ),
            report_id=list(report_id) if isinstance(report_id, set) else report_id,
            report_metric_id=list(report_metric_id) if isinstance(report_metric_id, set) else report_metric_id,
            device_id=list(device_id) if isinstance(device_id, set) else device_id,
            reported_at_gte=reported_at_gte,
            reported_at_lte=reported_at_lte,
        )

        reports = []

        for row in db_response:
            report = Report(**dict(row))
            if fields and "report_metric" in fields:
                report.report_metric = self.report_metric_store.get_report_metric(
                    report_metric_id=report.report_metric_id
                )
            if fields and "value" in fields:
                if report.report_metric.name == "temperature":
                    value_row = self.temperature_value_store.get_temperature_value_by_report_id(report_id=report_id)
                    report = TemperatureReport(**asdict(report), value=value_row.value)
                if report.report_metric.name == "humidity":
                    value_row = self.humidity_value_store.get_humidity_value_by_report_id(report_id=report_id)
                    report = HumidityReport(**asdict(report), value=value_row.value)
                if report.report_metric.name == "motion":
                    value_row = self.motion_value_store.get_motion_value_by_report_id(report_id=report_id)
                    report = MotionReport(**asdict(report), value=value_row.value)
            reports.append(report)

        return reports

    def update_report(
        self,
        report_id: int,
        report_metric_id: Optional[int] = None,
        reported_at: Optional[datetime] = None,
        device_id: Optional[str] = None,
    ) -> Optional[Report]:
        set_conditions: Set[str] = set()

        if report_metric_id:
            set_conditions.add("report_metric_id = :report_metric_id")
        if reported_at:
            set_conditions.add("reported_at = :reported_at")
        if device_id:
            set_conditions.add("device_id = :device_id")

        if not set_conditions:
            return self.get_report(report_id=report_id)

        db_response = self.db.execute(
            text(UPDATE_REPORT_QUERY.format(set_conditions=", ".join(set_conditions))),
            report_id=report_id,
            report_metric_id=report_metric_id,
            reported_at=reported_at,
            device_id=device_id,
        ).fetchone()

        return Report(
            report_id=db_response["report_id"],
            report_metric_id=db_response["report_metric_id"],
            reported_at=db_response["reported_at"],
            device_id=db_response["device_id"],
        ) if db_response else None

    def delete_report(self, report_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_REPORT_QUERY),
            report_id=report_id,
        ).scalar()

        return db_response

    def backup_reports(self) -> bool:
        self.db.execute(BACKUP_REPORTS)
        return True

    def load_reports_from_backup(self) -> bool:
        self.db.execute(LOAD_REPORTS_FROM_BACKUP)
        return True
