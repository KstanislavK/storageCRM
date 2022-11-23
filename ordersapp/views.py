from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .forms import SearchForm, NewOrderForm, UpdateOrderForm, OrderProductForm
from .models import OrderList, OrderProductsList


def get_order_list(request):
    objects = OrderList.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            search_results = []
            data_for_search = form.data['data_for_search']

            if data_for_search.isdigit():
                search_results = list(OrderList.objects.filter(pk=int(data_for_search)))
            search_results = set(list(OrderList.objects.filter(partner__partner_city__contains=data_for_search)) +
                                 list(OrderList.objects.filter(partner__name__contains=data_for_search)) +
                                 list(OrderList.objects.filter(partner__address__contains=data_for_search)) +
                                 list(OrderList.objects.filter(tk__name__contains=data_for_search)) +
                                 search_results)
            context = {
                'objects': search_results,
                'form': form,
            }
            return render(request, 'ordersapp/index.html', context)
    context = {
        'objects': objects,
    }
    return render(request, 'ordersapp/index.html', context)


class OrderActiveListView(ListView):
    """ Общий вывод активных заказов """
    model = OrderList
    template_name = 'ordersapp/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return OrderList.objects.filter(shipped=False)

    def get_context_data(self, **kwargs):
        context = super(OrderActiveListView, self).get_context_data(**kwargs)
        context['title'] = 'Заказы в работе'
        return context


class OrderDetailView(DetailView):
    model = OrderList
    template_name = 'ordersapp/order_detail.html'
    context_object_name = 'object'


class OrderCreateView(CreateView):
    model = OrderList
    template_name = 'ordersapp/order_crud_form.html'
    form_class = NewOrderForm

    # def form_valid(self, form):
    #     form.instance.user_creator = self.request.user
    #     return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(UpdateView):
    model = OrderList
    template_name = 'ordersapp/order_crud_form.html'
    form_class = UpdateOrderForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('ordersapp:order_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование заказа'
        return context


def order_delete(request, pk):
    order = get_object_or_404(OrderList, pk=pk)
    if request.method == 'GET':
        order.delete()
    return HttpResponseRedirect(reverse('ordersapp:index'))


def set_payed(request, pk):
    order = get_object_or_404(OrderList, pk=pk)
    if request.method == 'GET':
        if order.payed:
            order.payed = False
        else:
            order.payed = True
        order.save()

        return HttpResponseRedirect(reverse('ordersapp:order_detail', kwargs={'pk': pk}))


class OrderProductCreate(CreateView):
    model = OrderProductsList
    form_class = OrderProductForm
    template_name = 'ordersapp/order_product_create.html'

    def form_valid(self, form):
        order = OrderList.objects.get(pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.order = order
        self.object.save()

        return HttpResponseRedirect(reverse('ordersapp:order_detail', kwargs={'pk': order.pk}))


def order_product_delete(request, pk):
    product = get_object_or_404(OrderProductsList, pk=pk)
    if request.method == 'GET':
        product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
