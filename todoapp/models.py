from django.db import models


class ToDoList(models.Model):
    date = models.DateTimeField(verbose_name='Дата', auto_now=True)
    user_posted = models.CharField(verbose_name='Пользователь', max_length=64, default='admin')
    title = models.CharField(verbose_name='Заголовок', max_length=128)
    text = models.TextField(verbose_name='Текст', max_length=512)
    is_active = models.BooleanField(verbose_name='Активное', default=True)

    class Meta:
        ordering = ('-is_active', '-date',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title
