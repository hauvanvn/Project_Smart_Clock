from django.conf import settings
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone

def sendOtp(user):
    OtpToken.objects.create(user=user, otp_expired_at=timezone.now() + timezone.timedelta(minutes=5))

    otp = OtpToken.objects.filter(user=user).last()
    subject = "Email Verification"
    message = f"""
                    Hi {user.last_name}, here is your OTP: {otp.otp_code}, it will expire in 5 minutes.
    """
    
    sender = settings.EMAIL_HOST_USER
    receiver = [user.email,]
    send_mail(subject, message, sender, receiver, fail_silently=False)
