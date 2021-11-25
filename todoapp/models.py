from django.db import models


class ToDoList(models.Model):
    date = models.DateField(verbose_name='Дата', auto_now=True)
    title = models.CharField(verbose_name='Заголовок', max_length=128)
    text = models.TextField(verbose_name='Текст', max_length=512)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title
