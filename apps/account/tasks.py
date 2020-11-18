from django.conf import settings
from apps.orders.models import Customer


def log_request(sender, **kwargs):
    method = settings.REQUEST_METHOD
    host = settings.HTTP_HOST
    path = settings.PATH_INFO
    query = settings.QUERY_STRING
    query = '?' + query if query else ''
    print('New Request -> {method} {host}{path}{query}'.format(
        method=method,
        host=host,
        path=path,
        query=query,
    ))

# def save_or_create_user_customer(sender, instance, created, **kwargs):
#     print(instance)
#     if created:
#         Customer.objects.create(user=instance)
#     else:
#         instance.customer.save()
