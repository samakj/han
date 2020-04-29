import random
import re
import warnings
from functools import wraps
from typing import Dict  # noqa pylint: disable=unused-import
from typing import Any, Callable, List, Optional

from fastjsonschema import JsonSchemaException
from fastjsonschema import compile as compile_schema
from fastjsonschema.draft04 import CodeGeneratorDraft04
from fastjsonschema.draft06 import CodeGeneratorDraft06
from fastjsonschema.draft07 import CodeGeneratorDraft07
from fastjsonschema.generator import CodeGenerator, enforce_list
from flask import current_app, request
from werkzeug.datastructures import MultiDict

from han_flask.exceptions import APIError
from han_flask.responses import JSONResponse


def generate_format(self: CodeGenerator) -> None:
    self.fastjsonschema_generate_format()
    if self._definition["format"].startswith(
        "date-time"
    ):  # pylint: disable=protected-access
        self.l("from dateutil.parser import parse")
        with self.l("try:"):
            with self.l("if {variable}:"):
                self.l("parse({variable})")
        with self.l("except Exception:"):
            self.l('raise JsonSchemaException("{name} must be a valid date-time")')


def generate_type(self: CodeGenerator) -> None:
    self.fastjsonschema_generate_type()
    types = enforce_list(self._definition["type"])  # pylint: disable=protected-access
    if "string" in types:
        if (
            "_NO_BAD_CHARS" not in self._compile_regexps
        ):  # pylint: disable=protected-access
            self._compile_regexps[
                "_NO_BAD_CHARS"
            ] = re.compile(  # pylint: disable=protected-access
                "[\x00\uD800-\uDFFF]"
            )
        with self.l(
            'if isinstance({variable}, str) and REGEX_PATTERNS["_NO_BAD_CHARS"].search({variable}):'
        ):
            self.l(
                'raise JsonSchemaException("{name} cannot contain NULL or unpaired surrogate characters")'
            )


def patch_fastjsonschema_regex(code_generators: List[CodeGenerator]) -> None:
    for code_generator_cls in code_generators:
        code_generator_cls.FORMAT_REGEXS["date-time-like"] = (
            r"^[0-9]{4}-[01][0-9]-[0-3][0-9]"
            r"((T|\s)[0-2][0-9]:[0-5][0-9]:[0-5][0-9](?:\.[0-9]+)?(?:[+-][0-2][0-9]:[0-5][0-9]|Z)?)?$"
        )
        code_generator_cls.FORMAT_REGEXS["ip"] = "({}|{})".format(
            code_generator_cls.FORMAT_REGEXS["ipv4"],
            code_generator_cls.FORMAT_REGEXS["ipv6"],
        )
        code_generator_cls.fastjsonschema_generate_format = (
            code_generator_cls.generate_format
        )
        code_generator_cls.fastjsonschema_generate_type = code_generator_cls.generate_type
    for code_generator_cls in code_generators:
        code_generator_cls.generate_format = generate_format
        code_generator_cls.generate_type = generate_type


patch_fastjsonschema_regex(
    [CodeGeneratorDraft04, CodeGeneratorDraft06, CodeGeneratorDraft07]
)


class RequestValidationError(APIError):
    def __init__(self, message: str) -> None:
        super().__init__(400, "REQUEST_VALIDATION_ERROR", {"message": message})


class ResponseValidationError(Exception):
    """Do not handle this at flask level, this is a programming error."""


class InvalidSchemaError(Exception):
    pass


def _boolean_converter(maybe_bool: str) -> bool:
    lower_bool = maybe_bool.lower()
    if lower_bool == "true":
        return True
    elif lower_bool == "false":
        return False
    else:
        raise ValueError("Boolean must be 'true' or 'false' (ignoring case)")


type_converter = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": _boolean_converter,
}


def _maybe_convert_arg(arg: str, type_: Any) -> Any:
    try:
        return type_(arg)
    except ValueError:
        return arg


