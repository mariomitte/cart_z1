from django import template
from django.conf import settings
from django.db.models import Count

from apps.shop.models import Product, Category, Image
from apps.orders.models import Customer, Order, OrderItem
from apps.coupons.models import Coupon

register = template.Library()


@register.simple_tag
def query_products():
    """
    Django template filter which returns list of images in products
    """
    previews = []
    products = Product.objects.all().filter(available=True)
    for product in products:
        first_image_items = product.image_set.first()
        previews.append(first_image_items)
    return previews

@register.inclusion_tag('shop/products.html')
def preview_products_by_category(product=None, slug=None, title=None, first=False, icon=None, count=3, related=False, product_id=None):
    """
    Django template filter which returns list of images in products
    and filtering by category
    """
    previews = []
    if product:
        slug = product.category
    products = Product.objects.filter(category__name=slug)
    products = products.filter(available=True)
    if related:
        product_id = product.id
        # List of similar products
        products = products.exclude(id=product_id)
        products = products.annotate(same_category=Count('category')).order_by('-same_category','-created')
    products[:count]
    for product in products:
        first_image_items = product.image_set.first()
        previews.append(first_image_items)
    return {'currency': settings.SHOP_CURRENCY, 'products': previews, 'preview_title': title, 'first': first, 'icon': icon }

@register.inclusion_tag('shop/items/heading.html')
def section_heading(title, icon=None, first=False, dashboard=None):
    """
    Django template filter which is used for displaying pages title.
    """
    return { 'title': title, 'icon': icon, 'first': first, 'dashboard': dashboard }

@register.simple_tag
def get_product_image(product):
    """
    Django template filter which returns one product image.
    Receives a product queryset as a parameter.
    """
    return product.image_set.first().data_preview.url

@register.simple_tag
def get_categories():
    """
    Django template filter which returns list of categories.
    """
    return Category.objects.all()

@register.simple_tag
def get_product_thumbnail(product):
    """
    Django template filter which returns a thumbnail.
    Receives a product queryset as a parameter.
    """
    return product.image_set.first().data_thumbnail.url

@register.simple_tag
def get_order_item_detail(order_id):
    """
    Django template filter which returns an order by id.
    """
    return OrderItem.objects.filter(order_id=order_id)

@register.simple_tag
def model_name(value):
    """
    Django template filter which returns the verbose name of a model.
    """
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.verbose_name.title()

@register.simple_tag
def field_name(value, field):
    """
    Django template filter which returns the verbose name of an object's,
    model's or related manager's field.
    """
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.get_field(field).verbose_name.title()

@register.inclusion_tag('cart/items/coupon.html', takes_context=True)
def get_coupons(context):
    """
    Checks for coupons that can be combined
    """
    coupons = context.request.session.get('coupon_list')
    cart = context['cart']
    return { 'coupons': coupons, 'cart': cart, 'currency': settings.SHOP_CURRENCY }

@register.simple_tag
def get_coupon_value_by_id(coupon_id):
    """
    Make a database query to get Coupon and populate template
    """
    coupon = Coupon.objects.get(id=coupon_id)
    return coupon
