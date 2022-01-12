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
        return reverse('partnersapp:update', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    description = models.CharField(
        verbose_name='Описание', max_length=256, blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('partnersapp:update', kwargs={'slug': self.slug})