def _convert_request_args(request_args: MultiDict, schema: dict) -> dict:
    converted_request_args = {}

    properties = schema.get("properties", {})
    for property_name, property_ in properties.items():
        if property_name in request_args:
            values = request_args.getlist(property_name)
            if property_["type"] == "array":
                type_ = type_converter.get(property_["items"]["type"], str)
                converted = [_maybe_convert_arg(arg, type_) for arg in values]
                converted_request_args[property_name] = converted
            else:
                if len(values) == 1:
                    type_ = type_converter.get(property_["type"], str)
                    converted = _maybe_convert_arg(values[0], type_)
                else:
                    converted = values  # we will fail validation
                converted_request_args[property_name] = converted

    return converted_request_args


schema_definitions = {}  # type: Dict[str, Any]


def _maybe_create_validator(schema: Optional[Dict[str, Any]]) -> Optional[Callable]:
    validator = None
    if schema is not None:
        schema["definitions"] = {**schema_definitions, **schema.get("definitions", {})}
        validator = compile_schema(schema)
    return validator


def validate(  # noqa Flake8: C901
    *,
    request_schema: Optional[dict] = None,
    query_string_schema: Optional[dict] = None,
    response_schema: Optional[dict] = None,
    response_schemas: Optional[Dict[int, dict]] = None,
    response_validation_rate: float = 1.0,
) -> Callable[..., Any]:
    if request_schema is not None and request_schema["type"] != "object":
        raise InvalidSchemaError("Request schemas must be objects")

    if response_validation_rate < 0 or response_validation_rate > 1:
        raise InvalidSchemaError("Invalid response validation rate")

    if query_string_schema is not None:
        if query_string_schema["type"] != "object":
            raise InvalidSchemaError("Query string schemas must be objects")
        if "additionalProperties" in query_string_schema:
            raise InvalidSchemaError(
                '"additionalProperties" is not valid for query string schemas'
            )
        if "required" in query_string_schema:
            raise InvalidSchemaError('"required" is not valid for query string schemas')

    if response_schema is not None and response_schema["type"] != "object":
        warnings.warn("Responses should be within an envelope", FutureWarning)

    if response_schema is not None and response_schemas is not None:
        raise RuntimeError(
            "Define either a single response_schema or multiple response_schemas"
        )

    response_schemas = (
        {200: response_schema} if response_schema is not None else response_schemas
    )

    # NOTE: Validate the schemas once and create validators
    request_schema_validator = _maybe_create_validator(request_schema)
    query_string_schema_validator = _maybe_create_validator(query_string_schema)
    response_schema_validators = {
        http_status_code: _maybe_create_validator(schema)
        for http_status_code, schema in (response_schemas or {}).items()
    }

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Placing the schemas on the route function allow them to be
        # Used to produce documentation.
        func._request_schema = (
            request_schema
        )  # type: ignore # pylint: disable=protected-access
        func._query_string_schema = (
            query_string_schema
        )  # type: ignore # pylint: disable=protected-access
        func._response_schemas = (
            response_schemas
        )  # type: ignore # noqa pylint: disable=protected-access

        @wraps(func)
        def func_wrapper(*args: Any, **kwargs: Any) -> Any:
            if request_schema_validator is not None:
                request_data = request.get_json(
                    cache=True, converted=False
                )  # type: ignore
                if request_data is None:
                    raise RequestValidationError("No json in request")
                try:
                    request_schema_validator(request_data)
                except JsonSchemaException as error:
                    raise RequestValidationError(error.message)

            if (
                query_string_schema is not None
                and query_string_schema_validator is not None
            ):
                converted_args = _convert_request_args(request.args, query_string_schema)
                try:
                    query_string_schema_validator(converted_args)
                except JsonSchemaException as error:
                    raise RequestValidationError(error.message) from error
                else:
                    request.converted_args = converted_args

            response = func(*args, **kwargs)

            enabled = (
                current_app.config.get("ENABLE_RESPONSE_VALIDATION", True)
                or current_app.debug
            )
            response_schema_validator = response_schema_validators.get(
                response.status_code
            )
            should_validate = (
                current_app.debug or random.random() < response_validation_rate
            )
            if enabled and response_schema_validator is not None and should_validate:
                if not isinstance(response, JSONResponse):
                    raise TypeError("Response {} is not a JSONResponse".format(response))
                try:
                    response_schema_validator(response.raw_data)
                except JsonSchemaException as error:
                    raise ResponseValidationError(error.message)
            return response

        return func_wrapper

    return decorator
