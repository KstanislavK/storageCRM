from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .models import ToDoList


class TodoListView(ListView):
    model = ToDoList
    template_name = 'todoapp/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return ToDoList.objects.all()

    def get_context_data(self):
        context = super(TodoListView, self).get_context_data()
        return context


class TodoCreateView(CreateView):
    model = ToDoList
    template_name = 'todoapp/todo_create.html'
