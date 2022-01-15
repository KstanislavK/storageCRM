from django.urls import path

from .views import ProductListView, ProductDetailView, ProductByCategoryListView

app_name = 'storageapp'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>', ProductByCategoryListView.as_view(), name='by_category'),
]
