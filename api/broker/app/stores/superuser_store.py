from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.superuser_model import Superuser
from stores.queries.superuser_queries import (
    CREATE_SUPERUSER_QUERY,
    DELETE_SUPERUSER_QUERY,
    GET_SUPERUSER_QUERY_TEMPLATE,
    GET_SUPERUSER_BY_USER_ID_QUERY_TEMPLATE,
    GET_SUPERUSERS_QUERY_TEMPLATE,
    UPDATE_SUPERUSER_QUERY_TEMPLATE,
    BACKUP_SUPERUSERS,
    LOAD_SUPERUSERS_FROM_BACKUP,
)

ALL_FIELDS = {"superuser_id", "user_id"}


class SuperuserStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_superuser(self, user_id: int) -> Superuser:
        db_response = self.db.execute(
            text(CREATE_SUPERUSER_QUERY),
            user_id=user_id,
        ).fetchone()

        return Superuser(
            superuser_id=db_response["superuser_id"],
            user_id=db_response["user_id"],
        )

    def get_superuser(
        self,
        superuser_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[Superuser]:
        db_response = self.db.execute(
            text(
                GET_SUPERUSER_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            superuser_id=superuser_id,
        ).fetchone()

        return Superuser(**dict(db_response)) if db_response else None

    def get_superuser_by_user_id(
        self,
        user_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[Superuser]:
        db_response = self.db.execute(
            text(
                GET_SUPERUSER_BY_USER_ID_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            user_id=user_id,
        ).fetchone()

        return Superuser(**dict(db_response)) if db_response else None

    def get_superusers(
        self,
        fields: Optional[Set[str]] = None,
        superuser_id: Optional[Union[Set[int], int]] = None,
        user_id: Optional[Union[Set[int], int]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[Superuser]:
        where_conditions: Set[str] = set()

        if superuser_id:
            where_conditions.add(
                f"superuser_id = "
                f"{'ANY(:superuser_id)' if isinstance(superuser_id, set) else ':superuser_id'}"
            )
        if user_id:
            where_conditions.add(
                f"user_id = "
                f"{'ANY(:user_id)' if isinstance(user_id, set) else ':user_id'}"
            )

        db_response = self.db.execute(
            text(
                GET_SUPERUSERS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'superuser_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            superuser_id=list(superuser_id) if isinstance(superuser_id, set) else superuser_id,
            user_id=list(user_id) if isinstance(user_id, set) else user_id,
        )

        return [Superuser(**dict(row)) for row in db_response]

    def update_superuser(
        self,
        superuser_id: int,
        user_id: Optional[str] = None,
    ) -> Optional[Superuser]:
        set_conditions: Set[str] = set()

        if user_id:
            set_conditions.add("user_id = :user_id")

        if not set_conditions:
            return self.get_superuser(superuser_id=superuser_id)

        db_response = self.db.execute(
            text(UPDATE_SUPERUSER_QUERY_TEMPLATE.format(set_conditions=", ".join(set_conditions))),
            superuser_id=superuser_id,
            user_id=user_id,
        ).fetchone()

        return Superuser(
            superuser_id=db_response["superuser_id"],
            user_id=db_response["user_id"],
        ) if db_response else None

    def delete_superuser(self, superuser_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_SUPERUSER_QUERY),
            superuser_id=superuser_id,
        ).scalar()

        return db_response

    def backup_superusers(self) -> bool:
        self.db.execute(BACKUP_SUPERUSERS)
        return True

    def load_superusers_from_backup(self) -> bool:
        self.db.execute(LOAD_SUPERUSERS_FROM_BACKUP)
        return True
