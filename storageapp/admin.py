from django.contrib import admin

from .models import Category, Product, Batch, Nomenclature


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


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category','part_number')
    list_display_links = ('id', 'name', 'part_number')
    search_fields = ('id', 'name', 'part_number')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'batch')}
    list_display = ('id', 'name', 'quantity', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug', 'category')


