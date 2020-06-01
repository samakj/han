import logging
from flask import Blueprint, current_app, request

from flagon.exceptions import APIError
from flagon.responses import JSONResponse

LOG = logging.getLogger(__name__)
SUPERUSERS_V0_BLUEPRINT = Blueprint(name="v0_superuser", import_name=__name__)


@SUPERUSERS_V0_BLUEPRINT.route("/auth/superuser/", methods=["POST"])
def authorise_superuser() -> JSONResponse:
    request_data = request.get_json()

    user = current_app.user_store.get_user_by_username(username=request_data["username"])

    if user is None:
        raise APIError(404, "USER_NOT_FOUND", {"Ok": False, "Error": "User not found"})

    superuser = current_app.superuser_store.get_superuser_by_user_id(user_id=user.user_id)

    if superuser is None:
        raise APIError(400, "INVALID_SUPERUSER", {"Ok": False, "Error": "Invalid super user"})

    return JSONResponse({
        "Ok": True
    })


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/", methods=["POST"])
def create_superuser() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "superuser": current_app.superuser_store.create_superuser(
            user_id=request_data["user_id"],
        )
    })


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/<int:superuser_id>/", methods=["GET"])
def get_superuser(superuser_id: int) -> JSONResponse:
    return JSONResponse({
        "superuser": current_app.superuser_store.get_superuser(
            superuser_id=superuser_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/user-id/<int:user_id>", methods=["GET"])
def get_superuser_by_user_id(user_id: int) -> JSONResponse:
    return JSONResponse({
        "superuser": current_app.superuser_store.get_superuser_by_user_id(
            user_id=user_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/", methods=["GET"])
def get_superusers() -> JSONResponse:
    return JSONResponse({
        "superusers": current_app.superuser_store.get_superusers(
            fields=set(request.args.getlist("fields")),
            superuser_id=set(request.args.getlist("superuser_id")),
            user_id=set(request.args.getlist("user_id")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/<int:superuser_id>/", methods=["PATCH"])
def update_superuser(superuser_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "superuser": current_app.superuser_store.update_superuser(
            superuser_id=superuser_id,
            user_id=request_data.get("user_id", None),
        )
    })


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/<int:superuser_id>/", methods=["DELETE"])
def delete_superuser(superuser_id: int) -> JSONResponse:
    return JSONResponse({"superuser_id": current_app.superuser_store.delete_superuser(superuser_id=superuser_id)})


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/backup/", methods=["POST"])
def backup_superusers() -> JSONResponse:
    return JSONResponse({"success": current_app.superuser_store.backup_superusers()})


@SUPERUSERS_V0_BLUEPRINT.route("/superusers/load/", methods=["POST"])
def load_superusers() -> JSONResponse:
    return JSONResponse({"success": current_app.superuser_store.load_superusers_from_backup()})
