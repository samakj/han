from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.device_type_report_metric_model import DeviceTypeReportMetric
from stores.queries.device_type_report_metric_queries import (
    CREATE_DEVICE_TYPE_REPORT_METRIC_QUERY,
    DELETE_DEVICE_TYPE_REPORT_METRIC_QUERY,
    GET_DEVICE_TYPE_REPORT_METRIC_QUERY_TEMPLATE,
    GET_DEVICE_TYPE_REPORT_METRICS_QUERY_TEMPLATE,
    UPDATE_DEVICE_TYPE_REPORT_METRIC_QUERY,
    BACKUP_DEVICE_TYPE_REPORT_METRICS,
    LOAD_DEVICE_TYPE_REPORT_METRICS_FROM_BACKUP,
)

ALL_FIELDS = {"device_type_report_metric_id", "device_type_id", "report_metric_id"}


class DeviceTypeReportMetricStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_device_type_report_metric(self, device_type_id: int, report_metric_id: int) -> DeviceTypeReportMetric:
        db_response = self.db.execute(
            text(CREATE_DEVICE_TYPE_REPORT_METRIC_QUERY),
            device_type_id=device_type_id,
            report_metric_id=report_metric_id,
        ).fetchone()

        return DeviceTypeReportMetric(
            device_type_report_metric_id=db_response["device_type_report_metric_id"],
            device_type_id=db_response["device_type_id"],
            report_metric_id=db_response["report_metric_id"],
        )

    def get_device_type_report_metric(
        self,
        device_type_report_metric_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[DeviceTypeReportMetric]:
        db_response = self.db.execute(
            text(
                GET_DEVICE_TYPE_REPORT_METRIC_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                )
            ),
            device_type_report_metric_id=device_type_report_metric_id,
        ).fetchone()

        return DeviceTypeReportMetric(**dict(db_response)) if db_response else None

    def get_device_type_report_metrics(
        self,
        fields: Optional[Set[str]] = None,
        device_type_report_metric_id: Optional[Union[Set[int], int]] = None,
        device_type_id: Optional[Union[Set[int], int]] = None,
        report_metric_id: Optional[Union[Set[int], int]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[DeviceTypeReportMetric]:
        where_conditions: Set[str] = set()

        if device_type_report_metric_id:
            where_conditions.add(
                f"device_type_report_metric_id = "
                f"{'ANY(:device_type_report_metric_id)' if isinstance(device_type_report_metric_id, set) else ':device_type_report_metric_id'}"
            )
        if device_type_id:
            where_conditions.add(
                f"device_type_id = "
                f"{'ANY(:device_type_id)' if isinstance(device_type_id, set) else ':device_type_id'}"
            )
        if report_metric_id:
            where_conditions.add(
                f"report_metric_id = "
                f"{'ANY(:report_metric_id)' if isinstance(report_metric_id, set) else ':report_metric_id'}"
            )

        db_response = self.db.execute(
            text(
                GET_DEVICE_TYPE_REPORT_METRICS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'device_type_report_metric_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            device_type_report_metric_id=list(device_type_report_metric_id) if isinstance(device_type_report_metric_id, set) else device_type_report_metric_id,
            device_type_id=list(device_type_id) if isinstance(device_type_id, set) else device_type_id,
            report_metric_id=list(report_metric_id) if isinstance(report_metric_id, set) else report_metric_id,
        )

        return [DeviceTypeReportMetric(**dict(row)) for row in db_response]

    def update_device_type_report_metric(
        self,
        device_type_report_metric_id: int,
        device_type_id: Optional[int] = None,
        report_metric_id: Optional[int] = None,
    ) -> Optional[DeviceTypeReportMetric]:
        set_conditions: Set[str] = set()

        if device_type_id:
            set_conditions.add("device_type_id = :device_type_id")
        if report_metric_id:
            set_conditions.add("report_metric_id = :report_metric_id")

        if not set_conditions:
            return self.get_device_type_report_metric(device_type_report_metric_id=device_type_report_metric_id)

        db_response = self.db.execute(
            text(UPDATE_DEVICE_TYPE_REPORT_METRIC_QUERY.format(set_conditions=", ".join(set_conditions))),
            device_type_report_metric_id=device_type_report_metric_id,
            device_type_id=device_type_id,
            report_metric_id=report_metric_id,
        ).fetchone()

        return DeviceTypeReportMetric(
            device_type_report_metric_id=db_response["device_type_report_metric_id"],
            device_type_id=db_response["device_type_id"],
            report_metric_id=db_response["report_metric_id"],
        ) if db_response else None

    def delete_device_type_report_metric(self, device_type_report_metric_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_DEVICE_TYPE_REPORT_METRIC_QUERY),
            device_type_report_metric_id=device_type_report_metric_id,
        ).scalar()

        return db_response

    def backup_device_type_report_metrics(self) -> bool:
        self.db.execute(BACKUP_DEVICE_TYPE_REPORT_METRICS)
        return True

    def load_device_type_report_metrics_from_backup(self) -> bool:
        self.db.execute(LOAD_DEVICE_TYPE_REPORT_METRICS_FROM_BACKUP)
        return True
