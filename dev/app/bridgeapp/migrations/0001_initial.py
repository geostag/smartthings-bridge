from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OAuthState",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("state", models.CharField(max_length=128, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="SmartThingsInstallation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("installed_app_id", models.CharField(max_length=128, unique=True)),
                ("location_id", models.CharField(blank=True, max_length=128)),
                ("access_token", models.TextField(blank=True)),
                ("refresh_token", models.TextField(blank=True)),
                ("access_token_expires_at", models.DateTimeField(blank=True, null=True)),
                ("refresh_token_expires_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SmartThingsDevice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("device_id", models.CharField(max_length=128, unique=True)),
                ("label", models.CharField(blank=True, max_length=255)),
                ("location_id", models.CharField(blank=True, max_length=128)),
                ("raw", models.JSONField(blank=True, default=dict)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SmartThingsEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("event_time", models.DateTimeField(blank=True, null=True)),
                ("installed_app_id", models.CharField(blank=True, max_length=128)),
                ("device_id", models.CharField(blank=True, max_length=128)),
                ("component", models.CharField(blank=True, max_length=128)),
                ("capability", models.CharField(blank=True, max_length=128)),
                ("attribute", models.CharField(blank=True, max_length=128)),
                ("value", models.JSONField(blank=True, default=dict)),
                ("raw", models.JSONField(blank=True, default=dict)),
                ("mqtt_topic", models.CharField(blank=True, max_length=512)),
                ("mqtt_published", models.BooleanField(default=False)),
                ("mqtt_error", models.TextField(blank=True)),
            ],
        ),
    ]
