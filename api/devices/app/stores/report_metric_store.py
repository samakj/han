from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.report_metric_model import ReportMetric
from models.report_value_type import ReportValueType
from stores.queries.report_metric_queries import (
    CREATE_REPORT_METRIC_QUERY,
    DELETE_REPORT_METRIC_QUERY,
    GET_REPORT_METRIC_QUERY_TEMPLATE,
    GET_REPORT_METRIC_BY_NAME_QUERY_TEMPLATE,
    GET_REPORT_METRIC_BY_ABBREVIATION_QUERY_TEMPLATE,
    GET_REPORT_METRICS_QUERY_TEMPLATE,
    UPDATE_REPORT_METRIC_QUERY,
    BACKUP_REPORT_METRICS,
    LOAD_REPORT_METRICS_FROM_BACKUP,
)

ALL_FIELDS = {"report_metric_id", "name", "abbreviation", "report_value_type", "unit"}


class ReportMetricStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_report_metric(
        self,
        name: str,
        abbreviation: str,
        report_value_type: str,
        unit: Optional[str] = None,
    ) -> ReportMetric:
        if report_value_type not in ReportValueType.ALL:
            raise Exception

        db_response = self.db.execute(
            text(CREATE_REPORT_METRIC_QUERY),
            name=name,
            abbreviation=abbreviation,
            report_value_type=report_value_type,
            unit=unit,
        ).fetchone()

        return ReportMetric(
            report_metric_id=db_response["report_metric_id"],
            name=db_response["name"],
            abbreviation=db_response["abbreviation"],
            report_value_type=db_response["report_value_type"],
            unit=db_response["unit"],
        )

    def get_report_metric(
        self,
        report_metric_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[ReportMetric]:
        db_response = self.db.execute(
            text(
                GET_REPORT_METRIC_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            report_metric_id=report_metric_id,
        ).fetchone()

        return ReportMetric(**dict(db_response)) if db_response else None

    def get_report_metric_by_name(
        self,
        name: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[ReportMetric]:
        db_response = self.db.execute(
            text(
                GET_REPORT_METRIC_BY_NAME_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                )
            ),
            name=name,
        ).fetchone()

        return ReportMetric(**dict(db_response)) if db_response else None

    def get_report_metric_by_abbreviation(
        self,
        abbreviation: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[ReportMetric]:
        db_response = self.db.execute(
            text(
                GET_REPORT_METRIC_BY_ABBREVIATION_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_condition="abbreviation = :abbreviation",
                )
            ),
            abbreviation=abbreviation,
        ).fetchone()

        return ReportMetric(**dict(db_response)) if db_response else None

    def get_report_metrics(
        self,
        fields: Optional[Set[str]] = None,
        report_metric_id: Optional[Union[Set[int], int]] = None,
        name: Optional[Union[Set[str], str]] = None,
        abbreviation: Optional[Union[Set[Set], str]] = None,
        report_value_type: Optional[Union[List[str], str]] = None,
        unit: Optional[Union[Set[str], str]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[ReportMetric]:
        where_conditions: Set[str] = set()

        if report_metric_id:
            where_conditions.add(
                f"report_metric_id = "
                f"{'ANY(:report_metric_id)' if isinstance(report_metric_id, set) else ':report_metric_id'}"
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
        if report_value_type:
            where_conditions.add(
                f"device_id = "
                f"{'ANY(:report_value_type)' if isinstance(report_value_type, set) else ':level'}"
            )
        if unit:
            where_conditions.add(
                f"device_id = "
                f"{'ANY(:unit)' if isinstance(unit, set) else ':level'}"
            )

        db_response = self.db.execute(
            text(
                GET_REPORT_METRICS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'report_metric_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            report_metric_id=report_metric_id,
            name=name,
            abbreviation=abbreviation,
            report_value_type=report_value_type,
            unit=unit,
        )

        return [ReportMetric(**dict(row)) for row in db_response]

    def update_report_metric(
        self,
        report_metric_id: int,
        name: Optional[str] = None,
        abbreviation: Optional[str] = None,
        report_value_type: Optional[str] = None,
        unit: Optional[str] = None,
    ) -> Optional[ReportMetric]:
        if report_value_type is not None and report_value_type not in ReportValueType.ALL:
            raise Exception

        set_conditions: Set[str] = set()

        if name:
            set_conditions.add("name = :name")
        if abbreviation:
            set_conditions.add("abbreviation = :abbreviation")
        if report_value_type:
            set_conditions.add("report_value_type = :report_value_type")
        if unit:
            set_conditions.add("unit = :unit")

        if not set_conditions:
            return self.get_report_metric(report_metric_id=report_metric_id)

        db_response = self.db.execute(
            text(UPDATE_REPORT_METRIC_QUERY.format(set_conditions=", ".join(set_conditions))),
            report_metric_id=report_metric_id,
            name=name,
            abbreviation=abbreviation,
            report_value_type=report_value_type,
            unit=unit,
        ).fetchone()

        return ReportMetric(
            report_metric_id=db_response["report_metric_id"],
            name=db_response["name"],
            abbreviation=db_response["abbreviation"],
            report_value_type=db_response["report_value_type"],
            unit=db_response["unit"],
        ) if db_response else None

    def delete_report_metric(self, report_metric_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_REPORT_METRIC_QUERY),
            report_metric_id=report_metric_id,
        ).scalar()

        return db_response

    def backup_report_metrics(self) -> bool:
        self.db.execute(BACKUP_REPORT_METRICS)
        return True

    def load_report_metrics_from_backup(self) -> bool:
        self.db.execute(LOAD_REPORT_METRICS_FROM_BACKUP)
        return True
