from django.urls import path, reverse_lazy

from . import views


app_name = 'shop'

urlpatterns = [
    path('category/<slug:category_slug>/', views.shop_list, name='shop_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('', views.shop_list, name='shop_list'),
]
