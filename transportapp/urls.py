from django.urls import path

from .views import get_ride_list, RideActiveListView, RideCreateView, set_delivered, ride_delete, MileageListView, \
    MileageCreateView, delete_mileage

app_name = 'transportapp'

urlpatterns = [
    path('', get_ride_list, name='index'),
    path('active/', RideActiveListView.as_view(), name='active_rides'),
    path('create/', RideCreateView.as_view(), name='ride_create'),
    path('set_delivered/<int:pk>', set_delivered, name='ride_delivered'),
    path('delete/<int:pk>', ride_delete, name='ride_delete'),

    path('mileage/', MileageListView.as_view(), name='mileage_list'),
    path('mileage/create/', MileageCreateView.as_view(), name='mileage_create'),
    path('mileage/delete/<int:pk>', delete_mileage, name='mileage_delete'),
]
