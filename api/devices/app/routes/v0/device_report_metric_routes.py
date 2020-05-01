from flask import Blueprint, current_app, request
from han_flask.responses import JSONResponse

DEVICE_REPORT_METRICS_V0_BLUEPRINT = Blueprint(name="v0_device_report_metrics", import_name=__name__)


@DEVICE_REPORT_METRICS_V0_BLUEPRINT.route("/device-report-metrics/", methods=["POST"])
def create_device_report_metric() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device_report_metric": current_app.device_report_metric_store.create_device_report_metric(
            device_id=request_data["device_id"],
            report_metric_id=request_data["report_metric_id"],
        )
    })


@DEVICE_REPORT_METRICS_V0_BLUEPRINT.route("/device-report-metrics/<int:device_report_metric_id>/", methods=["GET"])
def get_device_report_metric(device_report_metric_id: int) -> JSONResponse:
    return JSONResponse({
        "device_report_metric": current_app.device_report_metric_store.get_device_report_metric(
            device_report_metric_id=device_report_metric_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@DEVICE_REPORT_METRICS_V0_BLUEPRINT.route("/device-report-metrics/", methods=["GET"])
def get_device_report_metrics() -> JSONResponse:
    return JSONResponse({
        "device_report_metrics": current_app.device_report_metric_store.get_device_report_metrics(
            fields=set(request.args.getlist("fields")),
            device_report_metric_id=set(request.args.getlist("device_report_metric_id")),
            device_id=set(request.args.getlist("device_id")),
            report_metric_id=set(request.args.getlist("report_metric_id")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@DEVICE_REPORT_METRICS_V0_BLUEPRINT.route("/device-report-metrics/<int:device_report_metric_id>/", methods=["PATCH"])
def update_device_report_metric(device_report_metric_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "device_report_metric": current_app.device_report_metric_store.update_device_report_metric(
            device_report_metric_id=device_report_metric_id,
            device_id=request_data.get("device_id", None),
            location_tag_id=request_data.get("location_tag_id", None),
        )
    })


@DEVICE_REPORT_METRICS_V0_BLUEPRINT.route("/device-report-metrics/<int:device_report_metric_id>/", methods=["DELETE"])
def delete_device_report_metric(device_report_metric_id: int) -> JSONResponse:
    return JSONResponse({"device_report_metric_id": current_app.device_report_metric_store.delete_device_report_metric(device_report_metric_id=device_report_metric_id)})


@DEVICE_REPORT_METRICS_V0_BLUEPRINT.route("/device-report-metrics/backup/", methods=["POST"])
def backup_device_report_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.device_report_metric_store.backup_device_report_metrics()})


@DEVICE_REPORT_METRICS_V0_BLUEPRINT.route("/device-report-metrics/load/", methods=["POST"])
def load_device_report_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.device_report_metric_store.load_device_report_metrics_from_backup()})
