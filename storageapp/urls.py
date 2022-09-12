from django.urls import path

from .views import product_list, ProductDetailView, ProductByCategoryListView, ProductCreateView, ProductUpdateView, \
    product_active, NomenCreateView, NomenUpdateView, NomenDetailView

app_name = 'storageapp'

urlpatterns = [
    path('', product_list, name='index'),

    path('product/create/<int:pk>', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<slug:slug>', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<slug:slug>', product_active, name='active'),
    path('product/detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

    path('nomen/detail/<slug:slug>/', NomenDetailView.as_view(), name='nomen_detail'),
    path('nomen/create/', NomenCreateView.as_view(), name='nomen_create'),
    path('nomen/update/<slug:slug>', NomenUpdateView.as_view(), name='nomen_update'),

    path('category/<slug:slug>', ProductByCategoryListView.as_view(), name='by_category'),
]
