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

"""Unit tests for configarium.models.python_logging."""

import pytest

from configarium.models.python_logging import LoggerConfig, LoggingConfig


def test_python_logging() -> None:
    """Unit tests for configarium.models.python_logging."""
    config = LoggingConfig.model_validate({})
    assert isinstance(config, LoggingConfig)


def test_invalid_root_log_level() -> None:
    """Test an invalid root log level."""
    with pytest.raises(ValueError, match="Unknown logging level: broken"):
        LoggingConfig.model_validate({
            "logger_name": "test",
            "log_level": "broken",
        })


def test_invalid_log_level() -> None:
    """Test an invalid logger log level."""
    with pytest.raises(ValueError, match="Unknown logging level: broken"):
        LoggerConfig.model_validate({
            "logger_name": "test",
            "log_level": "broken",
        })


def test_invalid_date_format() -> None:
    """Test and invalid date_format."""
    with pytest.raises(ValueError, match="Invalid date format: '%q'"):
        LoggingConfig.model_validate({
            "logger_name": "test",
            "date_format": "%q",
        })
