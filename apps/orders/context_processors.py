from django.conf import settings

from .models import Customer


def currency(request):
    currency = settings.SHOP_CURRENCY
    return {'currency': currency}
