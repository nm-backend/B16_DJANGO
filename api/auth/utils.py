import random
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def generate_otp(length=4):
    """Generate a random OTP of given length."""
    return ''.join(random.choices('0123456789', k=length))


def send_otp_email(email, otp):
    """Send OTP to the given email."""
    subject = 'Ваш одноразовый пароль (OTP)'
    message = f'Ваш одноразовый пароль: {otp}. Действителен в течение 5 минут.'
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, [email])
        logger.info(f"OTP {otp} sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP to {email}: {e}")
        raise  # Перебрасываем исключение, чтобы views мог обработать