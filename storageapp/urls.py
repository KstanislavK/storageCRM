from django.urls import path

from .views import product_list, ProductDetailView, ProductByCategoryListView, ProductCreateView, ProductUpdateView, \
    product_active, NomenCreateView, NomenUpdateView, NomenDetailView, roll_to_retail, TkCreateView, BatchCreateView, \
    CategoryCreateView

app_name = 'storageapp'

urlpatterns = [
    path('', product_list, name='index'),

    path('product/create/<int:pk>', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<slug:slug>', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<slug:slug>', product_active, name='active'),
    path('product/detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/to-retail/<slug:slug>/', roll_to_retail, name='roll_to_retail'),

    path('nomen/detail/<slug:slug>/', NomenDetailView.as_view(), name='nomen_detail'),
    path('nomen/create/', NomenCreateView.as_view(), name='nomen_create'),
    path('nomen/update/<slug:slug>', NomenUpdateView.as_view(), name='nomen_update'),

    path('category/<slug:slug>', ProductByCategoryListView.as_view(), name='by_category'),

    path('tk_create/', TkCreateView.as_view(), name='tk_create'),
    path('batch_create/', BatchCreateView.as_view(), name='batch_create'),
    path('category_create/', CategoryCreateView.as_view(), name='category_create'),
]
