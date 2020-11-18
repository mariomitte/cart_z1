from django.contrib import admin

from .models import Category, Product, Image


class ImageAdmin(admin.TabularInline):
    model = Image

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]
    list_display = ['name', 'price',
                    'available', 'updated']
    list_filter = ['category', 'available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
