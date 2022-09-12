from django.shortcuts import render

from ordersapp.models import OrderList
from todoapp.models import ToDoList


def index(request):
    todo_block = ToDoList.objects.filter(is_active=True).order_by('-id')[0:4]
    order_list = OrderList.objects.filter(shipped=False)
    context = {
        'todo_objects': todo_block,
        'title': 'Система управления складом',
        'order_objects': order_list,
    }
    return render(request, 'mainapp/index.html', context)
