import json
import logging
import uuid
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from .models import (
    SmartThingsInstallation,
    SmartThingsDevice,
    SmartThingsEvent,
    OAuthState,
)
from .mqtt import publish_event
from .smartthings import SmartThingsClient
from .webhook_verify import verify_request
from django.conf import settings

log = logging.getLogger(__name__)

def health(request):
    return JsonResponse({"status": "ok"})

def _mqtt_topic(device_label, capability, attribute):
    def clean(value):
        value = (value or "unknown").strip()
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in value)
    return "/".join([
        settings.MQTT_TOPIC_PREFIX.strip("/"),
        clean(device_label),
        clean(capability),
        clean(attribute),
    ])

def _handle_confirmation(body):
    confirmation_url = (
        body.get("confirmationData", {}).get("confirmationUrl")
    )
    if confirmation_url:
        import requests
        response = requests.get(confirmation_url, timeout=15)
        response.raise_for_status()
        return JsonResponse({"status": "confirmed"})
    return HttpResponseBadRequest("Missing confirmationUrl")

def _handle_event(body):
    event_data = body.get("eventData", {})
    installed = event_data.get("installedApp", {})
    installed_app_id = installed.get("installedAppId", "")

    for event in event_data.get("events", []):
        event_type = event.get("eventType")

        if event_type == "DEVICE_EVENT":
            device_id = event.get("deviceId", "")
            component = event.get("component", "main")
            capability = event.get("capability", "")
            attribute = event.get("attribute", "")
            value = event.get("value")
            event_time = parse_datetime(event.get("eventTime", ""))

            device, _ = SmartThingsDevice.objects.get_or_create(
                device_id=device_id,
                defaults={"location_id": installed.get("locationId", "")},
            )

            topic = _mqtt_topic(
                device.label or device_id,
                capability,
                attribute,
            )

            payload = {
                "value": value,
                "device_id": device_id,
                "capability": capability,
                "attribute": attribute,
                "component": component,
                "event_time": event.get("eventTime"),
            }

            record = SmartThingsEvent.objects.create(
                event_time=event_time,
                installed_app_id=installed_app_id,
                device_id=device_id,
                component=component,
                capability=capability,
                attribute=attribute,
                value=value if isinstance(value, dict) else {"value": value},
                raw=event,
                mqtt_topic=topic,
            )

            try:
                publish_event(topic, payload)
                record.mqtt_published = True
                record.save(update_fields=["mqtt_published"])
            except Exception as exc:
                record.mqtt_error = str(exc)
                record.save(update_fields=["mqtt_error"])
                log.exception("MQTT publish failed for %s", topic)

        elif event_type == "INSTALLED_APP_LIFECYCLE_EVENT":
            lifecycle = event.get("installedAppLifecycleEvent", {})
            if lifecycle.get("lifecycle") == "DELETE":
                SmartThingsInstallation.objects.filter(
                    installed_app_id=lifecycle.get("installedAppId", "")
                ).delete()

    return JsonResponse({})

def _handle_lifecycle(body):
    # Current SmartThings webhook lifecycle events are handled in _handle_event.
    return JsonResponse({})

@csrf_exempt
def smartthings_webhook(request):
    if request.method != "POST":
        return JsonResponse({"service": "smartthings-mqtt-bridge"})

    raw_body = request.body

    if not verify_request(request, raw_body):
        return HttpResponse(status=401)

    try:
        body = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid JSON")

    message_type = body.get("messageType")

    if message_type == "CONFIRMATION":
        return _handle_confirmation(body)

    if message_type == "EVENT":
        return _handle_event(body)

    return JsonResponse({})

def oauth_callback(request):
    error = request.GET.get("error")
    if error:
        return JsonResponse(
            {
                "error": error,
                "description": request.GET.get("error_description", ""),
            },
            status=400,
        )

    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code or not state:
        return JsonResponse(
            {"error": "missing code/state"},
            status=400,
        )

    try:
        OAuthState.objects.get(state=state)
    except OAuthState.DoesNotExist:
        return JsonResponse({"error": "invalid state"}, status=400)

    client = SmartThingsClient()
    token_data = client.exchange_code(code)

    # The exact installedAppId/locationId association is completed when the
    # API Access App registration and install flow are available.
    OAuthState.objects.filter(state=state).delete()

    return JsonResponse({
        "status": "authorization_received",
        "expires_in": token_data.get("expires_in"),
    })
