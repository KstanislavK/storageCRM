from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView

from .forms import PartnersForm
from .models import PartnersList


class PartnersListView(ListView):
    model = PartnersList
    template_name = 'partnersapp/index.html'
    context_object_name = 'partners_objects'

    def get_queryset(self):
        return PartnersList.objects.filter(is_active=True)

    def get_context_data(self):
        context = super(PartnersListView, self).get_context_data()
        context['title'] = 'Контрагенты'
        return context


class PartnersCreateView(CreateView):
    model = PartnersList
    template_name = 'partnersapp/partners_create_form.html'
    context_object_name = 'partners_objects'
    form_class = PartnersForm

    def get_context_data(self, **kwargs):
        context = super(PartnersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить контрагента'
        return context


class PartnersUpdateView(UpdateView):
    model = PartnersList
    form_class = PartnersForm
    template_name = 'partnersapp/partners_crud_form.html'
    success_url = reverse_lazy('partnersapp:index')

    def get_context_data(self, **kwargs):
        context = super(PartnersUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирования контрагента'
        context['obj'] = PartnersList.objects.get(slug=self.kwargs['slug'])
        return context


def partner_active(request, slug):
    partner = get_object_or_404(PartnersList, slug=slug)

    if request.method == 'GET':
        if partner.is_active:
            partner.is_active = False
        else:
            partner.is_active = True

        partner.save()

        return HttpResponseRedirect(reverse('partnersapp:index'))
