import logging
from flask import Blueprint, current_app, request

from flagon.responses import JSONResponse

LOG = logging.getLogger(__name__)
USERS_V0_BLUEPRINT = Blueprint(name="v0_user", import_name=__name__)


@USERS_V0_BLUEPRINT.route("/auth/user/", methods=["POST"])
def authorise_user() -> JSONResponse:
    request_data = request.get_json()

    user = current_app.user_store.get_user_by_username(username=request_data["username"])
    mac_address = request_data["clientid"].lower() if request_data.get("clientid", None) is not None else None

    error = None

    if not user:
        error = f"User not found: {request_data['username']}"
    if error is None and mac_address != user.mac_address:
        error = "Invalid mac address for user"

    if error is None and not current_app.user_store.verify_user(
        user_id=user.user_id,
        username=user.username,
        password=request_data["password"],
        mac_address=user.mac_address,
    ):
        error = "User verification failed"

    return JSONResponse({
        "Ok": error is None,
        "Error": error,
    })


@USERS_V0_BLUEPRINT.route("/users/", methods=["POST"])
def create_user() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "user": current_app.user_store.create_user(
            username=request_data["username"],
            password=request_data["password"],
            mac_address=(
                request_data["clientid"].lower()
                if request_data.get("clientid", None) is not None else
                None
            ),
        )
    })


@USERS_V0_BLUEPRINT.route("/users/<int:user_id>/", methods=["GET"])
def get_user(user_id: int) -> JSONResponse:
    return JSONResponse({
        "user": current_app.user_store.get_user(
            user_id=user_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@USERS_V0_BLUEPRINT.route("/users/username/<string:username>/", methods=["GET"])
def get_user_by_username(username: str) -> JSONResponse:
    return JSONResponse({
        "user": current_app.user_store.get_user_by_username(
            username=username,
            fields=set(request.args.getlist("fields")),
        )
    })


@USERS_V0_BLUEPRINT.route("/users/mac-address/<string:mac_address>/", methods=["GET"])
def get_user_by_mac_address(mac_address: str) -> JSONResponse:
    return JSONResponse({
        "user": current_app.user_store.get_user_by_mac_address(
            username=mac_address,
            fields=set(request.args.getlist("fields")),
        )
    })


@USERS_V0_BLUEPRINT.route("/users/", methods=["GET"])
def get_users() -> JSONResponse:
    return JSONResponse({
        "users": current_app.user_store.get_users(
            fields=set(request.args.getlist("fields")),
            user_id=set(request.args.getlist("user_id")),
            username=set(request.args.getlist("username")),
            mac_address=set(request.args.getlist("mac_address", lambda x: x.lower())),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@USERS_V0_BLUEPRINT.route("/users/<int:user_id>/", methods=["PATCH"])
def update_user(user_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "user": current_app.user_store.update_user(
            user_id=user_id,
            current_username=request_data["current_username"],
            current_password=request_data["current_password"],
            current_mac_address=(
                request_data["current_mac_address"].lower()
                if request_data.get("current_mac_address", None) is not None else
                None
            ),
            username=request_data.get("username", None),
            password=request_data.get("password", None),
            mac_address=(
                request_data["mac_address"].lower()
                if request_data.get("mac_address", None) is not None else
                None
            ),
        )
    })


@USERS_V0_BLUEPRINT.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id: int) -> JSONResponse:
    return JSONResponse({"user_id": current_app.user_store.delete_user(user_id=user_id)})


@USERS_V0_BLUEPRINT.route("/users/backup/", methods=["POST"])
def backup_users() -> JSONResponse:
    return JSONResponse({"success": current_app.user_store.backup_users()})


@USERS_V0_BLUEPRINT.route("/users/load/", methods=["POST"])
def load_users() -> JSONResponse:
    return JSONResponse({"success": current_app.user_store.load_users_from_backup()})
