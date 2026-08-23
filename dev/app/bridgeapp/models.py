from django.db import models

class SmartThingsInstallation(models.Model):
    installed_app_id = models.CharField(max_length=128, unique=True)
    location_id = models.CharField(max_length=128, blank=True)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    access_token_expires_at = models.DateTimeField(null=True, blank=True)
    refresh_token_expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.installed_app_id

class SmartThingsDevice(models.Model):
    device_id = models.CharField(max_length=128, unique=True)
    label = models.CharField(max_length=255, blank=True)
    location_id = models.CharField(max_length=128, blank=True)
    raw = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mqtt_label(self):
        value = (self.label or self.device_id).strip()
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in value)

class SmartThingsEvent(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    event_time = models.DateTimeField(null=True, blank=True)
    installed_app_id = models.CharField(max_length=128, blank=True)
    device_id = models.CharField(max_length=128, blank=True)
    component = models.CharField(max_length=128, blank=True)
    capability = models.CharField(max_length=128, blank=True)
    attribute = models.CharField(max_length=128, blank=True)
    value = models.JSONField(default=dict, blank=True)
    raw = models.JSONField(default=dict, blank=True)
    mqtt_topic = models.CharField(max_length=512, blank=True)
    mqtt_published = models.BooleanField(default=False)
    mqtt_error = models.TextField(blank=True)

class OAuthState(models.Model):
    state = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
