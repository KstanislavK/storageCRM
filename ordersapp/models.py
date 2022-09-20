from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from partnersapp.models import PartnersList
from storageapp.models import NomenList, BatchList, ProductList


class TKList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    logo = models.URLField(verbose_name='ссылка на картинку', blank=True)

    class Meta:
        db_table = 'TK_list'
        verbose_name = ("Транспортная")
        verbose_name_plural = ("Транспортные")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("TK_detail", kwargs={"pk": self.pk})


class OrderList(models.Model):

    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True)
    partner = models.ForeignKey(
        PartnersList,
        on_delete=models.PROTECT,
        verbose_name='Контрагент',
        related_name='orderlist')
    self_pickup = models.BooleanField(verbose_name='Самовывоз', default=False)
    tk = models.ForeignKey(
        TKList,
        verbose_name='Транспортная',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    payed = models.BooleanField(verbose_name='Оплачен', default=False)
    shipped = models.BooleanField(verbose_name='Отгружено', default=False)
    shipped_date = models.DateField(
        verbose_name='Дата отгрузки', blank=True, null=True)
    for_delivery = models.BooleanField(verbose_name='На доставку', default=False)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    user_creator = models.ForeignKey(
        User,
        verbose_name='Создатель',
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        db_table = 'order_list'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['shipped', '-shipped_date', '-created_at', '-pk']

    def __str__(self):
        return f'№{self.pk} от {self.created_at}, {self.partner.name}'

    def get_absolute_url(self):
        return reverse('ordersapp:order_detail', kwargs={'pk': self.pk})

    def get_order_products_list(self):
        return OrderProductsList.objects.filter(order=self.pk)


class OrderProductsList(models.Model):
    product = models.ForeignKey(
        NomenList,
        on_delete=models.PROTECT,
        verbose_name='Товар',
        related_name='orderproduct')
    order = models.ForeignKey(
        OrderList,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='orderproduct_o')
    batch = models.ForeignKey(BatchList, on_delete=models.CASCADE, verbose_name='Партия', related_name='batches_o', blank=True, null=True)
    is_retail = models.BooleanField(verbose_name='Нарезка', default=False)
    amount = models.FloatField(verbose_name='Количество')

    class Meta:
        db_table = 'orderproductlist'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse('ordersapp:order_detail', kwargs={'pk': self.pk})

    def get_prod_by_product(self):
        products = ProductList.objects.filter(name__name=self.product)
        return products

    def get_batches_by_product(self):
        return ProductList.objects.filter(name__name=self.product.name, is_active=True)
