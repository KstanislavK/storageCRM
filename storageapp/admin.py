from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('id', 'name', 'category', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
