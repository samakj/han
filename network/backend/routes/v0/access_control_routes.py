import logging
from flask import Blueprint, current_app, request

from han_flask.exceptions import APIError
from han_flask.responses import JSONResponse

LOG = logging.getLogger(__name__)
ACCESS_CONTROLS_V0_BLUEPRINT = Blueprint(name="v0_access_control", import_name=__name__)


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/auth/access-control/", methods=["POST"])
def authorise_access_control() -> JSONResponse:
    request_data = request.get_json()

    user = current_app.user_store.get_user_by_username(username=request_data["username"])

    if user is None:
        raise APIError(404, "USER_NOT_FOUND", {"Ok": False, "Error": "User not found"})

    access_controls = current_app.access_control_store.get_access_controls(
        user_id=user.user_id,
        topic=request_data["topic"],
        action=request_data["acc"],
    )

    if len(access_controls) != 1:
        raise APIError(401, "UNAUTHORIZED", {"Ok": False, "Error": "Invalid user access"})

    return JSONResponse({
        "Ok": True
    })


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/access-controls/", methods=["POST"])
def create_access_control() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "access_control": current_app.access_control_store.create_access_control(
            user_id=request_data["user_id"],
            topic=request_data["topic"],
            action=request_data["action"],
        )
    })


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/access-controls/<int:access_control_id>/", methods=["GET"])
def get_access_control(access_control_id: int) -> JSONResponse:
    return JSONResponse({
        "access_control": current_app.access_control_store.get_access_control(
            access_control_id=access_control_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/access-controls/", methods=["GET"])
def get_access_controls() -> JSONResponse:
    return JSONResponse({
        "access_controls": current_app.access_control_store.get_access_controls(
            fields=set(request.args.getlist("fields")),
            user_id=set(request.args.getlist("user_id")),
            topic=set(request.args.getlist("topic")),
            action=set(request.args.getlist("action")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/access-controls/<int:access_control_id>/", methods=["PATCH"])
def update_access_control(access_control_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "access_control": current_app.access_control_store.update_access_control(
            access_control_id=access_control_id,
            user_id=request_data.get("user_id", None),
            topic=request_data.get("topic", None),
            action=request_data.get("action", None),
        )
    })


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/access-controls/<int:access_control_id>/", methods=["DELETE"])
def delete_access_control(access_control_id: int) -> JSONResponse:
    return JSONResponse({"access_control_id": current_app.access_control_store.delete_access_control(access_control_id=access_control_id)})


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/access-controls/backup/", methods=["POST"])
def backup_access_controls() -> JSONResponse:
    return JSONResponse({"success": current_app.access_control_store.backup_access_controls()})


@ACCESS_CONTROLS_V0_BLUEPRINT.route("/access-controls/load/", methods=["POST"])
def load_access_controls() -> JSONResponse:
    return JSONResponse({"success": current_app.access_control_store.load_access_controls_from_backup()})
