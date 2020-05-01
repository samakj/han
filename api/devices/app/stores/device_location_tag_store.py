from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.device_location_tag_model import DeviceLocationTag
from stores.queries.device_location_tag_queries import (
    CREATE_DEVICE_LOCATION_TAG_QUERY,
    DELETE_DEVICE_LOCATION_TAG_QUERY,
    GET_DEVICE_LOCATION_TAG_QUERY_TEMPLATE,
    GET_DEVICE_LOCATION_TAGS_QUERY_TEMPLATE,
    UPDATE_DEVICE_LOCATION_TAG_QUERY,
    BACKUP_DEVICE_LOCATION_TAGS,
    LOAD_DEVICE_LOCATION_TAGS_FROM_BACKUP,
)

ALL_FIELDS = {"device_location_tag_id", "device_id", "location_tag_id"}


class DeviceLocationTagStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_device_location_tag(self, device_id: str, location_tag_id: int) -> DeviceLocationTag:
        db_response = self.db.execute(
            text(CREATE_DEVICE_LOCATION_TAG_QUERY),
            device_id=device_id,
            location_tag_id=location_tag_id,
        ).fetchone()

        return DeviceLocationTag(
            device_location_tag_id=db_response["device_location_tag_id"],
            device_id=db_response["device_id"],
            location_tag_id=db_response["location_tag_id"],
        )

    def get_device_location_tag(
        self,
        device_location_tag_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[DeviceLocationTag]:
        db_response = self.db.execute(
            text(
                GET_DEVICE_LOCATION_TAG_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            device_location_tag_id=device_location_tag_id,
        ).fetchone()

        return DeviceLocationTag(**dict(db_response)) if db_response else None

    def get_device_location_tags(
        self,
        fields: Optional[Set[str]] = None,
        device_location_tag_id: Optional[Union[Set[int], int]] = None,
        device_id: Optional[Union[Set[str], str]] = None,
        location_tag_id: Optional[Union[Set[int], int]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[DeviceLocationTag]:
        where_conditions: Set[str] = set()

        if device_location_tag_id:
            where_conditions.add(
                f"device_location_tag_id = "
                f"{'ANY(:device_location_tag_id)' if isinstance(device_location_tag_id, set) else ':device_location_tag_id'}"
            )
        if device_id:
            where_conditions.add(
                f"device_id = "
                f"{'ANY(:device_id)' if isinstance(device_id, set) else ':device_id'}"
            )
        if location_tag_id:
            where_conditions.add(
                f"location_tag_id = "
                f"{'ANY(:location_tag_id)' if isinstance(location_tag_id, set) else ':location_tag_id'}"
            )

        db_response = self.db.execute(
            text(
                GET_DEVICE_LOCATION_TAGS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'device_location_tag_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            device_location_tag_id=device_location_tag_id,
            device_id=device_id,
            location_tag_ids=location_tag_id,
        )

        return [DeviceLocationTag(**dict(row)) for row in db_response]

    def update_device_location_tag(
        self,
        device_location_tag_id: int,
        device_id: Optional[str] = None,
        location_tag_id: Optional[int] = None,
    ) -> Optional[DeviceLocationTag]:
        set_conditions: Set[str] = set()

        if device_id:
            set_conditions.add("device_id = :device_id")
        if location_tag_id:
            set_conditions.add("location_tag_id = :location_tag_id")

        if not set_conditions:
            return self.get_device_location_tag(device_location_tag_id=device_location_tag_id)

        db_response = self.db.execute(
            text(UPDATE_DEVICE_LOCATION_TAG_QUERY),
            device_id=device_id,
            location_tag_id=location_tag_id,
        ).fetchone()

        return DeviceLocationTag(
            device_location_tag_id=db_response["device_location_tag_id"],
            device_id=db_response["device_id"],
            location_tag_id=db_response["location_tag_id"],
        ) if db_response else None

    def delete_device_location_tag(self, device_location_tag_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_DEVICE_LOCATION_TAG_QUERY),
            device_location_tag_id=device_location_tag_id,
        ).scalar()

        return db_response

    def backup_device_location_tags(self) -> bool:
        self.db.execute(BACKUP_DEVICE_LOCATION_TAGS)
        return True

    def load_device_location_tags_from_backup(self) -> bool:
        self.db.execute(LOAD_DEVICE_LOCATION_TAGS_FROM_BACKUP)
        return True
