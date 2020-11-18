from django.urls import path, reverse_lazy
from django.urls import include

from . import views


app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
]
