from django.shortcuts import render

from todoapp.models import ToDoList


def index(request):
    todo_block = ToDoList.objects.order_by('-id')[0:3]
    context = {
        'todo_objects': todo_block,
    }
    return render(request, 'mainapp/index.html', context)
