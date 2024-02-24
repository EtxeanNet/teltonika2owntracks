import logging
import paho.mqtt.client as mqtt
from pynmeagps import NMEAMessage

from .owntracks_message import OwnTracksMessage
from .settings import Settings

logger = logging.getLogger(__name__)

class OwnTracksPublisher:
    
    def __init__(self, settings: Settings):
        self._has_published = False
        self._topic = f'owntracks/{settings.mqtt_username}/{settings.device_id}'
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        if settings.mqtt_username:
            client.username_pw_set(username=settings.mqtt_username, password=settings.mqtt_password)

        if settings.mqtt_port == 8883:
            client.tls_set()
        client.connect(host=settings.mqtt_host, 
                    port=settings.mqtt_port,
                    keepalive=60)

        client.loop_start()
        self._client = client

    async def publish(self, ot_msg: OwnTracksMessage):
        payload = ot_msg.to_mqtt_payload()
        self._client.publish(self._topic, payload, retain=True)
        self._has_published = True

    def has_published(self):
        return self._has_published

    # The callback for when the client receives a CONNACK response from the server.
    def _on_connect(self, client: mqtt.Client, userdata, flags, reason_code, properties):
        logger.info(f"Connected to MQTT broker with result code {reason_code}")
        client.subscribe(self._topic)

    # The callback for when a PUBLISH message is received from the server.
    def _on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        logger.debug(f"message: {msg.topic} {msg.payload}")