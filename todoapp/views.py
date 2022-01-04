from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from .models import ToDoList


class TodoListView(ListView):
    model = ToDoList
    template_name = 'todoapp/index.html'
    context_object_name = 'todo_objects'

    def get_queryset(self):
        return ToDoList.objects.all()

    def get_context_data(self):
        context = super(TodoListView, self).get_context_data()
        context['title'] = 'Задачи'
        return context


class TodoCreateView(CreateView):
    model = ToDoList
    template_name = 'todoapp/todo_crud_form.html'
    context_object_name = 'todo_objects'
    success_url = reverse_lazy('todoapp:index')
    fields = '__all__'

    def get_context_data(self):
        context = super(TodoCreateView, self).get_context_data()
        context.update({'title': 'Добавить задание'})
        return context


class TodoUpdateView(UpdateView):
    model = ToDoList
    template_name = 'todoapp/todo_crud_form.html'
    success_url = reverse_lazy('todoapp:index')
    # success_url = reverse_lazy('todoapp:update', kwargs={'pk': model.pk})
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(TodoUpdateView, self).get_context_data(**kwargs)
        context.update({'title': 'Редактирование задания'})
        return context


def todo_complete(request, pk):
    task = get_object_or_404(ToDoList, pk=pk)

    if request.method == 'GET':
        if task.is_active:
            task.is_active = False
        else:
            task.is_active = True

        task.save()

        return HttpResponseRedirect(reverse('todoapp:index'))


def todo_delete(request, pk):
    task = get_object_or_404(ToDoList, pk=pk)
    task.delete()
    return HttpResponseRedirect(reverse('todoapp:index'))
