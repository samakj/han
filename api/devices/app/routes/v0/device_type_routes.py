from flask import Blueprint, current_app, request
from flagon.responses import JSONResponse

DEVICE_TYPES_V0_BLUEPRINT = Blueprint(name="v0_device_types", import_name=__name__)


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/", methods=["POST"])
def create_device_type() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device_type": current_app.device_type_store.create_device_type(
            name=request_data["name"],
            report_period=request_data["report_period"],
        )
    })


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/<int:device_type_id>/", methods=["GET"])
def get_device_type(device_type_id: int) -> JSONResponse:
    return JSONResponse({
        "device_type": current_app.device_type_store.get_device_type(
            device_type_id=device_type_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/<string:name>/", methods=["GET"])
def get_device_type_by_name(name: str) -> JSONResponse:
    return JSONResponse({
        "device_type": current_app.device_type_store.get_device_type_by_name(
            name=name,
            fields=set(request.args.getlist("fields")),
        )
    })


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/", methods=["GET"])
def get_device_types() -> JSONResponse:
    return JSONResponse({
        "device_types": current_app.device_type_store.get_device_types(
            fields=set(request.args.getlist("fields")),
            device_type_id=set(request.args.getlist("device_type_id")),
            name=set(request.args.getlist("name")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/<int:device_type_id>/", methods=["PATCH"])
def update_device_type(device_type_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device_type": current_app.device_type_store.update_device_type(
            device_type_id=device_type_id,
            name=request_data.get("name", None),
        )
    })


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/<int:device_type_id>/", methods=["DELETE"])
def delete_device_type(device_type_id: int) -> JSONResponse:
    return JSONResponse({"device_type_id": current_app.device_type_store.delete_device_type(device_type_id=device_type_id)})


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/backup/", methods=["POST"])
def backup_device_types() -> JSONResponse:
    return JSONResponse({"success": current_app.device_type_store.backup_device_types()})


@DEVICE_TYPES_V0_BLUEPRINT.route("/device-types/load/", methods=["POST"])
def load_device_types() -> JSONResponse:
    return JSONResponse({"success": current_app.device_type_store.load_device_types_from_backup()})
