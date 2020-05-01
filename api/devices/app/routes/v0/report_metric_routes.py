from flask import Blueprint, current_app, request
from han_flask.responses import JSONResponse

REPORT_METRICS_V0_BLUEPRINT = Blueprint(name="v0_report_metrics", import_name=__name__)


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/", methods=["POST"])
def create_report_metric() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "report_metric": current_app.report_metric_store.create_report_metric(
            name=request_data["name"],
            abbreviation=request_data["abbreviation"],
            report_value_type=request_data["report_value_type"],
            unit=request_data["unit"],
        )
    })


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/<int:report_metric_id>/", methods=["GET"])
def get_report_metric(report_metric_id: int) -> JSONResponse:
    return JSONResponse({
        "report_metric": current_app.report_metric_store.get_report_metric(
            report_metric_id=report_metric_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/<string:name>/", methods=["GET"])
def get_report_metric_by_name(name: str) -> JSONResponse:
    return JSONResponse({
        "report_metric": current_app.report_metric_store.get_report_metric_by_name(
            name=name,
            fields=set(request.args.getlist("fields")),
        )
    })


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/<string:abbreviation>/", methods=["GET"])
def get_report_metric_by_abbreviation(abbreviation: str) -> JSONResponse:
    return JSONResponse({
        "report_metric": current_app.report_metric_store.get_report_metric_by_abbreviation(
            abbreviation=abbreviation,
            fields=set(request.args.getlist("fields")),
        )
    })


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/", methods=["GET"])
def get_report_metrics() -> JSONResponse:
    return JSONResponse({
        "report_metrics": current_app.report_metric_store.get_report_metrics(
            fields=set(request.args.getlist("fields")),
            report_metric_id=set(request.args.getlist("report_metric_id")),
            name=set(request.args.getlist("name")),
            abbreviation=set(request.args.getlist("abbreviation")),
            report_value_type=set(request.args.getlist("report_value_type")),
            unit=set(request.args.getlist("unit")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/<int:report_metric_id>/", methods=["PATCH"])
def update_report_metric(report_metric_id: int) -> JSONResponse:
    return JSONResponse({"report_metric": current_app.report_metric_store.update_report_metric(report_metric_id=report_metric_id)})


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/<int:report_metric_id>/", methods=["DELETE"])
def delete_report_metric(report_metric_id: int) -> JSONResponse:
    return JSONResponse({"report_metric_id": current_app.report_metric_store.delete_report_metric(report_metric_id=report_metric_id)})


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/backup/", methods=["POST"])
def backup_report_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.report_metric_store.backup_report_metrics()})


@REPORT_METRICS_V0_BLUEPRINT.route("/report-metrics/load/", methods=["POST"])
def load_report_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.report_metric_store.load_report_metrics_from_backup()})
