from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category, Nomenclature


class ProductListView(ListView):
    model = Nomenclature
    template_name = 'storageapp/index.html'
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Товары'
        context['category_links'] = Category.objects.all()

        return context


class ProductByCategoryListView(ListView):
    model = Nomenclature
    template_name = 'storageapp/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        qs = Nomenclature.objects.all()
        if self.kwargs['slug'] is not None:
            category = get_object_or_404(Category, slug=self.kwargs['slug'])
            qs = self.model.objects.filter(category=category.pk)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductByCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Товары'
        context['category_links'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'storageapp/product_detail.html'
    context_object_name = 'object'

