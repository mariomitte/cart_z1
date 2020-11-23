import decimal

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.shop.models import Product
from apps.coupons.models import Coupon

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

# Image resize defaults
thumbnail_size = settings.IMAGE_THUMBNAIL_SIZE
preview_size = settings.IMAGE_PREVIEW_SIZE
decimal.getcontext().prec = 2
Decimal=decimal.Decimal


class Customer(models.Model):
    """
    Shop Customer model
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    contact = models.CharField(max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='profile', blank=True)
    photo_thumbnail = ImageSpecField(source='photo',
                                      processors=[ResizeToFit(width=thumbnail_size,height=thumbnail_size)],
                                      format='JPEG',
                                      options={'quality': 60})
    photo_preview = ImageSpecField(source='photo',
                                      processors=[ResizeToFit(width=preview_size,height=preview_size)],
                                      format='JPEG',
                                      options={'quality': 60})
    currency = models.CharField(max_length=10, default=settings.SHOP_CURRENCY)

    class Meta:
        ordering = ('id',)
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.user.email

class Order(models.Model):
    """
    Shop Order model
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey("ShippingAddress", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH,
                                    blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    is_percent = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        if self.is_percent:
            return total_cost - total_cost * (self.discount / Decimal(100))
        else:
            return total_cost - self.discount


class OrderItem(models.Model):
    """
    Shop Item model
    """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        price = self.price * self.quantity
        if self.quantity > 1:
            price = price - ((self.quantity - 1) * Decimal(settings.STORE_HAS_QUANTITY_DISCOUNT_VALUE))
        return price

class ShippingAddress(models.Model):
    """
    Shop customer Shipping address model
    """
    email = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH)
    first_name = models.CharField(max_length=settings.WEBSITE_SLUG_MAX_LENGTH)
    last_name = models.CharField(max_length=settings.WEBSITE_SLUG_MAX_LENGTH)
    address = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH)
    postal_code = models.CharField(max_length=settings.WEBSITE_SLUG_MAX_LENGTH)
    city = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH)
    country = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH)
    submitted = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
        verbose_name = 'shipping address'
        verbose_name_plural = 'shipping address'

    def __str__(self):
        return str(f"{self.first_name}-{self.last_name}-{self.address}-{self.city}-{self.country}")

    def get_absolute_url(self):
        return reverse('account:dashboard_change_address')

class CreditCard(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    credit_card_number = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    credit_card_expiration_date = models.CharField(max_length=10, blank=True, null=True)
    month_date = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    year_date = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    credit_card_cvc = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'credit card'
        verbose_name_plural = 'credit card'

    def __str__(self):
        return self.customer.user.email

    def set_expiration_date(self, year_date, month_date):
        dates = [str(month_date), str(year_date)]
        dates = "/".join(dates)
        self.credit_card_expiration_date = dates

    def get_absolute_url(self):
        return reverse('account:dashboard_credit_card_edit')
