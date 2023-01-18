from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from partnersapp.models import PartnersList
from storageapp.models import BatchList, ProductList, NomenList
from transportapp.models import RideList
from .adiitional_functions import count_sold_products
from .forms import SearchForm, NewOrderForm, UpdateOrderForm, OrderProductForm
from .models import OrderList, OrderProductsList


@login_required
def get_order_list(request):
    objects = OrderList.objects.all()
    paginator = Paginator(objects, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            search_results = []
            data_for_search = form.data['data_for_search']

            if data_for_search.isdigit():
                search_results = list(
                    OrderList.objects.filter(
                        pk=int(data_for_search)))
            search_results = set(
                list(
                    OrderList.objects.filter(
                        partner__partner_city__contains=data_for_search)) +
                list(
                    OrderList.objects.filter(
                        partner__name__contains=data_for_search)) +
                list(
                    OrderList.objects.filter(
                        partner__address__contains=data_for_search)) +
                list(
                    OrderList.objects.filter(
                        tk__name__contains=data_for_search)) +
                search_results)
            context = {
                'page_obj': search_results,
                'form': form,
                'dfs': data_for_search,
            }
            return render(request, 'ordersapp/index.html', context)

    context = {
        'page_obj': page_obj,
        'title': 'Все заказы',
    }
    return render(request, 'ordersapp/index.html', context)


class OrderActiveListView(LoginRequiredMixin, ListView):
    """ Общий вывод активных заказов """
    model = OrderList
    template_name = 'ordersapp/index.html'
    context_object_name = 'objects'
    paginate_by = 10

    def get_queryset(self):
        return OrderList.objects.filter(shipped=False)

    def get_context_data(self, **kwargs):
        context = super(OrderActiveListView, self).get_context_data(**kwargs)
        context['title'] = 'Заказы в работе'
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = OrderList
    template_name = 'ordersapp/order_detail.html'
    context_object_name = 'object'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args, **kwargs)
        try:
            ride = get_object_or_404(RideList, order=self.object)
            context['ride'] = ride
        except:
            pass
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = OrderList
    template_name = 'ordersapp/order_crud_form.html'
    form_class = NewOrderForm

    def form_valid(self, form):
        form.instance.user_creator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый заказ'
        return context


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = OrderList
    template_name = 'ordersapp/order_crud_form.html'
    form_class = UpdateOrderForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('ordersapp:order_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование заказа'
        context['obj'] = OrderList.objects.get(pk=self.kwargs['pk'])
        return context


@login_required
def order_delete(request, pk):
    order = get_object_or_404(OrderList, pk=pk)
    if request.method == 'GET':
        order.delete()
    return HttpResponseRedirect(reverse('ordersapp:index'))


@login_required
def set_payed(request, pk):
    order = get_object_or_404(OrderList, pk=pk)
    if request.method == 'GET':
        if order.payed:
            order.payed = False
        else:
            order.payed = True
        order.save()

        return HttpResponseRedirect(
            reverse(
                'ordersapp:order_detail',
                kwargs={
                    'pk': pk}))


@login_required
def set_shipped(request, pk):
    order = get_object_or_404(OrderList, pk=pk)
    if request.method == 'GET':

        if order.shipped:
            order.shipped = False
            order_products = OrderProductsList.objects.filter(order=pk)
            for o_prod in order_products:
                product = get_object_or_404(ProductList, name=o_prod.product, batch=o_prod.batch, is_retail=o_prod.is_retail)
                product.amount = product.amount + o_prod.amount
                product.save()
        else:
            order.shipped = True
            order.shipped_date = datetime.now()
            order_products = OrderProductsList.objects.filter(order=pk)
            for o_prod in order_products:
                product = get_object_or_404(ProductList, name=o_prod.product, batch=o_prod.batch, is_retail=o_prod.is_retail)
                product.amount = product.amount - o_prod.amount
                product.save()

        order.save()

        return HttpResponseRedirect(
            reverse(
                'ordersapp:order_detail',
                kwargs={
                    'pk': pk}))


@login_required
def set_for_delivery(request, pk):
    order = get_object_or_404(OrderList, pk=pk)
    if request.method == 'GET':
        if order.for_delivery:
            order.for_delivery = False
            ride = get_object_or_404(RideList, order=order)
            ride.delete()
        else:
            order.for_delivery = True

            if order.tk:
                ride_adr = order.tk
            else:
                ride_adr = order.partner.address
            ride = RideList(
                title='Доставка пленки',
                address=ride_adr,
                order=order,
            )
            ride.save()
        order.save()

        return HttpResponseRedirect(
            reverse(
                'ordersapp:order_detail',
                kwargs={
                    'pk': pk}))


class OrderProductCreate(LoginRequiredMixin, CreateView):
    model = OrderProductsList
    form_class = OrderProductForm
    template_name = 'ordersapp/order_product_create.html'

    def form_valid(self, form):
        order = OrderList.objects.get(pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.order = order
        self.object.save()

        return HttpResponseRedirect(
            reverse(
                'ordersapp:order_detail',
                kwargs={
                    'pk': order.pk}))


@login_required
def order_product_delete(request, pk):
    product = get_object_or_404(OrderProductsList, pk=pk)
    if request.method == 'GET':
        product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def order_product_update(request, order_pk, good_pk):
    object = get_object_or_404(OrderProductsList, pk=good_pk)

    if request.method == 'POST':

        retail = request.POST.getlist('is_retail')
        if len(retail) > 0:
            object.is_retail = True
        else:
            object.is_retail = False

        b_slug = request.POST.get('batch').split('-')[1]
        batch = get_object_or_404(BatchList, slug=b_slug)
        amount = float(request.POST.get('amount').replace(',', '.'))

        object.batch = batch
        object.amount = amount

        object.save()

        return HttpResponseRedirect(reverse('ordersapp:order_detail', kwargs={'pk': order_pk}))

    context = {
        'title': 'Редактирование товара',
        'object': object,
    }
    return render(request, 'ordersapp/order_product_crud.html', context)


@login_required
def statistics(request):
    clients = PartnersList.objects.all()
    selected_client = request.POST.get('client_list')
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    objects = None
    calc_objects = None

    if selected_client:
        partner = PartnersList.objects.get(name=selected_client.split('|')[1].strip())
    else:
        partner = ''

    if date_to == '':
        date_to = date.today().strftime("%Y-%m-%d")
    if date_from == '':
        date_from = date(2020, 1, 1).strftime("%Y-%m-%d")

    if request.method == 'POST':
        if partner == '':
            calc_objects = OrderProductsList.objects.filter(order__shipped_date__gte=date_from,
                                                            order__shipped_date__lte=date_to,
                                                            is_retail=False)
            if len(calc_objects) > 0:
                objects = count_sold_products(calc_objects)
        else:
            calc_objects = OrderProductsList.objects.filter(order__partner=partner,
                                                            order__shipped_date__gte=date_from,
                                                            order__shipped_date__lte=date_to,
                                                            is_retail=False)
            if len(calc_objects) > 0:
                objects = count_sold_products(calc_objects)

    if calc_objects:
        total_sold = calc_objects.aggregate(Sum('amount'))

        tot = 0

        for key in total_sold:
            tot = total_sold[key]
    else:
        tot = 0

    context = {
        'objects': objects,
        'clients': clients,
        'partner': partner,
        'date_from': date_from,
        'date_to': date_to,
        'total_sold': int(tot),
    }

    return render(request, 'ordersapp/statistic.html', context)
