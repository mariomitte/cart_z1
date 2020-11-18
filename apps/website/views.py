from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

from apps.orders.models import Customer, Order, ShippingAddress


def home(request):
    context = { 'section': 'home' }
    return render(request, 'pages/home.html', context)

def about(request):
    context = { 'section': 'about' }
    return render(request, 'pages/about.html', context)

def faq(request):
    context = { 'section': 'faq' }
    return render(request, 'pages/faq.html', context)
