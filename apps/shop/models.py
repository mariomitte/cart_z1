from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

# Image resize defaults
thumbnail_size = settings.IMAGE_THUMBNAIL_SIZE
preview_size = settings.IMAGE_PREVIEW_SIZE

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    """
    Store category model
    """
    name = models.CharField(max_length=settings.WEBSITE_SLUG_MAX_LENGTH,
                            db_index=True)
    slug = models.SlugField(max_length=settings.WEBSITE_SLUG_MAX_LENGTH,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:shop_list_by_category', args=[self.slug])

class Image(models.Model):
    """
    Store product images in full size, thumbnail or preview
    """
    name = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    data = models.ImageField(upload_to='product')
    data_thumbnail = ImageSpecField(source='data',
                                      processors=[ResizeToFit(width=thumbnail_size,height=thumbnail_size)],
                                      format='JPEG',
                                      options={'quality': 60})
    data_preview = ImageSpecField(source='data',
                                      processors=[ResizeToFit(width=preview_size,height=preview_size)],
                                      format='JPEG',
                                      options={'quality': 60})

    class Meta:
        ordering = ('id',)
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    A product model stores information about product like name, price and
    category
    """
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=settings.WEBSITE_MODEL_FIELD_LENGTH,
                            db_index=True)
    slug = models.SlugField(max_length=settings.WEBSITE_SLUG_MAX_LENGTH,
                            db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=settings.PRODUCT_PRICE_MAX_DIGITS,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
