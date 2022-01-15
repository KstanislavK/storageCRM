from django.contrib import admin

from .models import Category, Product, Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'delivery_date', 'slug')
    list_display_links = ('id', 'delivery_date', 'name')
    search_fields = ('id', 'name', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'batch')}
    list_display = ('id', 'name', 'category', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug', 'category')
