from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.device_model import Device
from models.location_tag_model import LocationTag
from models.report_metric_model import ReportMetric
from stores.device_location_tag_store import DeviceLocationTagStore
from stores.device_report_metric_store import DeviceReportMetricStore
from stores.location_tag_store import LocationTagStore
from stores.report_metric_store import ReportMetricStore
from stores.queries.device_queries import (
    CREATE_DEVICE_QUERY,
    DELETE_DEVICE_QUERY,
    GET_DEVICE_QUERY_TEMPLATE,
    GET_DEVICES_QUERY_TEMPLATE,
    UPDATE_DEVICE_QUERY,
    BACKUP_DEVICES,
    LOAD_DEVICES_FROM_BACKUP,
)

ALL_FIELDS = {"device_id"}


class DeviceStore:
    def __init__(
        self,
        db: Engine,
        device_location_tag_store: DeviceLocationTagStore,
        device_report_metric_store: DeviceReportMetricStore,
        location_tag_store: LocationTagStore,
        report_metric_store: ReportMetricStore,
    ):
        self.db = db
        self.device_location_tag_store = device_location_tag_store
        self.device_report_metric_store = device_report_metric_store
        self.location_tag_store = location_tag_store
        self.report_metric_store = report_metric_store

    def create_device(
        self,
        device_id: str,
        location_tag_ids: Optional[Set[int]] = None,
        report_metric_ids: Optional[Set[int]] = None,
    ) -> Device:
        db_response = self.db.execute(
            text(CREATE_DEVICE_QUERY),
            device_id=device_id,
        ).fetchone()

        fields = ALL_FIELDS

        if location_tag_ids:
            fields.add("location_tags")
            for location_tag_id in location_tag_ids:
                self.device_location_tag_store.create_device_location_tag(
                    device_id=db_response["device_id"],
                    location_tag_id=location_tag_id,
                )
        if report_metric_ids:
            fields.add("report_metrics")
            for report_metric_id in report_metric_ids:
                self.device_report_metric_store.create_device_report_metric(
                    device_id=db_response["device_id"],
                    report_metric_id=report_metric_id,
                )

        return self.get_device(device_id=db_response["device_id"], fields=fields)

    def get_device(
        self,
        device_id: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[Device]:
        db_response = self.db.execute(
            text(
                GET_DEVICE_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                )
            ),
            device_id=device_id,
        ).fetchone()

        device = Device(**dict(db_response)) if db_response else None

        if fields and "location_tags" in fields:
            device.location_tags = self.get_device_location_tags(device_id=device_id)
        if fields and "report_metrics" in fields:
            device.report_metrics = self.get_device_report_metrics(device_id=device_id)

        return device

    def get_devices(
        self,
        fields: Optional[Set[str]] = None,
        device_id: Optional[Union[Set[str], str]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[Device]:
        where_conditions: Set[str] = set()

        if device_id:
            where_conditions.add(
                f"device_id = "
                f"{'ANY(:device_id)' if isinstance(device_id, list) else ':device_id'}"
            )

        db_response = self.db.execute(
            text(
                GET_DEVICES_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'device_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            device_id=device_id,
        )

        devices = []

        for row in db_response:
            device = Device(**dict(row))
            if fields and "location_tags" in fields:
                device.location_tags = self.get_device_location_tags(device_id=device_id)
            if fields and "report_metrics" in fields:
                device.report_metrics = self.get_device_report_metrics(device_id=device_id)
            devices.append(device)

        return devices

    def get_device_location_tags(self, device_id: str) -> List[LocationTag]:
        device_location_tags = self.device_location_tag_store.get_device_location_tags(device_id=device_id)

        return self.location_tag_store.get_location_tags(
            location_tag_id={device_location_tag.location_tag_id for device_location_tag in device_location_tags}
        )

    def get_device_report_metrics(self, device_id: str) -> List[ReportMetric]:
        device_report_metrics = self.device_report_metric_store.get_device_report_metrics(device_id=device_id)

        return self.report_metric_store.get_report_metrics(
            report_metric_id={device_report_metric.report_metric_id for device_report_metric in device_report_metrics}
        )

    def update_device(
        self,
        device_id: str,
    ) -> Optional[Device]:
        set_conditions: Set[str] = set()

        if not set_conditions:
            return self.get_device(device_id=device_id)

        db_response = self.db.execute(
            text(UPDATE_DEVICE_QUERY.format(set_conditions=", ".join(set_conditions))),
            device_id=device_id,
        ).fetchone()

        return Device(
            device_id=db_response["device_id"],
        ) if db_response else None

    def delete_device(self, device_id: str) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_DEVICE_QUERY),
            device_id=device_id,
        ).scalar()

        return db_response

    def backup_devices(self) -> bool:
        self.db.execute(BACKUP_DEVICES)
        return True

    def load_devices_from_backup(self) -> bool:
        self.db.execute(LOAD_DEVICES_FROM_BACKUP)
        return True
