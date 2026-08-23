import json
import ssl
import paho.mqtt.client as mqtt
from django.conf import settings

def publish_event(topic, payload):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    if settings.MQTT_USERNAME:
        client.username_pw_set(
            settings.MQTT_USERNAME,
            settings.MQTT_PASSWORD,
        )

    if settings.MQTT_TLS:
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

    client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)
    result = client.publish(
        topic,
        json.dumps(payload, ensure_ascii=False),
        qos=1,
        retain=False,
    )
    result.wait_for_publish()
    client.disconnect()

    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        raise RuntimeError(f"MQTT publish failed with rc={result.rc}")
