from django.conf import settings
from django.contrib import messages

from apps.shop.models import Product
from apps.coupons.models import Coupon
from apps.website.utils import Decimal


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.coupon_list = self.session['coupon_list'] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = None
        self.coupon_list = self.session.get('coupon_list')
        self.discount_from_store = Decimal(settings.STORE_HAS_QUANTITY_DISCOUNT_VALUE)
        self.has_run = False

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        start_discount_from_quantity = str(0)
        if product_id not in self.cart:
            if product.has_discount_from_store is True:
                start_discount_from_quantity = product.start_discount_from_quantity
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price),
                                      'start_discount_from_quantity': product.start_discount_from_quantity,}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            del self.coupon_list
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        def create_total_price(price, quantity):
            total_price = Decimal(price) * quantity
            if self.has_run is True:
                # product_price = product.price
                if item['start_discount_from_quantity'] is not '0':
                    if quantity >= Decimal(item['start_discount_from_quantity']):
                        # decimal.getcontext().prec = 2
                        total_price = Decimal(round(total_price - ((quantity - 1) * self.discount_from_store)))
            print("HAS PRICE #", total_price)
            return total_price

        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = create_total_price(item['price'], item['quantity'])
            self.has_run = True
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    # def get_total_price(self):
    #     return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total_price = []
        for item in self.cart.values():
            has_price = Decimal(item['price']) * item['quantity']
            if item['start_discount_from_quantity'] is not '0':
                if item['quantity'] >= Decimal(item['start_discount_from_quantity']):
                    has_price = Decimal(round(has_price - ((item['quantity'] - 1) * self.discount_from_store)))
            total_price.append(has_price)
        return sum(total_price)

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupons(self):
        if self.coupon_list:
            try:
                coupons = []
                for id in self.coupon_list:
                    coupons.append(Coupon.objects.get(id=id))
                return coupons
            except Coupon.DoesNotExist:
                pass
        return None

    def add_coupon(self, coupon_id, is_percent):
        self.coupon_id = coupon_id
        self.session['coupon_list'][str(coupon_id)] = {'coupon_id': coupon_id,
                                                       'is_percent': is_percent,}
        self.get_total_price_after_discount()
        self.save()

    def get_discount(self):
        discount = []
        total_discount = Decimal(0)

        if self.coupon_list:
            for item in self.coupon_list:
                coupon = Coupon.objects.get(id=item)
                discount_value = coupon.discount
                if coupon.is_percent:
                    discount.append((discount_value / Decimal(100)) * self.get_total_price())
                else:
                    discount.append(discount_value)
            for item in discount:
                total_discount += item
        return total_discount

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def remove_coupon_by_id(self, coupon_id):
        coupon_id = str(coupon_id)
        if coupon_id in self.coupon_list:
            del self.coupon_list[coupon_id]
        del self.coupon_id
        self.save()
