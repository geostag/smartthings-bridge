import base64
import hashlib
import json
from urllib.parse import urlencode
import requests
from django.conf import settings

class SmartThingsClient:
    """
    Thin client for the current SmartThings API Access App API.

    Registration is currently unavailable in the public Developer Console.
    Once SmartThings exposes API Access App registration, configure CLIENT_ID,
    CLIENT_SECRET and REDIRECT_URI and use this client for OAuth and subscriptions.
    """

    def authorization_url(self, state, scopes):
        params = {
            "client_id": settings.SMARTTHINGS_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": settings.SMARTTHINGS_REDIRECT_URI,
            "scope": " ".join(scopes),
            "state": state,
        }
        # SmartThings' current public docs define the OAuth flow, but the final
        # authorization endpoint path may change while API Access Apps roll out.
        # Keep it centralized here.
        return "https://api.smartthings.com/oauth/authorize?" + urlencode(params)

    def exchange_code(self, code):
        url = "https://api.smartthings.com/oauth/token"
        response = requests.post(
            url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.SMARTTHINGS_CLIENT_ID,
                "client_secret": settings.SMARTTHINGS_CLIENT_SECRET,
                "redirect_uri": settings.SMARTTHINGS_REDIRECT_URI,
            },
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def refresh(self, refresh_token):
        url = "https://api.smartthings.com/oauth/token"
        response = requests.post(
            url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.SMARTTHINGS_CLIENT_ID,
                "client_secret": settings.SMARTTHINGS_CLIENT_SECRET,
            },
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def list_devices(self, access_token):
        response = requests.get(
            settings.SMARTTHINGS_API_BASE_URL + "/devices",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def create_capability_subscription(
        self, access_token, installed_app_id, location_id,
        capability, attribute="*", value="*", subscription_name=None,
    ):
        body = {
            "sourceType": "CAPABILITY",
            "capability": {
                "locationId": location_id,
                "capability": capability,
                "attribute": attribute,
                "stateChangeOnly": True,
                "subscriptionName": subscription_name or capability,
                "value": value,
            },
        }
        response = requests.post(
            f"{settings.SMARTTHINGS_API_BASE_URL}/installedapps/"
            f"{installed_app_id}/subscriptions",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=body,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
