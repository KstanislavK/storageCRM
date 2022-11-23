from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from todoapp.models import ToDoList


@login_required
def index(request):
    todo_block = ToDoList.objects.filter(is_active=True).order_by('-id')[0:4]
    context = {
        'todo_objects': todo_block,
        'title': 'Система управления складом'
    }
    return render(request, 'mainapp/index.html', context)
