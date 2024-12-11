from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.conf import settings
import os
import secrets


# Create your models here.

def upload_path_handle(instance, filename):
    return 'users/{id}/{file}'.format(id=instance, file=filename)

class User(AbstractUser):
    avatar = models.ImageField(default='users/avatar.svg', upload_to=upload_path_handle)

class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expired_at = models.DateTimeField(blank=True, null=True)

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