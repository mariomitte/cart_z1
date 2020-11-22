from decimal import Decimal
from django.conf import settings
from django.contrib import messages

from apps.shop.models import Product
from apps.coupons.models import Coupon


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

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['price'] = str(self._change_product_price_on_quantity(product, quantity))
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
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

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

    def _change_product_price_on_quantity(self, product, quantity):
        product_discount = Decimal(0)
        has_delta = product.price * Decimal(settings.DISCOUNT_ON_QUANTITY_HAS_DISCOUNT_VALUE_MAIN)
        # price = product.price - (has_delta * quantity)
        sum = Decimal(0)
        drop_in = Decimal(0)
        price = product.price

        if quantity > 1:
            x = Decimal(settings.DISCOUNT_ON_QUANTITY_HAS_DISCOUNT_VALUE_MAIN)
            y = Decimal(settings.DISCOUNT_ON_QUANTITY_HAS_DISCOUNT_VALUE_DELTA)
            for item in range(1, quantity):
                # drop_in += (x + y - (x * y))
                drop_in += x
                print("DROP IN #", drop_in)
            price = product.price - (product.price * drop_in)

        print("PRODUCT DISCOUNT #1", product_discount)
        print("PRICE #", price)
        return Decimal(price)
