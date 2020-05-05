from flask import Blueprint, current_app, request
from han_flask.responses import JSONResponse

MOTION_VALUES_V0_BLUEPRINT = Blueprint(name="v0_motion_values", import_name=__name__)


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/", methods=["POST"])
def create_motion_value() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "motion_value": current_app.motion_value_creation_handler.create_motion_value(
            report_id=request_data["report_id"],
            value=request_data["value"],
        )
    })


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/<int:motion_value_id>/", methods=["GET"])
def get_motion_value(motion_value_id: int) -> JSONResponse:
    return JSONResponse({
        "motion_value": current_app.motion_value_store.get_motion_value(
            motion_value_id=motion_value_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/<int:report_id>/", methods=["GET"])
def get_motion_value_by_report_id(report_id: int) -> JSONResponse:
    return JSONResponse({
        "motion_value": current_app.motion_value_store.get_motion_value_by_report_id(
            report_id=report_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/", methods=["GET"])
def get_motion_values() -> JSONResponse:
    return JSONResponse({
        "motion_values": current_app.motion_value_store.get_motion_value(
            fields=set(request.args.getlist("fields")),
            motion_value_id=set(request.args.getlist("motion_value_id")),
            report_id=set(request.args.getlist("report_id")),
            value=bool(request.args["value"]) if request.args.get("value", None) is not None else None,
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
            limit=int(request.args["limit"]) if request.args.get("limit", None) is not None else None,
        )
    })


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/<int:motion_value_id>/", methods=["PATCH"])
def update_motion_value(motion_value_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "motion_value": current_app.motion_value_creation_handler.update_motion_value(
            motion_value_id=motion_value_id,
            report_id=request_data.get("report_id", None),
            value=request_data.get("value", None),
        )
    })


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/<int:motion_value_id>/", methods=["DELETE"])
def delete_motion_value(motion_value_id: int) -> JSONResponse:
    return JSONResponse({
        "motion_value_id": current_app.motion_value_creation_handler.delete_motion_value(
            motion_value_id=motion_value_id,
        )
    })


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/backup/", methods=["POST"])
def backup_motion_values() -> JSONResponse:
    return JSONResponse({"success": current_app.motion_value_store.backup_motion_values()})


@MOTION_VALUES_V0_BLUEPRINT.route("/motion-value/load/", methods=["POST"])
def load_motion_values() -> JSONResponse:
    return JSONResponse({"success": current_app.motion_value_store.load_motion_values_from_backup()})
