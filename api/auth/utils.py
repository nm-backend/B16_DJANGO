import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp(length=4):
    """Generate a random OTP of given length."""
    return ''.join(random.choices('0123456789', k=length))


def send_otp_email(email, otp):
    """Send OTP to the given email."""
    subject = 'Ваш одноразовый пароль (OTP)'
    message = f'Ваш одноразовый пароль: {otp}. Действителен в течение 5 минут.'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])