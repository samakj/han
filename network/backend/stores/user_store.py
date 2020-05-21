from typing import List, Optional, Set, Union

from han_flask.exceptions import APIError
from sqlalchemy import text
from sqlalchemy.engine import Engine

from crypto.password import hash_password, verify_password
from models.user_model import User
from stores.queries.user_queries import (
    CREATE_USER_QUERY,
    DELETE_USER_QUERY,
    GET_USER_QUERY_TEMPLATE,
    GET_USER_BY_USERNAME_QUERY_TEMPLATE,
    GET_USER_BY_MAC_ADDRESS_QUERY_TEMPLATE,
    GET_USERS_QUERY_TEMPLATE,
    UPDATE_USER_QUERY_TEMPLATE,
    BACKUP_USERS,
    LOAD_USERS_FROM_BACKUP,
)

ALL_FIELDS = {"user_id", "username", "mac_address"}


class UserStore:
    def __init__(self, db: Engine):
        self.db = db

    def create_user(self, username: str, password: str, mac_address: Optional[str] = None) -> User:
        db_response = self.db.execute(
            text(CREATE_USER_QUERY),
            username=username,
            password=hash_password(raw_password=password),
            mac_address=mac_address,
        ).fetchone()

        return User(
            user_id=db_response["user_id"],
            username=db_response["username"],
            mac_address=db_response["mac_address"],
        )

    def get_user(
        self,
        user_id: int,
        fields: Optional[Set[str]] = None,
    ) -> Optional[User]:
        db_response = self.db.execute(
            text(
                GET_USER_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            user_id=user_id,
        ).fetchone()

        return User(**dict(db_response)) if db_response else None

    def get_user_by_username(
        self,
        username: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[User]:
        db_response = self.db.execute(
            text(
                GET_USER_BY_USERNAME_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            username=username,
        ).fetchone()

        return User(**dict(db_response)) if db_response else None

    def get_user_by_mac_address(
        self,
        mac_address: str,
        fields: Optional[Set[str]] = None,
    ) -> Optional[User]:
        db_response = self.db.execute(
            text(
                GET_USER_BY_MAC_ADDRESS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS)
                )
            ),
            mac_address=mac_address,
        ).fetchone()

        return User(**dict(db_response)) if db_response else None

    def get_users(
        self,
        fields: Optional[Set[str]] = None,
        user_id: Optional[Union[Set[int], int]] = None,
        username: Optional[Union[Set[str], str]] = None,
        mac_address: Optional[Union[Set[str], str]] = None,
        order_by: Optional[str] = None,
        order_by_direction: Optional[str] = None,
    ) -> List[User]:
        where_conditions: Set[str] = set()

        if user_id:
            where_conditions.add(
                f"user_id = "
                f"{'ANY(:user_id)' if isinstance(user_id, set) else ':user_id'}"
            )
        if username:
            where_conditions.add(
                f"username = "
                f"{'ANY(:username)' if isinstance(username, set) else ':username'}"
            )
        if mac_address:
            where_conditions.add(
                f"mac_address = "
                f"{'ANY(:mac_address)' if isinstance(mac_address, set) else ':mac_address'}"
            )

        db_response = self.db.execute(
            text(
                GET_USERS_QUERY_TEMPLATE.format(
                    fields=", ".join((fields or ALL_FIELDS) & ALL_FIELDS),
                    where_conditions=" AND ".join(where_conditions) if where_conditions else "TRUE",
                    order_by_condition=(
                        f"{order_by if order_by in ALL_FIELDS else 'user_id'} "
                        f"{order_by_direction if order_by_direction in {'ASC', 'DESC'} else 'ASC'}"
                    )
                ),
            ),
            user_id=list(user_id) if isinstance(user_id, set) else user_id,
            username=list(username) if isinstance(username, set) else username,
            mac_address=list(mac_address) if isinstance(mac_address, set) else mac_address,
        )

        return [User(**dict(row)) for row in db_response]

    def verify_user(self, user_id: int, username: str, password: str,  mac_address: Optional[str] = None) -> bool:
        db_response = self.db.execute(
            text(
                GET_USERS_QUERY_TEMPLATE.format(
                    fields="password",
                    where_conditions="user_id = :user_id AND username = :username AND mac_address = :mac_address",
                    order_by_condition="user_id ASC"
                ),
            ),
            user_id=user_id,
            username=username,
            mac_address=mac_address,
        ).fetchone()

        if db_response is None:
            return False

        return verify_password(db_password=db_response["password"], test_password=password)

    def update_user(
        self,
        user_id: int,
        current_username: str,
        current_password: str,
        current_mac_address: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        mac_address: Optional[str] = None,
    ) -> Optional[User]:
        set_conditions: Set[str] = set()

        if not self.verify_user(
            user_id=user_id,
            username=current_username,
            password=current_password,
            mac_address=current_mac_address,
        ):
            raise APIError(401, "UNAUTHORIZED")

        if username:
            set_conditions.add("username = :username")
        if password:
            set_conditions.add("password = :password")
        if mac_address:
            set_conditions.add("mac_address = :mac_address")

        if not set_conditions:
            return self.get_user(user_id=user_id)

        db_response = self.db.execute(
            text(UPDATE_USER_QUERY_TEMPLATE.format(set_conditions=", ".join(set_conditions))),
            user_id=user_id,
            username=username,
            password=hash_password(raw_password=password),
            mac_address=mac_address,
        ).fetchone()

        return User(
            user_id=db_response["user_id"],
            username=db_response["username"],
            mac_address=db_response["mac_address"],
        ) if db_response else None

    def delete_user(self, user_id: int) -> Optional[int]:
        db_response = self.db.execute(
            text(DELETE_USER_QUERY),
            user_id=user_id,
        ).scalar()

        return db_response

    def backup_users(self) -> bool:
        self.db.execute(BACKUP_USERS)
        return True

    def load_users_from_backup(self) -> bool:
        self.db.execute(LOAD_USERS_FROM_BACKUP)
        return True
