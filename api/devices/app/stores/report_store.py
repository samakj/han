from datetime import datetime
from typing import List, Optional, Set, Union

from flagon.exceptions import APIError
from sqlalchemy import text
from sqlalchemy.engine import Engine

from helpers.metric_value_converter import convert_metric_value
from models.report_model import Report
from stores.queries.report_queries import (
    CREATE_REPORT_QUERY,
    DELETE_REPORT_QUERY,
    GET_REPORT_QUERY_TEMPLATE,
    GET_REPORTS_QUERY_TEMPLATE,
    UPDATE_REPORT_QUERY,
    BACKUP_REPORTS,
    LOAD_REPORTS_FROM_BACKUP,
)
from stores.device_store import DeviceStore
from stores.device_type_metric_store import DeviceTypeMetricStore
from stores.metric_store import MetricStore

ALL_FIELDS = {"report_id", "reported_at", "device_id", "metric_id", "value"}
DEFAULT_LIMIT = 1000


class ReportStore:
    def __init__(
        self,
        db: Engine,
        device_store: DeviceStore,
        device_type_metric_store: DeviceTypeMetricStore,
        metric_store: MetricStore,
    ):
        self.db = db
        self.metric_store = metric_store
        self.device_store = device_store
        self.device_type_metric_store = device_type_metric_store

    def create_report(
        self,
        device_id: str,
        metric_id: int,
        value: str,
        reported_at: Optional[datetime] = None,
    ) -> Report:
        device = self.device_store.get_device(device_id=device_id)

        if device is None:
            raise APIError(404, "DEVICE_NOT_FOUND")

        metrics = self.device_type_metric_store.get_device_type_metrics(device_type_id=device.device_type_id)

        if metric_id not in {metric.metric_id for metric in metrics}:
            raise APIError(400, "BAD_REPORT_METRIC")

        db_response = self.db.execute(
            text(CREATE_REPORT_QUERY),
            reported_at=reported_at or datetime.utcnow(),
            device_id=device_id,
            metric_id=metric_id,
            value=value
        ).fetchone()

        return Report(
            report_id=db_response["report_id"],
            reported_at=db_response["reported_at"],
            device_id=db_response["device_id"],
            metric_id=db_response["metric_id"],
            value=db_response["value"],
        )

    def get_report(
        self,
        report_id: int,
        fields: Optional[Set[str]] = None,
        convert_metric: bool = True,
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

        if report and fields and ("metric" in fields or convert_metric):
            metric = self.metric_store.get_metric(metric_id=report.metric_id)
            if "metric" in fields:
                report.metric = metric
            if convert_metric:
                report.value = convert_metric_value(
                    value_type=metric.value_type,
                    value=report.value
                )
        if report and fields and "metric" in fields:
            report.metric = self.metric_store.get_metric(metric_id=report.metric_id)
        if report and fields and "device" in fields:
            report.metric = self.device_store.get_device(device_id=report.device_id)

        return report

    def get_reports(
        self,
        fields: Optional[Set[str]] = None,
        report_id: Optional[Union[Set[int], int]] = None,
        metric_id: Optional[Union[Set[int], int]] = None,
        device_id: Optional[Union[Set[str], str]] = None,
        reported_at_gte: Optional[datetime] = None,
        reported_at_lte: Optional[datetime] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
        limit: Optional[int] = None,
        convert_metric: bool = True,
    ) -> List[Report]:
        where_conditions: Set[str] = set()

        if report_id:
            where_conditions.add(
                f"report_id = "
                f"{'ANY(:report_id)' if isinstance(report_id, set) else ':report_id'}"
            )
        if metric_id:
            where_conditions.add(
                f"metric_id = "
                f"{'ANY(:metric_id)' if isinstance(metric_id, set) else ':metric_id'}"
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
            metric_id=list(metric_id) if isinstance(metric_id, set) else metric_id,
            device_id=list(device_id) if isinstance(device_id, set) else device_id,
            reported_at_gte=reported_at_gte,
            reported_at_lte=reported_at_lte,
        )

        reports = []

        for row in db_response:
            report = Report(**dict(row))
            known_metrics = {}
            known_devices = {}

            if fields and ("metric" in fields or convert_metric):
                if report.metric_id not in known_metrics:
                    known_metrics[report.metric_id] = self.metric_store.get_metric(
                        metric_id=report.metric_id
                    )
                if "metric" in fields:
                    report.metric = known_metrics[report.metric_id]
                if convert_metric:
                    report.value = convert_metric_value(
                        value_type=known_metrics[report.metric_id].value_type,
                        value=report.value
                    )
            if fields and "device" in fields:
                if report.device_id not in known_devices:
                    known_devices[report.device_id] = self.device_store.get_device(
                        device_id=report.device_id
                    )
                report.device = known_devices[report.device_id]
            reports.append(report)

        return reports

    def update_report(
        self,
        report_id: int,
        reported_at: Optional[datetime] = None,
        device_id: Optional[str] = None,
        metric_id: Optional[int] = None,
        value: Optional[str] = None,
    ) -> Optional[Report]:
        set_conditions: Set[str] = set()

        if reported_at:
            set_conditions.add("reported_at = :reported_at")
        if device_id:
            set_conditions.add("device_id = :device_id")
        if metric_id:
            set_conditions.add("metric_id = :metric_id")
        if value:
            set_conditions.add("value = :value")

        if not set_conditions:
            return self.get_report(report_id=report_id)

        db_response = self.db.execute(
            text(UPDATE_REPORT_QUERY.format(set_conditions=", ".join(set_conditions))),
            report_id=report_id,
            reported_at=reported_at,
            device_id=device_id,
            metric_id=metric_id,
            value=value,
        ).fetchone()

        return Report(
            report_id=db_response["report_id"],
            reported_at=db_response["reported_at"],
            device_id=db_response["device_id"],
            metric_id=db_response["metric_id"],
            value=db_response["value"],
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
