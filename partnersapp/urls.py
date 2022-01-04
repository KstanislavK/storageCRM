from django.urls import path

from .views import PartnersListView, PartnersCreateView, partner_active, PartnersUpdateView

app_name = 'partnersapp'

urlpatterns = [
    path('', PartnersListView.as_view(), name="index"),
    path('create/', PartnersCreateView.as_view(), name='create'),
    path('complete/<int:pk>', partner_active, name='active'),
    path('update/<int:pk>', PartnersUpdateView.as_view(), name='update'),
]

