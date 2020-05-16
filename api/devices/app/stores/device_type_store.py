from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.device_type_model import DeviceType
from models.report_metric_model import ReportMetric
from stores.report_metric_store import ReportMetricStore
from stores.device_type_report_metric_store import DeviceTypeReportMetricStore
from stores.queries.device_type_queries import (
    CREATE_DEVICE_TYPE_QUERY,
    DELETE_DEVICE_TYPE_QUERY,
    GET_DEVICE_TYPE_QUERY_TEMPLATE,
    GET_DEVICE_TYPE_BY_NAME_QUERY_TEMPLATE,
    GET_DEVICE_TYPES_QUERY_TEMPLATE,
    UPDATE_DEVICE_TYPE_QUERY,
    BACKUP_DEVICE_TYPES,
    LOAD_DEVICE_TYPES_FROM_BACKUP,
)

ALL_FIELDS = {"device_type_id", "name"}


class DeviceTypeStore:
    def __init__(self, db: Engine, report_metric_store: ReportMetricStore, device_type_report_metric_store: DeviceTypeReportMetricStore):
        self.db = db
        self.device_type_report_metric_store = device_type_report_metric_store
        self.report_metric_store = report_metric_store

    def create_device_type(self, name: str) -> DeviceType:
        db_response = self.db.execute(
            text(CREATE_DEVICE_TYPE_QUERY),
            name=name,
        ).fetchone()

        return DeviceType(
            device_type_id=db_response["device_type_id"],
            name=db_response["name"],
        )

    def get_device_type(
        self,
        device_type_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[DeviceType]:
        db_response = self.db.execute(
            text(
                GET_DEVICE_TYPE_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            device_type_id=device_type_id,
        ).fetchone()

        device_type = DeviceType(**dict(db_response)) if db_response else None

        if device_type and fields and "report_metrics" in fields:
            device_type.report_metrics = self.get_device_type_report_metrics(device_type_id=device_type.device_type_id)

        return device_type

    def get_device_type_by_name(
        self,
        name: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[DeviceType]:
        db_response = self.db.execute(
            text(
                GET_DEVICE_TYPE_BY_NAME_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            name=name,
        ).fetchone()

        device_type = DeviceType(**dict(db_response)) if db_response else None

        if device_type and fields and "report_metrics" in fields:
            device_type.report_metrics = self.get_device_type_report_metrics(device_type_id=device_type.device_type_id)

        return device_type

    def get_device_types(
        self,
        fields: Optional[Set[str]] = None,
        device_type_id: Optional[Union[Set[int], int]] = None,
        name: Optional[Union[Set[str], str]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[DeviceType]:
        where_conditions: Set[str] = set()

        if device_type_id:
            where_conditions.add(
                f"device_type_id = "
                f"{'ANY(:device_type_id)' if isinstance(device_type_id, set) else ':device_type_id'}"
            )
        if name:
            where_conditions.add(
                f"name = "
                f"{'ANY(:name)' if isinstance(name, set) else ':name'}"
            )

        db_response = self.db.execute(
            text(
                GET_DEVICE_TYPES_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'device_type_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            device_type_id=list(device_type_id) if isinstance(device_type_id, set) else device_type_id,
            device_id=list(name) if isinstance(name, set) else name,
        )

        device_types = []

        for row in db_response:
            device_type = DeviceType(**dict(row))
            if fields and "location_tags" in fields:
                device_type.location_tags = self.get_device_type_report_metrics(device_type_id=device_type.device_type_id)
            device_types.append(device_type)

        return device_types

    def get_device_type_report_metrics(self, device_type_id: int) -> List[ReportMetric]:
        device_type_report_metrics = self.device_type_report_metric_store.get_device_type_report_metrics(device_type_id=device_type_id)

        return self.report_metric_store.get_report_metrics(
            report_metric_id={device_type_report_metric.device_type_report_metric_id for device_type_report_metric in device_type_report_metrics}
        )

    def update_device_type(
        self,
        device_type_id: int,
        name: Optional[str] = None,
    ) -> Optional[DeviceType]:
        set_conditions: Set[str] = set()

        if name:
            set_conditions.add("name = :name")

        if not set_conditions:
            return self.get_device_type(device_type_id=device_type_id)

        db_response = self.db.execute(
            text(UPDATE_DEVICE_TYPE_QUERY.format(set_conditions=", ".join(set_conditions))),
            device_type_id=device_type_id,
            name=name,
        ).fetchone()

        return DeviceType(
            device_type_id=db_response["device_type_id"],
            name=db_response["name"],
        ) if db_response else None

    def delete_device_type(self, device_type_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_DEVICE_TYPE_QUERY),
            device_type_id=device_type_id,
        ).scalar()

        return db_response

    def backup_device_types(self) -> bool:
        self.db.execute(BACKUP_DEVICE_TYPES)
        return True

    def load_device_types_from_backup(self) -> bool:
        self.db.execute(LOAD_DEVICE_TYPES_FROM_BACKUP)
        return True
