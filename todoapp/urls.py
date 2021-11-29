from django.contrib import admin
from django.urls import path, include

from todoapp.views import TodoListView, TodoCreateView, todo_complete, todo_delete, TodoUpdateView

app_name = 'todoapp'

urlpatterns = [
    path('', TodoListView.as_view(), name='index'),
    path('create/', TodoCreateView.as_view(), name='create'),
    path('complete/<int:pk>', todo_complete, name='complete'),
    path('delete/<int:pk>', todo_delete, name='delete'),
    path('update/<int:pk>', TodoUpdateView.as_view(), name='update'),
]

# прямые url - временное решение для отладки
