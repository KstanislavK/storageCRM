from django.contrib import admin
from django.urls import path, include

from todoapp.views import TodoListView, TodoCreateView, todo_complete, todo_delete

app_name = 'todoapp'

urlpatterns = [
    path('', TodoListView.as_view(), name='index'),
    path('create/', TodoCreateView.as_view(), name='create'),
    path('complete/<int:pk>', todo_complete, name='complete'),
    path('delete/<int:pk>', todo_delete, name='delete'),
]

# прямые url - временное решение для отладки
