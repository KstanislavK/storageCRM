from django.urls import path

from .views import ProductListView, ProductDetailView, ProductByCategoryListView, ProductCreateView, ProductUpdateView, \
    product_active, NomenCreateView, NomenUpdateView, NomenDetailView

app_name = 'storageapp'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),

    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<slug:slug>', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<slug:slug>', product_active, name='active'),
    path('product/detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

    path('nomen/detail/<slug:slug>/', NomenDetailView.as_view(), name='nomen_detail'),
    path('nomen/create/', NomenCreateView.as_view(), name='nomen_create'),
    path('nomen/update/<slug:slug>', NomenUpdateView.as_view(), name='nomen_update'),

    path('category/<slug:slug>', ProductByCategoryListView.as_view(), name='by_category'),
]
