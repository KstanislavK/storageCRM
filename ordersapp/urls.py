from django.urls import path

from .views import OrderActiveListView, OrderDetailView, get_order_list, order_delete, set_payed, OrderCreateView, \
    OrderUpdateView, OrderProductCreate, order_product_delete

app_name = 'ordersapp'

urlpatterns = [
    path('', get_order_list, name='index'),
    path('active/', OrderActiveListView.as_view(), name='active_orders'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('update/<int:pk>', OrderUpdateView.as_view(), name='order_update'),
    path('delete/<int:pk>', order_delete, name='order_delete'),
    path('payed/<int:pk>', set_payed, name='order_payed'),
    path('product_create/<int:pk>', OrderProductCreate.as_view(), name='order_product_create'),
    path('product_delete/<int:pk>', order_product_delete, name='order_product_delete'),
]
