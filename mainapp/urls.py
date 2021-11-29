from django.urls import path

from .views import index

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='index'),
    # path('create/', TodoCreateView.as_view(), name='create'),
    # path('complete/<int:pk>', todo_complete, name='complete'),
    # path('delete/<int:pk>', todo_delete, name='delete'),
    # path('update/<int:pk>', TodoUpdateView.as_view(), name='update'),
]
