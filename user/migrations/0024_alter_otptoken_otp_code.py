# Generated by Django 5.1.3 on 2024-12-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='c9b5c6', max_length=6),
        ),
    ]