from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    email = models.EmailField(verbose_name='электронная почта', unique=True, blank=False, null=False)
    avatar = ResizedImageField(verbose_name='аватар', upload_to='users/avatars/', 
                               crop=['middle', 'center'], 
                               null=True, blank=True, size=[300, 300], quality=90)
    phone_number = PhoneNumberField(verbose_name='номер телефона', unique=True, null=True, blank=True)
    bio = models.TextField(verbose_name='о себе', null=True, blank=True)
    address = models.CharField(verbose_name='адрес', max_length=255, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{str(self.email) or self.first_name}'

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_otps')
    otp_code = models.CharField(max_length=4)
    is_used = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Password Reset OTP'
        ordering = ['-created_at']

    def save (self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
            super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f'{self.user.email} - {self.otp}'