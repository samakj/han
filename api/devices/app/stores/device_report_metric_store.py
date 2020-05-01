from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.device_report_metric_model import DeviceReportMetric
from stores.queries.device_report_metric_queries import (
    CREATE_DEVICE_REPORT_METRIC_QUERY,
    DELETE_DEVICE_REPORT_METRIC_QUERY,
    GET_DEVICE_REPORT_METRIC_QUERY_TEMPLATE,
    GET_DEVICE_REPORT_METRICS_QUERY_TEMPLATE,
    UPDATE_DEVICE_REPORT_METRIC_QUERY,
    BACKUP_DEVICE_REPORT_METRICS,
    LOAD_DEVICE_REPORT_METRICS_FROM_BACKUP,
)

ALL_FIELDS = {"device_report_metric_id", "device_id", "report_metric_id"}


class DeviceReportMetricStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_device_report_metric(self, device_id: str, report_metric_id: int) -> DeviceReportMetric:
        db_response = self.db.execute(
            text(CREATE_DEVICE_REPORT_METRIC_QUERY),
            device_id=device_id,
            report_metric_id=report_metric_id,
        ).fetchone()

        return DeviceReportMetric(
            device_report_metric_id=db_response["device_report_metric_id"],
            device_id=db_response["device_id"],
            report_metric_id=db_response["report_metric_id"],
        )

    def get_device_report_metric(
        self,
        device_report_metric_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[DeviceReportMetric]:
        db_response = self.db.execute(
            text(
                GET_DEVICE_REPORT_METRIC_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                )
            ),
            device_report_metric_id=device_report_metric_id,
        ).fetchone()

        return DeviceReportMetric(**dict(db_response)) if db_response else None

    def get_device_report_metrics(
        self,
        fields: Optional[Set[str]] = None,
        device_report_metric_id: Optional[Union[Set[int], int]] = None,
        device_id: Optional[Union[Set[str], str]] = None,
        report_metric_id: Optional[Union[Set[int], int]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[DeviceReportMetric]:
        where_conditions: Set[str] = set()

        if device_report_metric_id:
            where_conditions.add(
                f"device_report_metric_id = "
                f"{'ANY(:device_report_metric_id)' if isinstance(device_report_metric_id, set) else ':device_report_metric_id'}"
            )
        if device_id:
            where_conditions.add(
                f"device_id = "
                f"{'ANY(:device_id)' if isinstance(device_id, set) else ':device_id'}"
            )
        if report_metric_id:
            where_conditions.add(
                f"report_metric_id = "
                f"{'ANY(:report_metric_id)' if isinstance(report_metric_id, set) else ':report_metric_id'}"
            )

        db_response = self.db.execute(
            text(
                GET_DEVICE_REPORT_METRICS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'device_report_metric_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            device_report_metric_id=device_report_metric_id,
            device_ids=device_id,
            report_metric_ids=report_metric_id,
        )

        return [DeviceReportMetric(**dict(row)) for row in db_response]

    def update_device_report_metric(
        self,
        device_report_metric_id: int,
        device_id: Optional[str] = None,
        report_metric_id: Optional[int] = None,
    ) -> Optional[DeviceReportMetric]:
        set_conditions: Set[str] = set()

        if device_id:
            set_conditions.add("device_id = :device_id")
        if report_metric_id:
            set_conditions.add("report_metric_id = :report_metric_id")

        if not set_conditions:
            return self.get_device_report_metric(device_report_metric_id=device_report_metric_id)

        db_response = self.db.execute(
            text(UPDATE_DEVICE_REPORT_METRIC_QUERY),
            device_id=device_id,
            report_metric_id=report_metric_id,
        ).fetchone()

        return DeviceReportMetric(
            device_report_metric_id=db_response["device_report_metric_id"],
            device_id=db_response["device_id"],
            report_metric_id=db_response["report_metric_id"],
        ) if db_response else None

    def delete_device_report_metric(self, device_report_metric_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_DEVICE_REPORT_METRIC_QUERY),
            device_report_metric_id=device_report_metric_id,
        ).fetchone()

        return db_response["device_report_metric_id"] if db_response else None

    def backup_device_report_metrics(self) -> bool:
        self.db.execute(BACKUP_DEVICE_REPORT_METRICS)
        return True

    def load_device_report_metrics_from_backup(self) -> bool:
        self.db.execute(LOAD_DEVICE_REPORT_METRICS_FROM_BACKUP)
        return True
