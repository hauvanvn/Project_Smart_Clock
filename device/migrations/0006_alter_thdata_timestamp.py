# Generated by Django 5.1.3 on 2024-12-19 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0005_devices_buzzermode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thdata',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]