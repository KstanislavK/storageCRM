from django.urls import path

from todoapp.views import TodoListView, TodoCreateView, todo_complete, todo_delete, TodoUpdateView

app_name = 'todoapp'

urlpatterns = [
    path('', TodoListView.as_view(), name='index'),
    path('create/', TodoCreateView.as_view(), name='create'),
    path('complete/<slug:slug>', todo_complete, name='complete'),
    path('delete/<slug:slug>', todo_delete, name='delete'),
    path('update/<slug:slug>', TodoUpdateView.as_view(), name='update'),
]
