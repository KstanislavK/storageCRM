from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from .forms import NewRideForm, NewMileageForm
from .models import RideList, MileageList, CarList


@login_required
def get_ride_list(request):
    objects = RideList.objects.all()
    paginator = Paginator(objects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'objects': page_obj,
        'title': 'Поездки',
    }
    return render(request, 'transportapp/index.html', context)


class RideActiveListView(LoginRequiredMixin, ListView):
    """ Общий вывод активных поездок """
    model = RideList
    template_name = 'transportapp/index.html'
    context_object_name = 'objects'
    paginate_by = 20

    def get_queryset(self):
        return RideList.objects.filter(delivered=False)

    def get_context_data(self, **kwargs):
        context = super(RideActiveListView, self).get_context_data(**kwargs)
        context['title'] = 'Поездки в работе'
        return context


class RideCreateView(LoginRequiredMixin, CreateView):
    model = RideList
    template_name = 'transportapp/ride_crud_form.html'
    form_class = NewRideForm

    def get_context_data(self, **kwargs):
        context = super(RideCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Новая поездка'
        return context


@login_required
def set_delivered(request, pk):
    ride = get_object_or_404(RideList, pk=pk)
    if request.method == 'GET':
        if ride.delivered:
            ride.delivered = False
        else:
            ride.delivered = True
            ride.delivered_at = datetime.now()
        ride.save()

        return HttpResponseRedirect(
            reverse('transportapp:index')
        )


@login_required
def ride_delete(request, pk):
    ride = get_object_or_404(RideList, pk=pk)
    if request.method == 'GET':
        ride.delete()
        return HttpResponseRedirect(
            reverse('transportapp:index')
        )


class MileageListView(LoginRequiredMixin, ListView):
    model = MileageList
    template_name = 'transportapp/mileage.html'
    context_object_name = 'objects'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(MileageListView, self).get_context_data(**kwargs)
        context['title'] = 'Записи пробегов'
        context['cars'] = CarList.objects.all()
        return context


class MileageCreateView(LoginRequiredMixin, CreateView):
    model = MileageList
    template_name = 'transportapp/ride_crud_form.html'
    form_class = NewMileageForm

    def get_context_data(self, **kwargs):
        context = super(MileageCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Новая запись пробега'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        car = form.instance.car
        km_start = form.instance.car.km_real
        km_end = form.instance.km_end
        self.object.km_start = km_start
        self.object.km_amount = km_end - km_start
        self.object.consumption = (car.consumption * self.object.km_docs) / 100
        self.object.save()
        car.km_real = km_end
        car.km_docs = car.km_docs + form.instance.km_docs
        car.save()

        return HttpResponseRedirect(reverse('transportapp:mileage_list'))


def delete_mileage(request, pk):
    post = get_object_or_404(MileageList, pk=pk)
    car = post.car

    car.km_docs = car.km_docs - post.km_docs
    car.km_real = post.km_start

    car.save()
    post.delete()

    return HttpResponseRedirect(reverse('transportapp:mileage_list'))


