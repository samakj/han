from typing import List, Optional, Set, Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from models.action_map import ActionMap
from models.access_control_model import AccessControl
from stores.queries.access_control_queries import (
    CREATE_ACCESS_CONTROL_QUERY,
    DELETE_ACCESS_CONTROL_QUERY,
    GET_ACCESS_CONTROL_QUERY_TEMPLATE,
    GET_ACCESS_CONTROLS_QUERY_TEMPLATE,
    UPDATE_ACCESS_CONTROL_QUERY_TEMPLATE,
    BACKUP_ACCESS_CONTROLS,
    LOAD_ACCESS_CONTROLS_FROM_BACKUP,
)

ALL_FIELDS = {"access_control_id", "user_id", "topic", "action"}


class AccessControlStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_access_control(self, user_id: int, topic: str, action: Union[str, int]) -> AccessControl:
        db_response = self.db.execute(
            text(CREATE_ACCESS_CONTROL_QUERY),
            user_id=user_id,
            topic=topic,
            action=ActionMap[action.upper()] if isinstance(action, str) else action,
        ).fetchone()

        return AccessControl(
            access_control_id=db_response["access_control_id"],
            user_id=db_response["user_id"],
            topic=db_response["topic"],
            action=db_response["action"],
            action_verbose=ActionMap[db_response["action"]],
        )

    def get_access_control(
        self,
        access_control_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[AccessControl]:
        db_response = self.db.execute(
            text(
                GET_ACCESS_CONTROL_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            access_control_id=access_control_id,
        ).fetchone()

        response_dict = dict(db_response)
        if "action" in response_dict:
            response_dict["action_verbose"] = ActionMap[db_response["action"]]

        return AccessControl(**response_dict) if db_response else None

    def get_access_controls(
        self,
        fields: Optional[Set[str]] = None,
        access_control_id: Optional[Union[Set[int], int]] = None,
        user_id: Optional[Union[Set[int], int]] = None,
        topic: Optional[Union[Set[str], str]] = None,
        action: Optional[Union[Set[int], int]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[AccessControl]:
        where_conditions: Set[str] = set()

        if access_control_id:
            where_conditions.add(
                f"access_control_id = "
                f"{'ANY(:access_control_id)' if isinstance(access_control_id, set) else ':access_control_id'}"
            )
        if user_id:
            where_conditions.add(
                f"user_id = "
                f"{'ANY(:user_id)' if isinstance(user_id, set) else ':user_id'}"
            )
        if topic:
            where_conditions.add(
                f"topic = "
                f"{'ANY(:topic)' if isinstance(topic, set) else ':topic'}"
            )
        if action:
            where_conditions.add(
                f"action = "
                f"{'ANY(:action)' if isinstance(action, set) else ':action'}"
            )

        db_response = self.db.execute(
            text(
                GET_ACCESS_CONTROLS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'access_control_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            access_control_id=list(access_control_id) if isinstance(access_control_id, set) else access_control_id,
            user_id=list(user_id) if isinstance(user_id, set) else user_id,
            topic=list(topic) if isinstance(topic, set) else topic,
            action=list(action) if isinstance(action, set) else action,
        )

        access_controls: List[AccessControl] = []

        for row in db_response:
            response_dict = dict(row)
            if "action" in response_dict:
                response_dict["action_verbose"] = ActionMap[response_dict["action"]]

            access_controls.append(AccessControl(**dict(response_dict)))

        return access_controls

    def update_access_control(
        self,
        access_control_id: int,
        user_id: Optional[int] = None,
        topic: Optional[str] = None,
        action: Optional[int] = None,
    ) -> Optional[AccessControl]:
        set_conditions: Set[str] = set()

        if user_id:
            set_conditions.add("user_id = :user_id")
        if topic:
            set_conditions.add("topic = :topic")
        if action:
            set_conditions.add("action = :action")

        if not set_conditions:
            return self.get_access_control(access_control_id=access_control_id)

        db_response = self.db.execute(
            text(UPDATE_ACCESS_CONTROL_QUERY_TEMPLATE.format(set_conditions=", ".join(set_conditions))),
            access_control_id=access_control_id,
            user_id=user_id,
            topic=topic,
            action=action,
        ).fetchone()

        return AccessControl(
            access_control_id=db_response["access_control_id"],
            user_id=db_response["user_id"],
            topic=db_response["topic"],
            action=db_response["action"],
            action_verbose=ActionMap[db_response["action"]],
        ) if db_response else None

    def delete_access_control(self, access_control_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_ACCESS_CONTROL_QUERY),
            access_control_id=access_control_id,
        ).scalar()

        return db_response

    def backup_access_controls(self) -> bool:
        self.db.execute(BACKUP_ACCESS_CONTROLS)
        return True

    def load_access_controls_from_backup(self) -> bool:
        self.db.execute(LOAD_ACCESS_CONTROLS_FROM_BACKUP)
        return True
