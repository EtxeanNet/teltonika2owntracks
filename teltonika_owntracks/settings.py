"""Configuration module."""
import os
import logging

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

from .__init__ import __version__, NAME

HOSTNAME = os.getenv("HOSTNAME")

class Settings(BaseSettings):
    """Application settings for the Teltonika to OwnTracks listener."""

    hostname: str = Field(NAME, alias='HOSTNAME')
    loglevel: str = Field('INFO', alias='LOGLEVEL')
    update_interval: int = Field(30, alias='UPDATE_INTERVAL')
    
    listen_host: str = Field("0.0.0.0", alias='LISTEN_HOST')
    listen_port: int = Field(8500, alias='LISTEN_PORT')
    device_id: str = Field('teltonika', alias='DEVICE_ID')

    mqtt_host: str | None = Field(None, alias='MQTT_HOST')
    mqtt_port: int = Field(1883, alias='MQTT_PORT')
    mqtt_username: str | None = Field(None, alias='MQTT_USERNAME')
    mqtt_password: str | None = Field(None, alias='MQTT_PASSWORD')
    mqtt_client: str = Field(f"{NAME}-{HOSTNAME}", alias='MQTT_CLIENT')

    detector_history: int = Field(60, alias='DETECTOR_HISTORY')
    detector_limit: int = Field(25, alias='DETECTOR_LIMIT')
