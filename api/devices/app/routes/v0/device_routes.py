from flask import Blueprint, current_app, request
from flagon.responses import JSONResponse

DEVICES_V0_BLUEPRINT = Blueprint(name="v0_devices", import_name=__name__)


@DEVICES_V0_BLUEPRINT.route("/devices/", methods=["POST"])
def create_device() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device": current_app.device_store.create_device(
            device_id=request_data["device_id"],
            location_tag_ids=(
                set(request_data["location_tag_ids"])
                if request_data.get("location_tag_ids", None) is not None else None
            ),
            report_metric_ids=(
                set(request_data["report_metric_ids"])
                if request_data.get("report_metric_ids", None) is not None else None
            ),
        )
    })


@DEVICES_V0_BLUEPRINT.route("/devices/<string:device_id>/", methods=["GET"])
def get_device(device_id: str) -> JSONResponse:
    return JSONResponse({
        "device": current_app.device_store.get_device(
            device_id=device_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@DEVICES_V0_BLUEPRINT.route("/devices/", methods=["GET"])
def get_devices() -> JSONResponse:
    return JSONResponse({
        "devices": current_app.device_store.get_devices(
            fields=set(request.args.getlist("fields")),
            device_id=set(request.args.getlist("device_id")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@DEVICES_V0_BLUEPRINT.route("/devices/<string:device_id>/", methods=["PATCH"])
def update_device(device_id: str) -> JSONResponse:
    return JSONResponse({"device": current_app.device_store.update_device(device_id=device_id)})


@DEVICES_V0_BLUEPRINT.route("/devices/<string:device_id>/", methods=["DELETE"])
def delete_device(device_id: str) -> JSONResponse:
    return JSONResponse({"device_id": current_app.device_store.delete_device(device_id=device_id)})


@DEVICES_V0_BLUEPRINT.route("/devices/backup/", methods=["POST"])
def backup_devices() -> JSONResponse:
    return JSONResponse({"success": current_app.device_store.backup_devices()})


@DEVICES_V0_BLUEPRINT.route("/devices/load/", methods=["POST"])
def load_devices() -> JSONResponse:
    return JSONResponse({"success": current_app.device_store.load_devices_from_backup()})
