from flask import Blueprint, request
from han_flask.responses import JSONResponse

USER_V0_BLUEPRINT = Blueprint(name="v0_user", import_name=__name__)

import logging
LOG = logging.getLogger(__name__)


@USER_V0_BLUEPRINT.route("/user/", methods=["POST"])
def user_check() -> JSONResponse:
    LOG.error(f"USER: {request.get_json()}")

    return JSONResponse({
        "Ok": True
    })


@USER_V0_BLUEPRINT.route("/superuser/", methods=["POST"])
def superuser_check() -> JSONResponse:
    LOG.error(f"SUPERUSER: {request.get_json()}")

    return JSONResponse({
        "Ok": True
    })


@USER_V0_BLUEPRINT.route("/acl/", methods=["POST"])
def acl_check() -> JSONResponse:
    LOG.error(f"ACL: {request.get_json()}")

    return JSONResponse({
        "Ok": True
    })
