from decimal import Decimal
from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.temperature_value_model import TemperatureValue
from stores.queries.temperature_value_queries import (
    CREATE_TEMPERATURE_VALUE_QUERY,
    DELETE_TEMPERATURE_VALUE_QUERY,
    GET_TEMPERATURE_VALUE_QUERY_TEMPLATE,
    GET_TEMPERATURE_VALUE_BY_REPORT_ID_QUERY_TEMPLATE,
    GET_TEMPERATURE_VALUES_QUERY_TEMPLATE,
    UPDATE_TEMPERATURE_VALUE_QUERY,
    BACKUP_TEMPERATURE_VALUES,
    LOAD_TEMPERATURE_VALUES_FROM_BACKUP,
)

ALL_FIELDS = {"temperature_value_id", "report_id", "value"}
DEFAULT_LIMIT = 1000


class TemperatureValueStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_temperature_value(
        self,
        report_id: str,
        value: Decimal,
    ) -> TemperatureValue:
        db_response = self.db.execute(
            text(CREATE_TEMPERATURE_VALUE_QUERY),
            report_id=report_id,
            value=value,
        ).fetchone()

        return TemperatureValue(
            temperature_value_id=db_response["temperature_value_id"],
            report_id=db_response["report_id"],
            value=db_response["value"],
        )

    def get_temperature_value(
        self,
        temperature_value_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[TemperatureValue]:
        db_response = self.db.execute(
            text(
                GET_TEMPERATURE_VALUE_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            temperature_value_id=temperature_value_id,
        ).fetchone()

        return TemperatureValue(**dict(db_response)) if db_response else None

    def get_temperature_value_by_report_id(
        self,
        report_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[TemperatureValue]:
        db_response = self.db.execute(
            text(
                GET_TEMPERATURE_VALUE_BY_REPORT_ID_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            report_id=report_id,
        ).fetchone()

        return TemperatureValue(**dict(db_response)) if db_response else None

    def get_temperature_values(
        self,
        fields: Optional[Set[str]] = None,
        temperature_value_id: Optional[Union[Set[int], int]] = None,
        report_id: Optional[Union[Set[int], int]] = None,
        value_gte: Optional[Decimal] = None,
        value_lte: Optional[Decimal] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[TemperatureValue]:
        where_conditions: Set[str] = set()

        if temperature_value_id:
            where_conditions.add(
                f"temperature_value_id = "
                f"{'ANY(:temperature_value_id)' if isinstance(temperature_value_id, set) else ':temperature_value_id'}"
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
                GET_TEMPERATURE_VALUES_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'temperature_value_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    ),
                    limit=limit or DEFAULT_LIMIT
                ),
            ),
            temperature_value_id=list(temperature_value_id) if isinstance(temperature_value_id, set) else temperature_value_id,
            report_id=list(report_id) if isinstance(report_id, set) else report_id,
            value_gte=value_gte,
            value_lte=value_lte,
        )

        return [TemperatureValue(**dict(row)) for row in db_response]

    def update_temperature_value(
        self,
        temperature_value_id: int,
        report_id: Optional[int] = None,
        value: Optional[Decimal] = None,
    ) -> Optional[TemperatureValue]:
        set_conditions: Set[str] = set()

        if report_id:
            set_conditions.add("report_id = :report_id")
        if value:
            set_conditions.add("value = :value")

        if not set_conditions:
            return self.get_temperature_value(temperature_value_id=temperature_value_id)

        db_response = self.db.execute(
            text(UPDATE_TEMPERATURE_VALUE_QUERY.format(set_conditions=", ".join(set_conditions))),
            temperature_value_id=temperature_value_id,
            report_id=report_id,
            value=value,
        ).fetchone()

        return TemperatureValue(
            temperature_value_id=db_response["temperature_value_id"],
            report_id=db_response["report_id"],
            value=db_response["value"],
        ) if db_response else None

    def delete_temperature_value(self, temperature_value_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_TEMPERATURE_VALUE_QUERY),
            temperature_value_id=temperature_value_id,
        ).scalar()

        return db_response

    def backup_temperature_values(self) -> bool:
        self.db.execute(BACKUP_TEMPERATURE_VALUES)
        return True

    def load_temperature_values_from_backup(self) -> bool:
        self.db.execute(LOAD_TEMPERATURE_VALUES_FROM_BACKUP)
        return True
