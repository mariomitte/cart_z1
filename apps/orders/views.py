from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.cart.cart import Cart
from apps.account.models import User
from .models import Customer, Order, OrderItem, ShippingAddress, CreditCard
from .forms import ShippingAddressForm, CreditCardEditForm
from .tasks import order_created


def order_create(request):
    """
    Creates an Order for User if user is a Customer or not.
    - Prefills form data with User and Address details if any,
    - Makes sure no orders are created if cart is empty,
    - Creates User as a Customer if user is not yet a Customer,
    """
    user = request.user
    cart_session = Cart(request)

    # Redirect to Login page if there is no Cart instance.
    # prevents creating new empty orders on order created page.
    if cart_session:
        cart = cart_session
    else:
        if user.is_anonymous:
            return redirect('account:login')
        else:
            return redirect('shop:shop_list')

    if request.method == 'POST':
        form_address = ShippingAddressForm(data=request.POST)
        form_card = CreditCardEditForm(data=request.POST)

        if form_address.is_valid() and form_card.is_valid():
            email = form_address.cleaned_data['email']

            user_exists = User.objects.filter(email=email).exists()
            address_exists = ShippingAddress.objects.filter(email=email).exists()

            if request.user.is_anonymous:
                if address_exists:
                    messages.warning(request, settings.MESSAGE['MESSAGE_WARNING_ADDRESS_OR_CREDIT_CARD_EXISTS'])
                    return redirect('account:login')
                else:
                    user = User.objects.create_user(email=email)
                    customer, customer_created = Customer.objects.get_or_create(user=user)
                    credit_card_exists = CreditCard.objects.filter(customer=customer).exists()
                    messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_NEW_USER'])
            else:
                if user_exists:
                    user = User.objects.get(email=email)
                    customer, customer_created = Customer.objects.get_or_create(user=user)
                    credit_card_exists = CreditCard.objects.filter(customer=customer).exists()

            form_card_obj = form_card.save(commit=False)
            year_date = form_card.cleaned_data['year_date']
            month_date = form_card.cleaned_data['month_date']
            form_card_obj.set_expiration_date(year_date=str(year_date),
                                 month_date=str(month_date))
            form_card_obj.customer = user.customer

            if not address_exists and not credit_card_exists:
                form_address.save()
                form_card_obj.save()

            address = ShippingAddress.objects.filter(email=user.email)[0]
            order = Order(customer=customer, address=address)
            if cart.coupons:
                total_discount = Decimal(0)
                for item in cart.coupons:
                    total_discount += item.discount
                    order.coupon = item
                    order.is_percent = item.is_percent
                order.discount = total_discount
            order.save()
            messages.success(request, str(f"{settings.MESSAGE['MESSAGE_SUCCESS_NEW_ORDER']} {order.id}"))
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.apply_async(args=[order.id], countdown=5)
            return render(request, 'orders/order/created.html', {'order': order})

    if request.method == 'GET':
        # GET: User is a Customer?
        if request.user.is_anonymous:
            form_address = ShippingAddressForm()
            form_card = CreditCardEditForm()
        else:
            try:
                customer = user.customer
                fill_form_address = ShippingAddress.objects.get(email=customer.user.email)
                fill_form_card = customer.creditcard_set.get(customer=customer)
                form_address = ShippingAddressForm(instance=fill_form_address)
                form_card = CreditCardEditForm(instance=fill_form_card)
                if fill_form_address.submitted:
                    messages.warning(request, settings.MESSAGE['MESSAGE_WARNING_ORDER_UPDATE_FOR_AUTHENTICATED_USER'])
            except Customer.DoesNotExist:
                form_address = ShippingAddressForm(initial={'email': request.user.get_email()})
    context = {
        'cart': cart,
        'form_address': form_address,
        'form_card': form_card,
    }
    return render(request, 'orders/order/create.html', context)
