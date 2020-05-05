from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.motion_value_model import MotionValue
from stores.queries.motion_value_queries import (
    CREATE_MOTION_VALUE_QUERY,
    DELETE_MOTION_VALUE_QUERY,
    GET_MOTION_VALUE_QUERY_TEMPLATE,
    GET_MOTION_VALUE_BY_REPORT_ID_QUERY_TEMPLATE,
    GET_MOTION_VALUES_QUERY_TEMPLATE,
    UPDATE_MOTION_VALUE_QUERY,
    BACKUP_MOTION_VALUES,
    LOAD_MOTION_VALUES_FROM_BACKUP,
)

ALL_FIELDS = {"motion_value_id", "report_id", "value"}
DEFAULT_LIMIT = 1000


class MotionValueStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_motion_value(
        self,
        report_id: str,
        value: bool,
    ) -> MotionValue:
        db_response = self.db.execute(
            text(CREATE_MOTION_VALUE_QUERY),
            report_id=report_id,
            value=value,
        ).fetchone()

        return MotionValue(
            motion_value_id=db_response["motion_value_id"],
            report_id=db_response["report_id"],
            value=db_response["value"],
        )

    def get_motion_value(
        self,
        motion_value_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[MotionValue]:
        db_response = self.db.execute(
            text(
                GET_MOTION_VALUE_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            motion_value_id=motion_value_id,
        ).fetchone()

        return MotionValue(**dict(db_response)) if db_response else None

    def get_motion_value_by_report_id(
        self,
        report_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[MotionValue]:
        db_response = self.db.execute(
            text(
                GET_MOTION_VALUE_BY_REPORT_ID_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            report_id=report_id,
        ).fetchone()

        return MotionValue(**dict(db_response)) if db_response else None

    def get_motion_values(
        self,
        fields: Optional[Set[str]] = None,
        motion_value_id: Optional[Union[Set[int], int]] = None,
        report_id: Optional[Union[Set[int], int]] = None,
        value: Optional[bool] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[MotionValue]:
        where_conditions: Set[str] = set()

        if motion_value_id:
            where_conditions.add(
                f"motion_value_id = "
                f"{'ANY(:motion_value_id)' if isinstance(motion_value_id, set) else ':motion_value_id'}"
            )
        if report_id:
            where_conditions.add(
                f"name = "
                f"{'ANY(:report_id)' if isinstance(report_id, set) else ':report_id'}"
            )
        if value:
            where_conditions.add("value = :value")

        db_response = self.db.execute(
            text(
                GET_MOTION_VALUES_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'motion_value_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    ),
                    limit=limit or DEFAULT_LIMIT
                ),
            ),
            motion_value_id=list(motion_value_id) if isinstance(motion_value_id, set) else motion_value_id,
            report_id=list(report_id) if isinstance(report_id, set) else report_id,
            value=value,
        )

        return [MotionValue(**dict(row)) for row in db_response]

    def update_motion_value(
        self,
        motion_value_id: int,
        report_id: Optional[int] = None,
        value: Optional[bool] = None,
    ) -> Optional[MotionValue]:
        set_conditions: Set[str] = set()

        if report_id:
            set_conditions.add("report_id = :report_id")
        if value:
            set_conditions.add("value = :value")

        if not set_conditions:
            return self.get_motion_value(motion_value_id=motion_value_id)

        db_response = self.db.execute(
            text(UPDATE_MOTION_VALUE_QUERY.format(set_conditions=", ".join(set_conditions))),
            motion_value_id=motion_value_id,
            report_id=report_id,
            value=value,
        ).fetchone()

        return MotionValue(
            motion_value_id=db_response["motion_value_id"],
            report_id=db_response["report_id"],
            value=db_response["value"],
        ) if db_response else None

    def delete_motion_value(self, motion_value_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_MOTION_VALUE_QUERY),
            motion_value_id=motion_value_id,
        ).scalar()

        return db_response

    def backup_motion_values(self) -> bool:
        self.db.execute(BACKUP_MOTION_VALUES)
        return True

    def load_motion_values_from_backup(self) -> bool:
        self.db.execute(LOAD_MOTION_VALUES_FROM_BACKUP)
        return True
