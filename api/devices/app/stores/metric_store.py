from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.metric_model import Metric
from stores.queries.metric_queries import (
    CREATE_METRIC_QUERY,
    DELETE_METRIC_QUERY,
    GET_METRIC_QUERY_TEMPLATE,
    GET_METRIC_BY_NAME_QUERY_TEMPLATE,
    GET_METRIC_BY_ABBREVIATION_QUERY_TEMPLATE,
    GET_METRICS_QUERY_TEMPLATE,
    UPDATE_METRIC_QUERY,
    BACKUP_METRICS,
    LOAD_METRICS_FROM_BACKUP,
)

ALL_FIELDS = {"metric_id", "name", "abbreviation", "value_type", "unit"}


class MetricStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_metric(
        self,
        name: str,
        abbreviation: str,
        value_type: str,
        unit: Optional[str] = None,
    ) -> Metric:
        db_response = self.db.execute(
            text(CREATE_METRIC_QUERY),
            name=name,
            abbreviation=abbreviation,
            value_type=value_type,
            unit=unit,
        ).fetchone()

        return Metric(
            metric_id=db_response["metric_id"],
            name=db_response["name"],
            abbreviation=db_response["abbreviation"],
            value_type=db_response["value_type"],
            unit=db_response["unit"],
        )

    def get_metric(
        self,
        metric_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[Metric]:
        db_response = self.db.execute(
            text(
                GET_METRIC_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            metric_id=metric_id,
        ).fetchone()

        return Metric(**dict(db_response)) if db_response else None

    def get_metric_by_name(
        self,
        name: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[Metric]:
        db_response = self.db.execute(
            text(
                GET_METRIC_BY_NAME_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                )
            ),
            name=name,
        ).fetchone()

        return Metric(**dict(db_response)) if db_response else None

    def get_metric_by_abbreviation(
        self,
        abbreviation: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[Metric]:
        db_response = self.db.execute(
            text(
                GET_METRIC_BY_ABBREVIATION_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_condition="abbreviation = :abbreviation",
                )
            ),
            abbreviation=abbreviation,
        ).fetchone()

        return Metric(**dict(db_response)) if db_response else None

    def get_metrics(
        self,
        fields: Optional[Set[str]] = None,
        metric_id: Optional[Union[Set[int], int]] = None,
        name: Optional[Union[Set[str], str]] = None,
        abbreviation: Optional[Union[Set[Set], str]] = None,
        unit: Optional[Union[Set[str], str]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[Metric]:
        where_conditions: Set[str] = set()

        if metric_id:
            where_conditions.add(
                f"metric_id = "
                f"{'ANY(:metric_id)' if isinstance(metric_id, set) else ':metric_id'}"
            )
        if name:
            where_conditions.add(
                f"name = "
                f"{'ANY(:name)' if isinstance(name, set) else ':name'}"
            )
        if abbreviation:
            where_conditions.add(
                f"abbreviation = "
                f"{'ANY(:abbreviation)' if isinstance(abbreviation, set) else ':abbreviation'}"
            )
        if unit:
            where_conditions.add(
                f"device_id = "
                f"{'ANY(:unit)' if isinstance(unit, set) else ':level'}"
            )

        db_response = self.db.execute(
            text(
                GET_METRICS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'metric_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            metric_id=list(metric_id) if isinstance(metric_id, set) else metric_id,
            name=list(name) if isinstance(name, set) else name,
            abbreviation=list(abbreviation) if isinstance(abbreviation, set) else abbreviation,
            unit=unit,
        )

        return [Metric(**dict(row)) for row in db_response]

    def update_metric(
        self,
        metric_id: int,
        name: Optional[str] = None,
        abbreviation: Optional[str] = None,
        value_type: Optional[str] = None,
        unit: Optional[str] = None,
    ) -> Optional[Metric]:

        set_conditions: Set[str] = set()

        if name:
            set_conditions.add("name = :name")
        if abbreviation:
            set_conditions.add("abbreviation = :abbreviation")
        if value_type:
            set_conditions.add("value_type = :value_type")
        if unit:
            set_conditions.add("unit = :unit")

        if not set_conditions:
            return self.get_metric(metric_id=metric_id)

        db_response = self.db.execute(
            text(UPDATE_METRIC_QUERY.format(set_conditions=", ".join(set_conditions))),
            metric_id=metric_id,
            name=name,
            abbreviation=abbreviation,
            value_type=value_type,
            unit=unit,
        ).fetchone()

        return Metric(
            metric_id=db_response["metric_id"],
            name=db_response["name"],
            abbreviation=db_response["abbreviation"],
            value_type=db_response["value_type"],
            unit=db_response["unit"],
        ) if db_response else None

    def delete_metric(self, metric_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_METRIC_QUERY),
            metric_id=metric_id,
        ).scalar()

        return db_response

    def backup_metrics(self) -> bool:
        self.db.execute(BACKUP_METRICS)
        return True

    def load_metrics_from_backup(self) -> bool:
        self.db.execute(LOAD_METRICS_FROM_BACKUP)
        return True
