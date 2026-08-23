# Deployment notes

Expected public endpoint:

    https://smartthingsbridge.ostertage.de/

Django listens on:

    127.0.0.1:8080

Put your existing reverse proxy in front of it and terminate TLS there.

The MQTT broker can remain in the private network as long as the bridge host can
route to it directly.

Before production:
- set a strong DJANGO_SECRET_KEY
- set DEBUG=0
- configure ALLOWED_HOSTS
- configure MQTT credentials/TLS if needed
- configure the SmartThings OAuth credentials when API Access App registration
  becomes available
- enable production webhook signature verification in bridgeapp/webhook_verify.py
