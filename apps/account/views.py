from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page


from .forms import UserLoginForm, UserSignupForm, UserEditForm, UserChangePassword
from apps.orders.models import Customer, Order, OrderItem, ShippingAddress
from apps.shop.models import Product
from apps.orders.forms import EditShippingAddressForm, CustomerEditForm, CreditCardEditForm

User = get_user_model()

section = 'dashboard'

@login_required
# @cache_page(60 * 1)
def dashboard(request, address_id=None):
    order_items = ()
    try:
        customer = request.user.customer
        orders = customer.order_set.all()
        credit_card = customer.creditcard_set.get(customer=customer)
        address = ShippingAddress.objects.get(email=request.user.email)
        for item in orders:
            order_items = item.items.all()
        context = {
            'section': section,
            'customer': customer,
            'orders': orders,
            'order_items': order_items,
            'address': address,
            'credit_card': credit_card,
        }
    except Customer.DoesNotExist:
        User.objects.create_customer()
        messages.warning(request, settings.MESSAGE['MESSAGE_WARNING_ORDER_NOT_EXISTS'])
        context = {'section': section}
    return render(request, 'account/dashboard/pages/dashboard.html', context)

@login_required
def dashboard_change_address(request):
    """
    Django view which checks for user address and can update an
    existing address.
    """
    address = ShippingAddress.objects.get(email=request.user.email)
    if request.method == "POST":
        form = EditShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_SHIPPING_ADDRESS'])
            return redirect('account:dashboard')
    if request.method == "GET":
        form = EditShippingAddressForm(instance=address)
    context = {
        'section': 'change_address',
        'form': form,
    }
    return render(request, 'account/dashboard/pages/address_change.html', context)

def signup(request):
    if request.method == "POST":
        user_form = UserSignupForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_NEW_USER'])
            return redirect(new_user.get_absolute_url())
    else:
        user_form = UserSignupForm()
    return render(request,
                  'account/signup.html',
                  {'form': user_form})

@login_required
def dashoard_customer_edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = CustomerEditForm(
            instance=request.user.customer,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_PROFILE_UPDATED'])
        else:
            messages.error(request, settings.MESSAGE['MESSAGE_FAILED_PROFILE_UPDATE'])
    if request.method == "GET":
        user_form = UserEditForm(instance=request.user)
        profile_form = CustomerEditForm(instance=request.user.customer)
    context = {
        'section': 'change_customer',
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'account/dashboard/pages/customer_change.html', context)

@login_required
def dashboard_credit_card_edit(request):
    customer = request.user.customer
    credit_card = customer.creditcard_set.get(customer=customer)
    if request.method == "POST":
        form_obj = CreditCardEditForm(instance=credit_card, data=request.POST)
        if form_obj.is_valid():
            form = form_obj.save(commit=False)
            year_date = form_obj.cleaned_data['year_date']
            month_date = form_obj.cleaned_data['month_date']
            form.set_expiration_date(year_date=str(year_date),
                                     month_date=str(month_date))
            form.save()
            messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_CREDIT_CARD_UPDATED'])
            return redirect('account:dashboard')
        else:
            messages.error(request, settings.MESSAGE['MESSAGE_ERROR_CREDIT_CARD_UPDATE'])
    if request.method == "GET":
        form = CreditCardEditForm(instance=credit_card)
    context = {
        'section': 'change_credit_card',
        'form': form,
    }
    return render(request, 'account/dashboard/pages/credit_card_change.html', context)

@login_required
def dashboard_user_password_edit(request):
    if request.method == "POST":
        form_obj = UserChangePassword(request.POST, instance=request.user)
        if form_obj.is_valid():
            form = form_obj.save(commit=False)
            # email = form_obj.cleaned_data['email']
            form.password = form.set_password(form_obj.cleaned_data['password'])
            form.save()
            messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_UPDATE_PASSWORD'])
            return redirect('account:dashboard')
    else:
        form = UserChangePassword()
    context = {
        'section': 'password_change',
        'form': form,
    }
    return render(request,
                  'account/dashboard/pages/password_change.html',
                  context)
