from django.db import models
from django.urls import reverse
from slugify import slugify
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    description = models.CharField(verbose_name='Описание', max_length=256, blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        db_table = 'product_category'
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
        db_table = "product_batch"
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


class Nomenclature(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    part_number = models.CharField(verbose_name='Артикул', max_length=32)
    description = models.CharField(verbose_name='Описание', max_length=256, blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_nomenclature'
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатуры'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def get_slug(self):
        return Product.objects.filter(name=self.pk)[0].slug

    def get_quantity(self):
        dict_1 = Product.objects.filter(name=self.pk).aggregate(Sum('quantity'))
        for key in dict_1:
            return dict_1[key]


class Product(models.Model):
    name = models.ForeignKey(Nomenclature, verbose_name='Название', on_delete=models.CASCADE, related_name='products')
    batch = models.ForeignKey(Batch, verbose_name='Партия', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество', default=0)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name.name}-{self.batch.name}')
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:product_update', kwargs={'slug': self.slug})

    def get_product_sum(self):
        dict_1 = Product.objects.filter(name=self.name).aggregate(Sum('quantity'))
        for key in dict_1:
            return dict_1[key]

    def get_batches_of_product(self):
        prods = Product.objects.filter(name=self.name)
        prods_by_batch = {}
        for item in prods:
            prods_by_batch[item.batch] = item.quantity
        return prods_by_batch
