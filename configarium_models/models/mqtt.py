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

"""Pydantic models for MQTT."""

from typing import Literal

from pydantic import BaseModel, Field


class MQTTConnectionModel(BaseModel):
    """A pydantic model representing a MQTT connection."""

    host: str = Field(
        default="localhost",
        description="The MQTT server hostname.")

    port: int = Field(
        default=1883,
        description="The MQTT server port.")

    username: str | None = Field(
        default=None,
        description="The username to use for the MQTT connection.")

    password: str | None = Field(
        default=None,
        description="The password to use for the MQTT connection.")

    ssl: bool = Field(
        default=False,
        description="Whether or not to use SSL.")

    ssl_verify: bool = Field(
        default=True,
        description="Whether or not to use verify the SSL certificates.")

    client_id: str | None = Field(
        default=None,
        description="The MQTT client ID to use.")

    keepalive: int = Field(
        default=60,
        description="The MQTT keep-alive interval.")

    clean_session: bool = Field(
        default=True,
        description="Do we use a clean MQTT connection")

    transport: Literal["tcp", "websockets"] = Field(
        default="tcp",
        description="The MQTT transport to use.")

    websocket_path: str = Field(
        default="/mqtt/",
        description="The MQTT websocket path, when transport==websockets.")
