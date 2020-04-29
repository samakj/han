import logging
import math
import os
from typing import Optional, Union

from flask import Flask, Response, redirect, request
from werkzeug.exceptions import HTTPException

from han_flask.converters.datetime_converter import DatetimeConverter
from han_flask.converters.int_list_converter import IntListConverter
from han_flask.converters.int_set_converter import IntSetConverter
from han_flask.converters.str_list_converter import StrListConverter
from han_flask.converters.str_set_converter import StrSetConverter
from han_flask.exceptions import APIError
from han_flask.requests import JSONRequest
from han_flask.responses import JSONResponse
from han_flask.routes import BLUEPRINT as DEFAULT_ROUTES_BLUEPRINT

log = logging.getLogger(__name__)


def generate_request_id(length: int = 8) -> str:
    return os.urandom(math.ceil(length / 2)).hex()[:length]


def before_request() -> None:
    url_split = request.url.split("?")
    path_split = url_split[0].split("/")

    if path_split[-1] and "." not in path_split[-1]:
        url_split[0] += "/"
        return redirect("?".join(url_split), 308)


def after_request(response: Response) -> Response:
    return response


def handle_api_error(error: APIError) -> Response:
    log.exception(error)
    return generate_error_response(error)


def handle_http_error(error: HTTPException) -> Response:
    log.exception(error)
    return generate_error_response(APIError(status_code=error.code))


def handle_generic_error(error: Exception) -> Union[Response, Exception]:
    log.exception(error)
    for error_type in [APIError, HTTPException]:
        if isinstance(error, error_type):
            return error

    return generate_error_response(APIError(status_code=500))


def generate_error_response(error: APIError) -> Response:
    response = JSONResponse(error.data)
    response.status_code = error.status_code
    response.headers.add("Error-Type", error.error_type)
    response.headers.add("Cache-Control", "no-cache")

    return response


class HanFlask(Flask):

    request_class = JSONRequest

    def __init__(self, name: str, static_folder: Optional[str] = None):
        super().__init__(name, static_folder=static_folder)

        # Before Request Handlers
        self.before_request(before_request)
        # After Request Handlers
        self.after_request(after_request)
        # URL Converters
        self.url_map.converters["datetime"] = DatetimeConverter
        self.url_map.converters["int_list"] = IntListConverter
        self.url_map.converters["int_set"] = IntSetConverter
        self.url_map.converters["str_list"] = StrListConverter
        self.url_map.converters["str_set"] = StrSetConverter
        # Default Routes
        self.register_blueprint(blueprint=DEFAULT_ROUTES_BLUEPRINT, url_prefix="/v0")
        # Error Handers
        self.register_error_handler(APIError, handle_api_error)
        self.register_error_handler(HTTPException, handle_http_error)
        self.register_error_handler(Exception, handle_generic_error)
