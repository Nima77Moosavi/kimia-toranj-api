from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number must be set")

        # Normalize the phone number (optional, if needed)
        phone_number = self.normalize_phone_number(phone_number)

        # Create the user
        user = self.model(phone_number=phone_number, **extra_fields)

        # Hash the password before saving
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure is_staff and is_superuser are True for superusers
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Normalize the phone number by removing any non-digit characters.
        """
        return ''.join(filter(str.isdigit, phone_number))


class User(AbstractBaseUser):
    # Use phone_number as the primary identifier
    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        unique=True,
        help_text=_('Required. 15 characters or fewer. Digits only.'),
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
    )
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    # Track user status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Set phone_number as the USERNAME_FIELD
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # No additional fields are required

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.phone_number}"

    @classmethod
    def generate_otp(cls, phone_number):
        code = ''.join(random.choices('0123456789', k=6))
        expires_at = timezone.now() + timezone.timedelta(minutes=2)
        otp = cls.objects.create(
            phone_number=phone_number, code=code, expires_at=expires_at)
        return otp

    def is_valid(self):
        return timezone.now() <= self.expires_at

class BlacklistedAccessToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.jti
    