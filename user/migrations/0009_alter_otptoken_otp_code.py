# Generated by Django 5.1.3 on 2024-12-12 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='1f2d64', max_length=6),
        ),
    ]
