from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .additional_functions import do_backup
from ordersapp.models import OrderList
from todoapp.models import ToDoList


@login_required
def index(request):
    todo_block = ToDoList.objects.filter(is_active=True).order_by('-id')[0:4]
    order_list = OrderList.objects.filter(shipped=False)
    context = {
        'todo_objects': todo_block,
        'title': 'Система управления складом',
        'order_objects': order_list,
    }
    return render(request, 'mainapp/index.html', context)


@login_required
def back_up(request):

    do_backup()

    return HttpResponseRedirect(reverse('mainapp:index'))


