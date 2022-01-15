from django.db import models
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    description = models.CharField(verbose_name='Описание', max_length=256, blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:category_update', kwargs={'slug': self.slug})


class Batch(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    delivery_date = models.DateField(verbose_name='Дата разгрузки')
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Партия'
        verbose_name_plural = 'Партии'
        ordering = ['delivery_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Batch, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:batch_update', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    description = models.CharField(verbose_name='Описание', max_length=256, blank=True, null=True)
    batch = models.ForeignKey(Batch, verbose_name='Партия', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    # todo переделать определение конечного продукта
    # todo создать номенклатуру товара, из нее подтягивать сюда остальное

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.batch}')
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:product_update', kwargs={'slug': self.slug})
