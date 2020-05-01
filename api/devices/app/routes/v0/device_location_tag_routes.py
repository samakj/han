from flask import Blueprint, current_app, request
from han_flask.responses import JSONResponse

DEVICE_LOCATION_TAGS_V0_BLUEPRINT = Blueprint(name="v0_device_location_tags", import_name=__name__)


@DEVICE_LOCATION_TAGS_V0_BLUEPRINT.route("/device-location-tags/", methods=["POST"])
def create_device_location_tag() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device_location_tag": current_app.device_location_tag_store.create_device_location_tag(
            device_location_tag_id=request_data["device_location_tag_id"],
            device_id=request_data["device_id"],
            location_tag_id=request_data["location_tag_id"],
        )
    })


@DEVICE_LOCATION_TAGS_V0_BLUEPRINT.route("/device-location-tags/<int:device_location_tag_id>/", methods=["GET"])
def get_device_location_tag(device_location_tag_id: int) -> JSONResponse:
    return JSONResponse({
        "device_location_tag": current_app.device_location_tag_store.get_device_location_tag(
            device_location_tag_id=device_location_tag_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@DEVICE_LOCATION_TAGS_V0_BLUEPRINT.route("/device-location-tags/", methods=["GET"])
def get_device_location_tags() -> JSONResponse:
    return JSONResponse({
        "device_location_tags": current_app.device_location_tag_store.get_device_location_tags(
            fields=set(request.args.getlist("fields")),
            device_location_tag_id=set(request.args.getlist("device_location_tag_id")),
            device_id=set(request.args.getlist("device_id")),
            location_tag_id=set(request.args.getlist("location_tag_id")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@DEVICE_LOCATION_TAGS_V0_BLUEPRINT.route("/device-location-tags/<int:device_location_tag_id>/", methods=["PATCH"])
def update_device_location_tag(device_location_tag_id: int) -> JSONResponse:
    return JSONResponse({"device_location_tag": current_app.device_location_tag_store.update_device_location_tag(device_location_tag_id=device_location_tag_id)})


@DEVICE_LOCATION_TAGS_V0_BLUEPRINT.route("/device-location-tags/<int:device_location_tag_id>/", methods=["DELETE"])
def delete_device_location_tag(device_location_tag_id: int) -> JSONResponse:
    return JSONResponse({"device_location_tag_id": current_app.device_location_tag_store.delete_device_location_tag(device_location_tag_id=device_location_tag_id)})


@DEVICE_LOCATION_TAGS_V0_BLUEPRINT.route("/device-location-tags/backup/", methods=["POST"])
def backup_device_location_tags() -> JSONResponse:
    return JSONResponse({"success": current_app.device_location_tag_store.backup_device_location_tags()})


@DEVICE_LOCATION_TAGS_V0_BLUEPRINT.route("/device-location-tags/load/", methods=["POST"])
def load_device_location_tags() -> JSONResponse:
    return JSONResponse({"success": current_app.device_location_tag_store.load_device_location_tags_from_backup()})
