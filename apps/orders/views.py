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

    try:
        if not request.user.is_anonymous:
            email = request.user.email
            customer = user.customer
            fill_form_address = ShippingAddress.objects.get(email=customer.user.email)
            fill_form_card = customer.creditcard_set.get(customer=customer)
    except ShippingAddress.DoesNotExist:
        email = None
        fill_form_address = None
        fill_form_card = None

    if request.method == 'POST':

        form_address_obj = ShippingAddressForm(data=request.POST, instance=fill_form_address)
        form_card_obj = CreditCardEditForm(data=request.POST, instance=fill_form_card)
        if form_address_obj.is_valid() and form_card_obj.is_valid():
            form_address_obj.save()

            if email is None:
                email = form_address_obj.cleaned_data['email']
            form_card = form_card_obj.save(commit=False)

            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                user = User.objects.create_user(email=email)
                messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_NEW_USER'])
            else:
                user = User.objects.get(email=email)

            customer = Customer.objects.get(user=user)
            address = ShippingAddress.objects.filter(email=user.email)[0]


            year_date = form_card_obj.cleaned_data['year_date']
            month_date = form_card_obj.cleaned_data['month_date']
            form_card.set_expiration_date(year_date=str(year_date),
                                     month_date=str(month_date))
            form_card.save()

            order = Order(customer=customer, address=address)
            if cart.coupons:
                total_discount = Decimal(0)
                for item in cart.coupons:
                    order.coupon = item
                    total_discount += item.discount
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
