from flask import Blueprint, current_app, request
from han_flask.responses import JSONResponse

HUMIDITY_VALUES_V0_BLUEPRINT = Blueprint(name="v0_humidity_values", import_name=__name__)


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/", methods=["POST"])
def create_humidity_value() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "humidity_value": current_app.humidity_value_creation_handler.create_humidity_value(
            report_id=request_data["report_id"],
            value=request_data["value"],
        )
    })


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/<int:humidity_value_id>/", methods=["GET"])
def get_humidity_value(humidity_value_id: int) -> JSONResponse:
    return JSONResponse({
        "humidity_value": current_app.humidity_value_store.get_humidity_value(
            humidity_value_id=humidity_value_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/<int:report_id>/", methods=["GET"])
def get_humidity_value_by_report_id(report_id: int) -> JSONResponse:
    return JSONResponse({
        "humidity_value": current_app.humidity_value_store.get_humidity_value_by_report_id(
            report_id=report_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/", methods=["GET"])
def get_humidity_values() -> JSONResponse:
    return JSONResponse({
        "humidity_values": current_app.humidity_value_store.get_humidity_value(
            fields=set(request.args.getlist("fields")),
            humidity_value_id=set(request.args.getlist("humidity_value_id")),
            report_id=set(request.args.getlist("report_id")),
            value_gte=request.args.get("value_gte", None),
            value_lte=request.args.get("value_lte", None),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
            limit=int(request.args["limit"]) if request.args.get("limit", None) is not None else None,
        )
    })


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/<int:humidity_value_id>/", methods=["PATCH"])
def update_humidity_value(humidity_value_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "humidity_value": current_app.humidity_value_creation_handler.update_humidity_value(
            humidity_value_id=humidity_value_id,
            report_id=request_data.get("report_id", None),
            value=request_data.get("value", None),
        )
    })


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/<int:humidity_value_id>/", methods=["DELETE"])
def delete_humidity_value(humidity_value_id: int) -> JSONResponse:
    return JSONResponse({
        "humidity_value_id": current_app.humidity_value_creation_handler.delete_humidity_value(
            humidity_value_id=humidity_value_id,
        )
    })


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/backup/", methods=["POST"])
def backup_humidity_values() -> JSONResponse:
    return JSONResponse({"success": current_app.humidity_value_store.backup_humidity_values()})


@HUMIDITY_VALUES_V0_BLUEPRINT.route("/humidity-value/load/", methods=["POST"])
def load_humidity_values() -> JSONResponse:
    return JSONResponse({"success": current_app.humidity_value_store.load_humidity_values_from_backup()})
