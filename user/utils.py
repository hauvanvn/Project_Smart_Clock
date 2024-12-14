from django.db import models
from django.conf import settings
from .models import OtpToken, User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils import timezone
import os

# Delete old Avatar image
@receiver(models.signals.pre_save, sender=User)
def auto_delete_material(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_avatar = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    
    new_avatar = instance.avatar
    if not old_avatar == new_avatar and old_avatar.name != 'users/avatar.svg':
        if os.path.isfile(old_avatar.path):
            os.remove(old_avatar.path)

def sendOtp(user):
    OtpToken.objects.update_or_create(
        user=user,
        defaults={
            'otp_expired_at': timezone.now() + timezone.timedelta(minutes=5),
        }
    )

    otp = OtpToken.objects.filter(user=user).last()
    subject = "Email Verification"
    message = f"""
                    Hi {user.last_name}, here is your OTP: {otp.otp_code}, it will expire in 5 minutes.
    """
    
    sender = settings.EMAIL_HOST_USER
    receiver = [user.email,]
    send_mail(subject, message, sender, receiver, fail_silently=False)
