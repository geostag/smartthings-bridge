from django.urls import path
from bridgeapp import views

urlpatterns = [
    path("", views.smartthings_webhook, name="smartthings-webhook"),
    path("health/", views.health, name="health"),
    path("oauth/callback", views.oauth_callback, name="oauth-callback"),
]
