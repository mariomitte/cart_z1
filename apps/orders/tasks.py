from celery import task
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
import html2text

from .models import Order, OrderItem


ORDER_NOTIFY_TEMPLATE = 'orders/html/email_order_notification.html'

@task(name="send_mail_to_customer")
def order_created(order_id, from_email: str = None):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    products = order.items.all()
    user = order.customer.user

    subject = '{} Submitted a New Order'.format(user.email)

    # Render the HTML template
    body_html = render_to_string(
        ORDER_NOTIFY_TEMPLATE,
        {'order': order,
         'products': products},
    )

    # Take rendered HTML and convert to plain text (Markdown)
    text_content = html2text.html2text(body_html)
    to = [user.email,]

    mail.send_mail(
        subject,
        text_content,
        from_email or settings.DEFAULT_FROM_EMAIL,
        to,
        html_message=text_content,
    )
