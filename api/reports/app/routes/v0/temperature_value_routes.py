from flask import Blueprint, current_app, request
from flagon.responses import JSONResponse

TEMPERATURE_VALUES_V0_BLUEPRINT = Blueprint(name="v0_temperature_values", import_name=__name__)


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/", methods=["POST"])
def create_temperature_value() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "temperature_value": current_app.temperature_value_creation_handler.create_temperature_value(
            report_id=request_data["report_id"],
            value=request_data["value"],
        )
    })


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/<int:temperature_value_id>/", methods=["GET"])
def get_temperature_value(temperature_value_id: int) -> JSONResponse:
    return JSONResponse({
        "temperature_value": current_app.temperature_value_store.get_temperature_value(
            temperature_value_id=temperature_value_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/<int:report_id>/", methods=["GET"])
def get_temperature_value_by_report_id(report_id: int) -> JSONResponse:
    return JSONResponse({
        "temperature_value": current_app.temperature_value_store.get_temperature_value_by_report_id(
            report_id=report_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/", methods=["GET"])
def get_temperature_values() -> JSONResponse:
    return JSONResponse({
        "temperature_values": current_app.temperature_value_store.get_temperature_value(
            fields=set(request.args.getlist("fields")),
            temperature_value_id=set(request.args.getlist("temperature_value_id")),
            report_id=set(request.args.getlist("report_id")),
            value_gte=request.args.get("value_gte", None),
            value_lte=request.args.get("value_lte", None),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
            limit=int(request.args["limit"]) if request.args.get("limit", None) is not None else None,
        )
    })


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/<int:temperature_value_id>/", methods=["PATCH"])
def update_temperature_value(temperature_value_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "temperature_value": current_app.temperature_value_creation_handler.update_temperature_value(
            temperature_value_id=temperature_value_id,
            report_id=request_data.get("report_id", None),
            value=request_data.get("value", None),
        )
    })


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/<int:temperature_value_id>/", methods=["DELETE"])
def delete_temperature_value(temperature_value_id: int) -> JSONResponse:
    return JSONResponse({
        "temperature_value_id": current_app.temperature_value_creation_handler.delete_temperature_value(
            temperature_value_id=temperature_value_id,
        )
    })


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/backup/", methods=["POST"])
def backup_temperature_values() -> JSONResponse:
    return JSONResponse({"success": current_app.temperature_value_store.backup_temperature_values()})


@TEMPERATURE_VALUES_V0_BLUEPRINT.route("/temperature-value/load/", methods=["POST"])
def load_temperature_values() -> JSONResponse:
    return JSONResponse({"success": current_app.temperature_value_store.load_temperature_values_from_backup()})
