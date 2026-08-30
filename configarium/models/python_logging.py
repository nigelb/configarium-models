# Pydantic models for common application configuration.
# Copyright (C) 2026 NigelB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A pydantic model to configure Python's Logging module."""

import logging
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, field_validator

def_fmt = (
    "%(asctime)-15s %(process)-8d %(levelname)-7s %(name)s %(filename)s"
    ":%(funcName)s:%(lineno)d - %(message)s"
)

debug_def_fmt = (
    '%(asctime)-15s %(process)-8d %(levelname)-7s %(name)s File '
    '"%(pathname)s", line %(lineno)d, in %(funcName)s - %(message)s'
)


class LoggerConfig(BaseModel):
    """Configuration for a specific Logger in Pythons's Logging module."""

    logger_name: str = Field()
    log_level: str = Field()

    @field_validator("log_level")
    @classmethod
    def validate_style(cls, value: str) -> str:
        """Validate that level is a valid Log Level."""
        if value.upper() not in logging._nameToLevel: # noqa: SLF001 getLevelNamesMapping not until python3.12
            msg = f"Unknown logging level: {value}"
            raise ValueError(msg)
        return value.upper()


class LoggerFormatStyle(str, Enum):
    """
    The logger format style to use in the logging format.

    See the style field of: https://docs.python.org/3/library/logging.html#formatter-objects
    """

    PRINTF   = "%" # https://docs.python.org/3/library/stdtypes.html#old-string-formatting
    FORMAT   = "{" # https://docs.python.org/3/library/stdtypes.html#str.format
    TEMPLATE = "$"# https://docs.python.org/3/library/string.html#string.Template


class LoggingConfig(BaseModel):
    """
    Configuration for Pythons's Logging module's basicConfig.

    https://docs.python.org/3/library/logging.html#formatter-objects
    """

    format: str = Field(
        description="The format string used to ",
        default=def_fmt) # See https://docs.python.org/3/library/logging.html#logrecord-attributes

    style: LoggerFormatStyle = Field(
                                description="Logging format style used in the format string.",
                                default=LoggerFormatStyle.PRINTF)

    log_level: str = Field(
        description="The log level of the root logger",
        default=logging.getLevelName(logging.INFO),
    )

    date_format: str | None = Field(
        description=(
            "The date format to use. If None you get a ISO8601-like"
            " (or RFC 3339-like) format"),
        default=None,
    )

    filename: str | None = Field(
        description=(
            "a FileHandler will be created instead of a StreamHandler."
            " Using the specified filename."),
        default=None,
    )

    filemode: str = Field(
        description="If filename is specified, the is the mode in which the file is opened.",
        default="a",
    )

    logger_configs: list[LoggerConfig] = Field(
        description="A list of logger configurations",
        default_factory=list,
    )

    @field_validator("date_format")
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        """Validate that date_format is a valid date_format."""
        if value is not None:
            try:
                datetime.now(tz=timezone.utc).strftime(value)
            except (ValueError, TypeError) as exc:
                msg = f"Invalid date format: {value!r}"
                raise ValueError(msg) from exc
        return value

    @field_validator("log_level")
    @classmethod
    def validate_style(cls, value: str) -> str:
        """Validate that log_level is a valid Log Level."""
        if value.upper() not in logging._nameToLevel: # noqa: SLF001 getLevelNamesMapping not until python3.12
            msg = f"Unknown logging level: {value}"
            raise ValueError(msg)
        return value.upper()
