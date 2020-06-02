from flask import Blueprint, current_app, request
from flagon.responses import JSONResponse

METRICS_V0_BLUEPRINT = Blueprint(name="v0_metrics", import_name=__name__)


@METRICS_V0_BLUEPRINT.route("/metrics/", methods=["POST"])
def create_metric() -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "metric": current_app.metric_store.create_metric(
            name=request_data["name"],
            abbreviation=request_data["abbreviation"],
            value_type=request_data["value_type"],
            unit=request_data.get("unit", None),
        )
    })


@METRICS_V0_BLUEPRINT.route("/metrics/<int:metric_id>/", methods=["GET"])
def get_metric(metric_id: int) -> JSONResponse:
    return JSONResponse({
        "metric": current_app.metric_store.get_metric(
            metric_id=metric_id,
            fields=set(request.args.getlist("fields")),
        )
    })


@METRICS_V0_BLUEPRINT.route("/metrics/<string:name>/", methods=["GET"])
def get_metric_by_name(name: str) -> JSONResponse:
    return JSONResponse({
        "metric": current_app.metric_store.get_metric_by_name(
            name=name,
            fields=set(request.args.getlist("fields")),
        )
    })


@METRICS_V0_BLUEPRINT.route("/metrics/abbreviation/<string:abbreviation>/", methods=["GET"])
def get_metric_by_abbreviation(abbreviation: str) -> JSONResponse:
    return JSONResponse({
        "metric": current_app.metric_store.get_metric_by_abbreviation(
            abbreviation=abbreviation,
            fields=set(request.args.getlist("fields")),
        )
    })


@METRICS_V0_BLUEPRINT.route("/metrics/", methods=["GET"])
def get_metrics() -> JSONResponse:
    return JSONResponse({
        "metrics": current_app.metric_store.get_metrics(
            fields=set(request.args.getlist("fields")),
            metric_id=set(request.args.getlist("metric_id")),
            name=set(request.args.getlist("name")),
            abbreviation=set(request.args.getlist("abbreviation")),
            unit=set(request.args.getlist("unit")),
            order_by=request.args.get("order_by", None),
            order_by_direction=request.args.get("order_by_direction", None),
        )
    })


@METRICS_V0_BLUEPRINT.route("/metrics/<int:metric_id>/", methods=["PATCH"])
def update_metric(metric_id: int) -> JSONResponse:
    request_data = request.get_json()
    return JSONResponse({
        "metric": current_app.metric_store.update_metric(
            metric_id=metric_id,
            name=request_data.get("name", None),
            abbreviation=request_data.get("abbreviation", None),
            value_type=request_data.get("value_type", None),
            unit=request_data.get("unit", None),
        )
    })


@METRICS_V0_BLUEPRINT.route("/metrics/<int:metric_id>/", methods=["DELETE"])
def delete_metric(metric_id: int) -> JSONResponse:
    return JSONResponse({"metric_id": current_app.metric_store.delete_metric(metric_id=metric_id)})


@METRICS_V0_BLUEPRINT.route("/metrics/backup/", methods=["POST"])
def backup_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.metric_store.backup_metrics()})


@METRICS_V0_BLUEPRINT.route("/metrics/load/", methods=["POST"])
def load_metrics() -> JSONResponse:
    return JSONResponse({"success": current_app.metric_store.load_metrics_from_backup()})
