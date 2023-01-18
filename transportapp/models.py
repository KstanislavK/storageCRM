from django.db import models
from django.urls import reverse

from ordersapp.models import OrderList


class RideList(models.Model):
    title = models.CharField(verbose_name='Цель', max_length=256)
    address = models.CharField(verbose_name='Адрес', max_length=256, blank=True)
    order = models.OneToOneField(OrderList, verbose_name='Заказ', on_delete=models.PROTECT, blank=True, null=True, related_name='ridelist')
    description = models.TextField(verbose_name='Описание', blank=True)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    delivered = models.BooleanField(verbose_name='Доставлено', default=False)
    delivered_at = models.DateTimeField(verbose_name='Дата доставки', blank=True, null=True)

    class Meta:
        db_table = 'ridelist'
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('transportapp:index')


class CarList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    km_real = models.PositiveIntegerField(verbose_name='Пробег (ОДО)')
    km_docs = models.PositiveIntegerField(verbose_name='Пробег (ДОК)')
    consumption = models.PositiveIntegerField(verbose_name='Расход на 100 км')
    gos_num = models.CharField(verbose_name='Гос Номер', max_length=10, blank=True)
    sts = models.CharField(verbose_name='Гос Номер', max_length=20, blank=True)

    class Meta:
        db_table = 'carlist'
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f'{self.name}, {self.gos_num}'

    def get_absolute_url(self):
        return reverse('transportapp:index')


class MileageList(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата')
    car = models.ForeignKey(CarList, verbose_name='Машина', on_delete=models.PROTECT)
    km_start = models.PositiveIntegerField(verbose_name='Пробег (Начало)')
    km_end = models.PositiveIntegerField(verbose_name='Пробег (Конец)')
    km_amount = models.PositiveIntegerField(verbose_name='Пробег (За день)', default=0)
    km_docs = models.PositiveIntegerField(verbose_name='Пробег (Док)')
    consumption = models.PositiveIntegerField(verbose_name='Расход за день')
    comment = models.CharField(verbose_name='Комментарий', max_length=512, blank=True)

    class Meta:
        db_table = 'mileagelist'
        verbose_name = 'Пробег'
        verbose_name_plural = 'Пробеги'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.car.name}, {self.created_at}'

    def get_absolute_url(self):
        return reverse('transportapp:index')
