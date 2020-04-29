from collections import defaultdict

from flask import Blueprint, current_app

from han_flask.responses import JSONResponse

BLUEPRINT = Blueprint("default_routes", __name__)
DISPLAY_METHODS = {"GET", "PATCH", "POST", "DELETE"}


@BLUEPRINT.route("/", methods=["GET"])
def route_map() -> JSONResponse:
    rules: defaultdict = defaultdict(list)

    for rule in current_app.url_map.iter_rules():
        for method in rule.methods:
            if method in DISPLAY_METHODS:
                rules[method].append(str(rule))

    for method, method_routes in rules.items():
        rules[method] = sorted(
            method_routes, key=lambda method_route: method_route.split("/")
        )

    return JSONResponse(rules)


@BLUEPRINT.route("/ping/", methods=["GET"])
def ping() -> JSONResponse:
    return JSONResponse({"ping": "pong"})
