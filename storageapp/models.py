from django.db import models
from django.urls import reverse
from slugify import slugify
from django.db.models import Sum


class CategoryList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    description = models.CharField(verbose_name='Описание', max_length=256, blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        db_table = 'product_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(CategoryList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:category_update', kwargs={'slug': self.slug})

    def get_products_amount_by_category(self):
        dict_1 = ProductList.objects.filter(name__category=self.pk, is_active=True).aggregate(Sum('amount'))
        for key in dict_1:
            if dict_1[key] is None:
                return 0
            return dict_1[key]


class BatchList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    delivery_date = models.DateField(verbose_name='Дата разгрузки')
    products_json = models.JSONField(verbose_name='Поступившие товары', blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        db_table = "product_batch"
        verbose_name = 'Партия'
        verbose_name_plural = 'Партии'
        ordering = ['delivery_date']

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(BatchList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:batch_update', kwargs={'slug': self.slug})


class MakerList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    country = models.CharField(verbose_name='СТрана', max_length=64)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        db_table = "product_maker"
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        ordering = ['name']

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(MakerList, self).save(*args, **kwargs)


class NomenList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    part_number = models.CharField(verbose_name='Артикул', max_length=32)
    category = models.ForeignKey(CategoryList, verbose_name='Категория',
                                 on_delete=models.CASCADE, related_name='nomen')
    maker = models.ForeignKey(MakerList, verbose_name='Производитель',
                              on_delete=models.CASCADE, related_name='nomen')
    description = models.CharField(verbose_name='Описание', max_length=512, blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        db_table = "nomen_list"
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатуры'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(NomenList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:nomen_update', kwargs={'slug': self.slug})

    def get_quantity(self):
        dict_1 = ProductList.objects.filter(name=self.pk, is_active=True).aggregate(Sum('amount'))
        for key in dict_1:
            if dict_1[key] is None:
                return 0
            return dict_1[key]

    def get_prod_batches(self):
        return ProductList.objects.filter(name=self.pk, is_active=True)


class ProductList(models.Model):
    name = models.ForeignKey(NomenList, verbose_name='Название',
                             on_delete=models.CASCADE, max_length=128, related_name='product')
    batch = models.ForeignKey(BatchList, verbose_name='Партия', on_delete=models.CASCADE, related_name='products')
    amount = models.IntegerField(verbose_name='Количество')
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        db_table = "product_list"
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', 'batch']

    def __str__(self):
        return self.name.name or ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name.name}-{self.batch}')
        super(ProductList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('storageapp:product_update', kwargs={'slug': self.slug})

    def get_product_sum(self):
        dict_1 = ProductList.objects.filter(name=self.name, is_active=True).aggregate(Sum('amount'))
        for key in dict_1:
            return dict_1[key]

    @staticmethod
    def get_all_products_amount(self):
        dict_1 = ProductList.objects.filter(is_active=True).aggregate(Sum('amount'))
        for key in dict_1:
            return dict_1[key]

    def get_product_batches(self):
        prods = ProductList.objects.filter(name=self.name, is_active=True)
        prods_by_batch = {}
        for item in prods:
            prods_by_batch[item.batch] = item.amount
        return prods_by_batch


