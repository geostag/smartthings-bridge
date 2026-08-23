from django.contrib import admin
from .models import SmartThingsInstallation, SmartThingsDevice, SmartThingsEvent, OAuthState

admin.site.register(SmartThingsInstallation)
admin.site.register(SmartThingsDevice)
admin.site.register(SmartThingsEvent)
admin.site.register(OAuthState)
