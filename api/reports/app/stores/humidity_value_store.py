from decimal import Decimal
from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.humidity_value_model import HumidityValue
from stores.queries.humidity_value_queries import (
    CREATE_HUMIDITY_VALUE_QUERY,
    DELETE_HUMIDITY_VALUE_QUERY,
    GET_HUMIDITY_VALUE_QUERY_TEMPLATE,
    GET_HUMIDITY_VALUE_BY_REPORT_ID_QUERY_TEMPLATE,
    GET_HUMIDITY_VALUES_QUERY_TEMPLATE,
    UPDATE_HUMIDITY_VALUE_QUERY,
    BACKUP_HUMIDITY_VALUES,
    LOAD_HUMIDITY_VALUES_FROM_BACKUP,
)

ALL_FIELDS = {"humidity_value_id", "report_id", "value"}
DEFAULT_LIMIT = 1000


class HumidityValueStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_humidity_value(
        self,
        report_id: str,
        value: Decimal,
    ) -> HumidityValue:
        db_response = self.db.execute(
            text(CREATE_HUMIDITY_VALUE_QUERY),
            report_id=report_id,
            value=value,
        ).fetchone()

        return HumidityValue(
            humidity_value_id=db_response["humidity_value_id"],
            report_id=db_response["report_id"],
            value=db_response["value"],
        )

    def get_humidity_value(
        self,
        humidity_value_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[HumidityValue]:
        db_response = self.db.execute(
            text(
                GET_HUMIDITY_VALUE_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            humidity_value_id=humidity_value_id,
        ).fetchone()

        return HumidityValue(**dict(db_response)) if db_response else None

    def get_humidity_value_by_report_id(
        self,
        report_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[HumidityValue]:
        db_response = self.db.execute(
            text(
                GET_HUMIDITY_VALUE_BY_REPORT_ID_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            report_id=report_id,
        ).fetchone()

        return HumidityValue(**dict(db_response)) if db_response else None

    def get_humidity_values(
        self,
        fields: Optional[Set[str]] = None,
        humidity_value_id: Optional[Union[Set[int], int]] = None,
        report_id: Optional[Union[Set[int], int]] = None,
        value_gte: Optional[Decimal] = None,
        value_lte: Optional[Decimal] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[HumidityValue]:
        where_conditions: Set[str] = set()

        if humidity_value_id:
            where_conditions.add(
                f"humidity_value_id = "
                f"{'ANY(:humidity_value_id)' if isinstance(humidity_value_id, set) else ':humidity_value_id'}"
            )
        if report_id:
            where_conditions.add(
                f"name = "
                f"{'ANY(:report_id)' if isinstance(report_id, set) else ':report_id'}"
            )
        if value_gte:
            where_conditions.add("value >= :value_gte")
        if value_lte:
            where_conditions.add("value <= :value_lte")

        db_response = self.db.execute(
            text(
                GET_HUMIDITY_VALUES_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'humidity_value_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    ),
                    limit=limit or DEFAULT_LIMIT
                ),
            ),
            humidity_value_id=list(humidity_value_id) if isinstance(humidity_value_id, set) else humidity_value_id,
            report_id=list(report_id) if isinstance(report_id, set) else report_id,
            value_gte=value_gte,
            value_lte=value_lte,
        )

        return [HumidityValue(**dict(row)) for row in db_response]

    def update_humidity_value(
        self,
        humidity_value_id: int,
        report_id: Optional[int] = None,
        value: Optional[Decimal] = None,
    ) -> Optional[HumidityValue]:
        set_conditions: Set[str] = set()

        if report_id:
            set_conditions.add("report_id = :report_id")
        if value:
            set_conditions.add("value = :value")

        if not set_conditions:
            return self.get_humidity_value(humidity_value_id=humidity_value_id)

        db_response = self.db.execute(
            text(UPDATE_HUMIDITY_VALUE_QUERY.format(set_conditions=", ".join(set_conditions))),
            humidity_value_id=humidity_value_id,
            report_id=report_id,
            value=value,
        ).fetchone()

        return HumidityValue(
            humidity_value_id=db_response["humidity_value_id"],
            report_id=db_response["report_id"],
            value=db_response["value"],
        ) if db_response else None

    def delete_humidity_value(self, humidity_value_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_HUMIDITY_VALUE_QUERY),
            humidity_value_id=humidity_value_id,
        ).scalar()

        return db_response

    def backup_humidity_values(self) -> bool:
        self.db.execute(BACKUP_HUMIDITY_VALUES)
        return True

    def load_humidity_values_from_backup(self) -> bool:
        self.db.execute(LOAD_HUMIDITY_VALUES_FROM_BACKUP)
        return True
