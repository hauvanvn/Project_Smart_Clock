# Generated by Django 5.1.3 on 2024-12-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0007_alter_thdata_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thdata',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]