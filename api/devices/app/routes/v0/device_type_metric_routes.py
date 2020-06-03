from flask import Blueprint, current_app, request
from flagon.responses import JSONResponse
from flagon.request_args import arg_to_bool

DEVICE_TYPE_METRICS_V0_BLUEPRINT = Blueprint(name="v0_device_type_metrics", import_name=__name__)


@DEVICE_TYPE_METRICS_V0_BLUEPRINT.route("/device-type-metrics/", methods=["POST"])
def create_device_type_metric() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device_type_metric": current_app.device_type_metric_store.create_device_type_metric(
            device_type_id=request_data["device_type_id"],
            metric_id=request_data["metric_id"],
            reportable=request_data["reportable"],
            commandable=request_data["commandable"],
        )
    })


@DEVICE_TYPE_METRICS_V0_BLUEPRINT.route("/device-type-metrics/<int:device_type_metric_id>/", methods=["GET"])
def get_device_type_metric(device_type_metric_id: int) -> JSONResponse:
    return JSONResponse({
        "device_type_metric": current_app.device_type_metric_store.get_device_type_metric(
            device_type_metric_id=device_type_metric_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@DEVICE_TYPE_METRICS_V0_BLUEPRINT.route("/device-type-metrics/", methods=["GET"])
def get_device_type_metrics() -> JSONResponse:
    return JSONResponse({
        "device_type_metrics": current_app.device_type_metric_store.get_device_type_metrics(
            fields=set(request.args.getlist("fields")),
            device_type_metric_id=set(request.args.getlist("device_type_metric_id")),
            device_type_id=set(request.args.getlist("device_id")),
            metric_id=set(request.args.getlist("metric_id")),
            reportable=arg_to_bool(request.args.get("reportable", None), None),
            commandable=arg_to_bool(request.args.get("commandable", None), None),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@DEVICE_TYPE_METRICS_V0_BLUEPRINT.route("/device-type-metrics/<int:device_type_metric_id>/", methods=["PATCH"])
def update_device_type_metric(device_type_metric_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device_type_metric": current_app.device_type_metric_store.update_device_type_metric(
            device_type_metric_id=device_type_metric_id,
            device_type_id=request_data.get("device_id", None),
            metric_id=request_data.get("metric_id", None),
            reportable=request_data.get("reportable", None),
            commandable=request_data.get("commandable", None),
        )
    })


@DEVICE_TYPE_METRICS_V0_BLUEPRINT.route("/device-type-metrics/<int:device_type_metric_id>/", methods=["DELETE"])
def delete_device_type_metric(device_type_metric_id: int) -> JSONResponse:
    return JSONResponse({"device_type_metric_id": current_app.device_type_metric_store.delete_device_type_metric(device_type_metric_id=device_type_metric_id)})


@DEVICE_TYPE_METRICS_V0_BLUEPRINT.route("/device-type-metrics/backup/", methods=["POST"])
def backup_device_type_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.device_type_metric_store.backup_device_type_metrics()})


@DEVICE_TYPE_METRICS_V0_BLUEPRINT.route("/device-type-metrics/load/", methods=["POST"])
def load_device_type_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.device_type_metric_store.load_device_type_metrics_from_backup()})
