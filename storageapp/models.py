from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    description = models.CharField(verbose_name='Описание', max_length=256, blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    description = models.CharField(
        verbose_name='Описание', max_length=256, blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name
