from django.contrib import admin
from .models import OrderList, OrderProductsList, TKList


@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'partner', 'created_at', 'payed', 'shipped')
    list_display_links = ('pk', 'partner')
    search_fields = ('pk', 'partner', 'created_at', 'payed', 'shipped')


@admin.register(OrderProductsList)
class OrderProductsListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'order', 'amount')
    list_display_links = ('pk', 'product', 'order', 'amount')
    search_fields = ('pk', 'product', 'order', 'amount')


@admin.register(TKList)
class TKListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
