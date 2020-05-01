from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.location_tag_model import LocationTag
from stores.queries.location_tag_queries import (
    CREATE_LOCATION_TAG_QUERY,
    DELETE_LOCATION_TAG_QUERY,
    GET_LOCATION_TAG_QUERY_TEMPLATE,
    GET_LOCATION_TAG_BY_NAME_QUERY_TEMPLATE,
    GET_LOCATION_TAGS_QUERY_TEMPLATE,
    UPDATE_LOCATION_TAG_QUERY,
    BACKUP_LOCATION_TAGS,
    LOAD_LOCATION_TAGS_FROM_BACKUP,
)

ALL_FIELDS = {"location_tag_id", "name", "level"}


class LocationTagStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_location_tag(self, name: str, level: int) -> LocationTag:
        db_response = self.db.execute(
            text(CREATE_LOCATION_TAG_QUERY),
            name=name,
            level=level,
        ).fetchone()

        return LocationTag(
            location_tag_id=db_response["location_tag_id"],
            name=db_response["name"],
            level=db_response["level"],
        )

    def get_location_tag(
        self,
        location_tag_id: int,
        fields: Optional[List[str]] = None,
    ) -> Optional[LocationTag]:
        db_response = self.db.execute(
            text(
                GET_LOCATION_TAG_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                )
            ),
            location_tag_id=location_tag_id,
        ).fetchone()

        return LocationTag(**dict(db_response)) if db_response else None

    def get_location_tag_by_name(
        self,
        name: str,
        fields: Optional[List[str]] = None,
    ) -> Optional[LocationTag]:
        db_response = self.db.execute(
            text(
                GET_LOCATION_TAG_BY_NAME_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                )
            ),
            name=name,
        ).fetchone()

        return LocationTag(**dict(db_response)) if db_response else None

    def get_location_tags(
        self,
        fields: Optional[Set[str]] = None,
        location_tag_id: Optional[Union[Set[int], int]] = None,
        name: Optional[Union[Set[str], str]] = None,
        level: Optional[Union[Set[int], int]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[LocationTag]:
        where_conditions: Set[str] = set()

        if location_tag_id:
            where_conditions.add(
                f"location_tag_id = "
                f"{'ANY(:location_tag_id)' if isinstance(location_tag_id, set) else ':location_tag_id'}"
            )
        if name:
            where_conditions.add(
                f"name = "
                f"{'ANY(:name)' if isinstance(name, set) else ':name'}"
            )
        if level:
            where_conditions.add(
                f"level = "
                f"{'ANY(:level)' if isinstance(level, set) else ':level'}"
            )

        db_response = self.db.execute(
            text(
                GET_LOCATION_TAGS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'level'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            location_tag_id=location_tag_id,
            name=name,
            level=level,
        )

        return [LocationTag(**dict(row)) for row in db_response]

    def update_location_tag(
        self,
        location_tag_id: int,
        name: Optional[str] = None,
        level: Optional[int] = None,
    ) -> Optional[LocationTag]:
        set_conditions: Set[str] = set()

        if name:
            set_conditions.add("name = :name")
        if level:
            set_conditions.add("level = :level")

        if not set_conditions:
            return self.get_location_tag(location_tag_id=location_tag_id)

        db_response = self.db.execute(
            text(UPDATE_LOCATION_TAG_QUERY),
            location_tag_id=location_tag_id,
            name=name,
            level=level,
        ).fetchone()

        return LocationTag(
            location_tag_id=db_response["location_tag_id"],
            name=db_response["name"],
            level=db_response["level"],
        ) if db_response else None

    def delete_location_tag(self, location_tag_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_LOCATION_TAG_QUERY),
            location_tag_id=location_tag_id,
        ).scalar()

        return db_response

    def backup_location_tags(self) -> bool:
        self.db.execute(BACKUP_LOCATION_TAGS)
        return True

    def load_location_tags_from_backup(self) -> bool:
        self.db.execute(LOAD_LOCATION_TAGS_FROM_BACKUP)
        return True
