from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import ProductList, CategoryList


class ProductListView(ListView):
    model = ProductList
    template_name = 'storageapp/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return ProductList.objects.order_by('name').distinct('name')

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Товары'
        context['category_links'] = CategoryList.objects.all()
        context['products_count'] = ProductList.get_all_products_amount(self)
        return context


class ProductByCategoryListView(ListView):
    model = ProductList
    template_name = 'storageapp/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        qs = ProductList.objects.all()
        if self.kwargs['slug'] is not None:
            category = get_object_or_404(CategoryList, slug=self.kwargs['slug'])
            qs = self.model.objects.filter(category=category.pk)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductByCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Товары'
        context['category_links'] = CategoryList.objects.all()
        context['products_count'] = ProductList.get_all_products_amount
        return context


class ProductDetailView(DetailView):
    model = ProductList
    template_name = 'storageapp/product_detail.html'
    context_object_name = 'object'

