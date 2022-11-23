from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import ProductForm, NomenForm, SearchForm
from .models import ProductList, CategoryList, NomenList


# class ProductListView(ListView):
#     model = NomenList
#     template_name = 'storageapp/index.html'
#     context_object_name = 'objects'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductListView, self).get_context_data(**kwargs)
#         context['title'] = 'Товары'
#         context['category_links'] = CategoryList.objects.all()
#         context['products_count'] = ProductList.get_all_products_amount(self)
#         return context


def product_list(request):
    objects = NomenList.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            search_results = []
            data_for_search = form.data['data_for_search']

            if data_for_search.isdigit():
                search_results = list(NomenList.objects.filter(pk=int(data_for_search)))
            search_results = set(list(NomenList.objects.filter(part_number__contains=data_for_search)) + \
                                 list(NomenList.objects.filter(name__contains=data_for_search)) + \
                                 search_results)

            context = {
                'title': 'Товары',
                'objects': search_results,
                'category_links': CategoryList.objects.all(),
                'products_count': ProductList.get_all_products_amount(),
            }
            return render(request, 'storageapp/index.html', context)

    context = {
        'title': 'Товары',
        'objects': objects,
        'category_links': CategoryList.objects.all(),
        'products_count': ProductList.get_all_products_amount(),
    }

    return render(request, 'storageapp/index.html', context)


class ProductByCategoryListView(ListView):
    model = NomenList
    template_name = 'storageapp/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        qs = NomenList.objects.all()
        if self.kwargs['slug'] is not None:
            category = get_object_or_404(CategoryList, slug=self.kwargs['slug'])
            qs = self.model.objects.filter(category=category.pk)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductByCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Товары'
        context['category_links'] = CategoryList.objects.all()
        context['products_count'] = ProductList.get_all_products_amount()
        return context


class ProductDetailView(DetailView):
    model = ProductList
    template_name = 'storageapp/product_detail.html'
    context_object_name = 'object'

    def get_queryset(self):
        return ProductList.objects.filter(is_active=True)


class ProductCreateView(CreateView):
    model = ProductList
    template_name = 'storageapp/product_create_form.html'
    context_object_name = 'product_objects'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить товар'
        return context


class ProductUpdateView(UpdateView):
    model = ProductList
    form_class = ProductForm
    template_name = 'storageapp/product_crud_form.html'
    success_url = reverse_lazy('storageapp:index')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирования товара'
        context['obj'] = ProductList.objects.get(slug=self.kwargs['slug'])
        return context


def product_active(request, slug):
    product = get_object_or_404(ProductList, slug=slug)
    prod_slug = NomenList.objects.get(product__slug=slug).slug

    if request.method == 'GET':
        if product.is_active:
            product.is_active = False
        else:
            product.is_active = True

        product.save()

        return HttpResponseRedirect(reverse('storageapp:nomen_detail', kwargs={'slug': prod_slug}))


class NomenCreateView(CreateView):
    model = NomenList
    template_name = 'storageapp/product_create_form.html'
    context_object_name = 'nomen_objects'
    form_class = NomenForm

    def get_context_data(self, **kwargs):
        context = super(NomenCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить номенклатуру'
        return context


class NomenUpdateView(UpdateView):
    model = NomenList
    form_class = NomenForm
    template_name = 'storageapp/product_crud_form.html'
    success_url = reverse_lazy('storageapp:index')

    def get_context_data(self, **kwargs):
        context = super(NomenUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирования номенклатуры'
        context['obj'] = NomenList.objects.get(slug=self.kwargs['slug'])
        return context


class NomenDetailView(DetailView):
    model = NomenList
    template_name = 'storageapp/nomen_detail.html'
    context_object_name = 'object'
