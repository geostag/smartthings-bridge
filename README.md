# smartthings-bridge
small service to bridge from samsung smartthings to my smart home universe

Django-based bridge for:

SmartThings -> HTTPS webhook -> Django -> MQTT

The project is intentionally prepared for the new SmartThings API Access App / Service
Integration flow. SmartThings API Access App registration is currently not yet available
in the Developer Console, so the SmartThings OAuth/subscription integration is isolated
behind a small client module and can be enabled when Samsung exposes the registration.

## Current functionality

- Django backend
- SQLite persistence
- MQTT publishing via paho-mqtt
- `/health/` health endpoint
- `/` webhook endpoint
- SmartThings `CONFIRMATION` handling
- SmartThings `EVENT` handling
- SmartThings uninstall lifecycle cleanup
- OAuth callback endpoint placeholder
- device/event logging in the database
- generic capability -> MQTT topic mapping
- Docker / docker-compose deployment

## MQTT topic format

By default:

    smartthings/<device_label>/<capability>/<attribute>

Example:

    smartthings/Wohnzimmer_Lampe/switch/switch

Payload:

    {
      "value": "on",
      "device_id": "...",
      "capability": "switch",
      "attribute": "switch",
      "component": "main",
      "event_time": "2026-08-23T15:00:00Z"
    }

The bridge publishes JSON by default.

## Important SmartThings status

Samsung's current documentation describes API Access Apps / Service Integrations as
the replacement path for SmartApp-style cloud integrations. The public documentation
currently states that API Access App registration is "coming soon". Until the
registration is available in your Developer Console, this project can be deployed
and tested locally, but you cannot complete the final SmartThings OAuth/subscription
connection.

## Configuration

Copy `.env.example` to `.env` and adjust:

    DJANGO_SECRET_KEY=change-me
    DJANGO_DEBUG=0
    DJANGO_ALLOWED_HOSTS=smartthingsbridge.ostertage.de,localhost,127.0.0.1

    PUBLIC_BASE_URL=https://smartthingsbridge.ostertage.de

    MQTT_HOST=192.168.1.10
    MQTT_PORT=1883
    MQTT_USERNAME=
    MQTT_PASSWORD=
    MQTT_TOPIC_PREFIX=smartthings

SmartThings settings are already included for the future API Access App:

    SMARTTHINGS_API_BASE_URL=https://api.smartthings.com/v1
    SMARTTHINGS_CLIENT_ID=
    SMARTTHINGS_CLIENT_SECRET=
    SMARTTHINGS_REDIRECT_URI=https://smartthingsbridge.ostertage.de/oauth/callback

Do not commit `.env`.

## Run with Docker

    cp .env.example .env
    docker compose up -d --build

Check:

    curl https://smartthingsbridge.ostertage.de/health/

Expected:

    {"status":"ok"}

## Reverse proxy

Expose Django through your existing reverse proxy:

    https://smartthingsbridge.ostertage.de

Proxy to:

    http://127.0.0.1:8080

TLS should terminate at the reverse proxy.

## Local development

    python -m venv .venv
    .venv\Scripts\activate       # Windows
    source .venv/bin/activate    # Linux/macOS
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8080

## Testing MQTT without SmartThings

You can send a synthetic SmartThings-style event:

    curl -X POST http://localhost:8080/ \
      -H "Content-Type: application/json" \
      -d @tests/sample_event.json

The webhook will publish the event to MQTT. In production, SmartThings webhook
signatures must be validated before accepting events; the verification module is
already separated so it can be enabled/configured against Samsung's signing keys.

## Next step when API Access App registration becomes available

1. Register an API Access App in SmartThings Developer Console.
2. Set Target URL to:
       https://smartthingsbridge.ostertage.de/
3. Set OAuth callback to:
       https://smartthingsbridge.ostertage.de/oauth/callback
4. Grant the least-privileged device read scope needed.
5. Put the resulting Client ID/Client Secret in `.env`.
6. Complete OAuth.
7. Use the SmartThings client to discover devices and create subscriptions.
