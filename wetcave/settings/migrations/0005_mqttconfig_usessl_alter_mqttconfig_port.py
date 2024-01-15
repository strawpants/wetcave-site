# Generated by Django 4.2.5 on 2024-01-04 10:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("settings", "0004_mqttconfig_pubclientid_alter_mqttconfig_clientid"),
    ]

    operations = [
        migrations.AddField(
            model_name="mqttconfig",
            name="usessl",
            field=models.BooleanField(
                default=1, verbose_name="Use SSL for the MQTT connection"
            ),
        ),
        migrations.AlterField(
            model_name="mqttconfig",
            name="port",
            field=models.IntegerField(default=8883, verbose_name="MQTT port used"),
        ),
    ]