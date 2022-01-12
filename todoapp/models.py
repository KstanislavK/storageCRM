from django.db import models
from django.urls import reverse
from slugify import slugify


class ToDoList(models.Model):
    date = models.DateTimeField(verbose_name='Дата', auto_now=True)
    user_posted = models.CharField(verbose_name='Пользователь', max_length=64, default='admin')
    title = models.CharField(verbose_name='Заголовок', max_length=128)
    text = models.TextField(verbose_name='Текст', max_length=512)
    is_active = models.BooleanField(verbose_name='Активное', default=True)
    slug = models.SlugField(verbose_name='URL', unique=True, max_length=255)

    class Meta:
        ordering = ('-is_active', '-date',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ToDoList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('todoapp:update', kwargs={'slug': self.slug})
