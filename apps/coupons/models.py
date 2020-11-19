from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=10,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    active = models.BooleanField()
    allow_combine = models.BooleanField(default=True)
    is_percent = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.code
