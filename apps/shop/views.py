from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Category, Product
# from cart.forms import CartAddProductForm


def shop_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        print(category_slug)
        print(products)
    context = {'section': 'store',
               'category': category,
               'categories': categories,
               'products': products}
    return render(request, 'shop/shop_list.html', context)

def product_detail(request, id, slug):
    user = request.user
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    context = {
        'section': 'detail',
        'product': product,
        'product_image': product.image_set.first(),
        'product_images': product.image_set.all(),
    }
    return render(request, 'shop/product/detail.html', context)
