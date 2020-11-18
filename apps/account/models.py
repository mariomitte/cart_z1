import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import signals
from django.dispatch import receiver

from .managers import CustomUserManager
from apps.orders.models import Customer, ShippingAddress

def _default_uuid():
    return str(uuid.uuid4())

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model
    """
    username = models.TextField(default=_default_uuid, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('date_joined',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email

    def get_absolute_url(self):
        return reverse('account:dashboard')

@receiver(signals.post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(id=instance.id)
        customer = Customer.objects.create(user=user)
        customer.creditcard_set.create(customer=customer)
        address = ShippingAddress.objects.create(email=instance.email)
        customer.save()
