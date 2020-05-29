from flask import Blueprint, current_app, request
from flagon.responses import JSONResponse

LOCATION_TAGS_V0_BLUEPRINT = Blueprint(name="v0_location_tags", import_name=__name__)


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/", methods=["POST"])
def create_location_tag() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "location_tag": current_app.location_tag_store.create_location_tag(
            name=request_data["name"],
            level=request_data["level"],
        )
    })


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/<int:location_tag_id>/", methods=["GET"])
def get_location_tag(location_tag_id: int) -> JSONResponse:
    return JSONResponse({
        "location_tag": current_app.location_tag_store.get_location_tag(
            location_tag_id=location_tag_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/<string:name>/", methods=["GET"])
def get_location_tag_by_name(name: str) -> JSONResponse:
    return JSONResponse({
        "location_tag": current_app.location_tag_store.get_location_tag_by_name(
            name=name,
            fields=set(request.args.getlist("fields")),
        )
    })


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/", methods=["GET"])
def get_location_tags() -> JSONResponse:
    return JSONResponse({
        "location_tags": current_app.location_tag_store.get_location_tags(
            fields=set(request.args.getlist("fields")),
            location_tag_id=set(request.args.getlist("location_tag_id")),
            name=set(request.args.getlist("name")),
            level=set(request.args.getlist("level")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/<int:location_tag_id>/", methods=["PATCH"])
def update_location_tag(location_tag_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "location_tag": current_app.location_tag_store.update_location_tag(
            location_tag_id=location_tag_id,
            name=request_data.get("name", None),
            level=request_data.get("level", None),
        )
    })


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/<int:location_tag_id>/", methods=["DELETE"])
def delete_location_tag(location_tag_id: int) -> JSONResponse:
    return JSONResponse({"location_tag_id": current_app.location_tag_store.delete_location_tag(location_tag_id=location_tag_id)})


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/backup/", methods=["POST"])
def backup_location_tags() -> JSONResponse:
    return JSONResponse({"success": current_app.location_tag_store.backup_location_tags()})


@LOCATION_TAGS_V0_BLUEPRINT.route("/location-tags/load/", methods=["POST"])
def load_location_tags() -> JSONResponse:
    return JSONResponse({"success": current_app.location_tag_store.load_location_tags_from_backup()})
