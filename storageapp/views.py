from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from ordersapp.models import OrderList, OrderProductsList, TKList
from partnersapp.models import PartnersList
from .forms import ProductForm, NomenForm, SearchForm, TkCreateViewForm, BatchCreateViewForm, CategoryCreateViewForm
from .models import ProductList, CategoryList, NomenList, BatchList


@login_required
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
                'dfs': data_for_search,
            }
            return render(request, 'storageapp/index.html', context)

    context = {
        'title': 'Товары',
        'objects': objects,
        'category_links': CategoryList.objects.all(),
        'products_count': ProductList.get_all_products_amount(),
    }

    return render(request, 'storageapp/index.html', context)


class ProductByCategoryListView(LoginRequiredMixin, ListView):
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = ProductList
    template_name = 'storageapp/product_detail.html'
    context_object_name = 'object'

    def get_queryset(self):
        return ProductList.objects.filter(is_active=True)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = ProductList
    template_name = 'storageapp/product_create_form.html'
    context_object_name = 'product_objects'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить товар'
        return context

    def form_valid(self, form):
        nomen = NomenList.objects.get(pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.name = nomen
        self.object.save()

        return HttpResponseRedirect(
            reverse(
                'storageapp:nomen_detail',
                kwargs={'slug': nomen.slug}))


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductList
    form_class = ProductForm
    template_name = 'storageapp/product_crud_form.html'
    success_url = reverse_lazy('storageapp:index')

    def get_success_url(self):
        product_slug = self.kwargs['slug']
        nomen = NomenList.objects.get(product__slug=product_slug)
        return reverse('storageapp:nomen_detail', kwargs={'slug': nomen.slug})

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирования товара'
        context['obj'] = ProductList.objects.get(slug=self.kwargs['slug'])
        return context


@login_required
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


@login_required
def roll_to_retail(request, slug):
    product = get_object_or_404(ProductList, slug=slug)
    prod_slug = NomenList.objects.get(product__slug=slug).slug

    if request.method == 'GET':
        product.amount = product.amount - 1
        product.save()

        new_ret = ProductList(
            name=product.name,
            batch=product.batch,
            is_active=True,
            is_retail=True,
            amount=NomenList.objects.get(product__slug=slug).meters
            )

        new_ret.save()

        return HttpResponseRedirect(
            reverse(
                'storageapp:nomen_detail',
                kwargs={
                    'slug': prod_slug}))


class NomenCreateView(LoginRequiredMixin, CreateView):
    model = NomenList
    template_name = 'storageapp/product_create_form.html'
    context_object_name = 'nomen_objects'
    form_class = NomenForm

    def get_context_data(self, **kwargs):
        context = super(NomenCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить номенклатуру'
        return context


class NomenUpdateView(LoginRequiredMixin, UpdateView):
    model = NomenList
    form_class = NomenForm
    template_name = 'storageapp/product_crud_form.html'
    success_url = reverse_lazy('storageapp:index')

    def get_context_data(self, **kwargs):
        context = super(NomenUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирования номенклатуры'
        context['obj'] = NomenList.objects.get(slug=self.kwargs['slug'])
        return context


class NomenDetailView(LoginRequiredMixin, DetailView):
    model = NomenList
    template_name = 'storageapp/nomen_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super(NomenDetailView, self).get_context_data(**kwargs)
        context['retail'] = ProductList.objects.filter(name=self.object, is_retail=True, is_active=True)
        return context


class TkCreateView(LoginRequiredMixin, CreateView):
    model = TKList
    template_name = 'storageapp/product_crud_form.html'
    context_object_name = 'nomen_objects'
    form_class = TkCreateViewForm
    success_url = reverse_lazy('storageapp:index')

    def get_context_data(self, **kwargs):
        context = super(TkCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить Транспортную'
        return context


class BatchCreateView(LoginRequiredMixin, CreateView):
    model = BatchList
    template_name = 'storageapp/product_crud_form.html'
    context_object_name = 'nomen_objects'
    form_class = BatchCreateViewForm
    success_url = reverse_lazy('storageapp:index')

    def get_context_data(self, **kwargs):
        context = super(BatchCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить партию'
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = CategoryList
    template_name = 'storageapp/product_crud_form.html'
    context_object_name = 'nomen_objects'
    form_class = CategoryCreateViewForm
    success_url = reverse_lazy('storageapp:index')

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить категорию'
        return context
