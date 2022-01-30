from django.contrib import admin

from .models import CategoryList, BatchList, MakerList, ProductList, NomenList


@admin.register(NomenList)
class NomenListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'part_number', 'name', 'slug')
    list_display_links = ('id', 'part_number', 'name')
    search_fields = ('id', 'part_number', 'name', 'slug', 'category')


@admin.register(BatchList)
class BatchListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'delivery_date', 'slug')
    list_display_links = ('id', 'delivery_date', 'name')
    search_fields = ('id', 'name', 'slug')


@admin.register(CategoryList)
class CategoryListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'slug')


@admin.register(MakerList)
class CategoryListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('id', 'name', 'country', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'country', 'slug')


@admin.register(ProductList)
class ProductListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'batch')}
    list_display = ('id', 'name', 'batch', 'amount', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'batch', 'slug')
