from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Coupon
from .forms import CouponApplyForm
from apps.cart.cart import Cart





@require_POST
def coupon_apply(request):
    cart = Cart(request)
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    next_type = True
    if form.is_valid():
        code = form.cleaned_data['code']


        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            coupons_list = request.session.get('coupon_list')
            coupons_keys = coupons_list.keys()

            if coupon.allow_combine is True:
                next_type = True
                if coupons_keys:
                    not_combine_type = Coupon.objects.filter(id__in=coupons_keys, allow_combine=False)
                    if not_combine_type:
                        next_type = False
                        messages.error(request, settings.MESSAGE['MESSAGE_ERROR_COUPON_CANNOT_COMBINE'])
                if next_type is True:
                    cart.add_coupon(coupon.id, coupon.is_percent)
                    messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_COUPON_ADDED'])
            if len(coupons_list) == 0:
                if coupon.allow_combine is False:
                    next_type = True
                    cart.add_coupon(coupon.id, coupon.is_percent)
                    messages.success(request, settings.MESSAGE['MESSAGE_SUCCESS_COUPON_ADDED'])
            else:
                if coupon.allow_combine is False:
                    next_type = False
                    messages.error(request, settings.MESSAGE['MESSAGE_ERROR_COUPON_CANNOT_COMBINE'])

                print(coupons_keys)
                for id in coupons_keys:
                    id = int(id)
                    print("id", id)
        except Coupon.DoesNotExist:
            pass
            messages.error(request, settings.MESSAGE['MESSAGE_ERROR_COUPON_CODE_EXPIRED'])
    return redirect('cart:cart_detail')

@require_POST
def coupon_remove(request, coupon_id):
    cart = Cart(request)
    cart.remove_coupon_by_id(coupon_id)
    return redirect('cart:cart_detail')


# for id in coupons:
#     if id not in can_be_combined.id:
#         cart.remove_coupon_by_id(id)
#         messages.error(
#             context.request,
#             settings.MESSAGES['MESSAGE_ERROR_COUPON_CANNOT_COMBINE'])
