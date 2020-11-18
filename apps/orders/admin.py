from django.contrib import admin

from .models import Customer, Order, OrderItem, ShippingAddress, CreditCard


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'gender']
    list_filter = ['user', 'gender']
    readonly_fields = ['currency']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'paid', 'created', 'updated']
    list_filter = ['customer', 'address', 'paid', 'created', 'updated']
    inlines = [OrderItemInline]

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'address', 'city', 'country']
    list_filter = ['email', 'first_name', 'last_name', 'address', 'postal_code', 'city', 'country']

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['customer']
    list_filter = ['customer']
