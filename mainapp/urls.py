from django.urls import path

from .views import index, back_up

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='index'),
    path('backup/', back_up, name='backup'),
]
