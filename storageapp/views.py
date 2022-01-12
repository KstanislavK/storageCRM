from django.shortcuts import render
from django.views.generic import ListView

from .models import Product, Category


class ProductsListView(ListView):
    model = Product
    template_name = 'partnersapp/index.html'
    context_object_name = 'partners_objects'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Контрагенты'
        return context
