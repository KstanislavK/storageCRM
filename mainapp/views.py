from django.shortcuts import render

from todoapp.models import ToDoList


def index(request):
    todo_block = ToDoList.objects.filter(is_active=True).order_by('-id')[0:4]
    context = {
        'todo_objects': todo_block,
    }
    return render(request, 'mainapp/index.html', context)
