from flask import Blueprint, current_app, request
from han_flask.responses import JSONResponse

REPORTS_V0_BLUEPRINT = Blueprint(name="v0_reports", import_name=__name__)


@REPORTS_V0_BLUEPRINT.route("/reports/", methods=["POST"])
def create_report() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "report": current_app.report_creation_handler.create_report(
            device_id=request_data["device_id"],
            value=request_data["value"],
            reported_at=request_data["reported_at"],
            report_metric_id=request_data.get("report_metric_id", None),
            report_metric_name=request_data.get("report_metric_name", None),
            report_metric_abbreviation=request_data.get("report_metric_abbreviation", None),
        )
    })


@REPORTS_V0_BLUEPRINT.route("/reports/<int:report_id>/", methods=["GET"])
def get_report(report_id: int) -> JSONResponse:
    return JSONResponse({
        "report": current_app.report_store.get_report(
            report_id=report_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@REPORTS_V0_BLUEPRINT.route("/reports/", methods=["GET"])
def get_reports() -> JSONResponse:
    return JSONResponse({
        "reports": current_app.report_store.get_report(
            fields=set(request.args.getlist("fields")),
            report_id=set(request.args.getlist("report_id")),
            report_metric_id=set(request.args.getlist("report_metric_id")),
            device_id=set(request.args.getlist("device_id")),
            reported_at_gte=request.args.get("reported_at_gte", None),
            reported_at_lte=request.args.get("reported_at_lte", None),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
            limit=int(request.args["limit"]) if request.args.get("limit", None) is not None else None,
        )
    })


@REPORTS_V0_BLUEPRINT.route("/reports/<int:report_id>/", methods=["PATCH"])
def update_report(report_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "report": current_app.report_creation_handler.update_report(
            report_id=report_id,
            device_id=request_data.get("device_id", None),
            reported_at=request_data.get("reported_at", None),
            report_metric_id=request_data.get("report_metric_id", None),
        )
    })


@REPORTS_V0_BLUEPRINT.route("/reports/<int:report_id>/", methods=["DELETE"])
def delete_report(report_id: int) -> JSONResponse:
    return JSONResponse({
        "report_id": current_app.report_creation_handler.delete_report(
            report_id=report_id,
        )
    })


@REPORTS_V0_BLUEPRINT.route("/reports/backup/", methods=["POST"])
def backup_reports() -> JSONResponse:
    return JSONResponse({"success": current_app.report_store.backup_reports()})


@REPORTS_V0_BLUEPRINT.route("/reports/load/", methods=["POST"])
def load_reports() -> JSONResponse:
    return JSONResponse({"success": current_app.report_store.load_reports_from_backup()})
