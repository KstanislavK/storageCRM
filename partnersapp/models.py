from django.db import models
from django.urls import reverse
from slugify import slugify


class PartnersList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    partner_city = models.CharField(verbose_name='Город', max_length=128, default='Москва')
    contact_person = models.CharField(verbose_name='Контактное лицо', max_length=256, null=True, blank=True)
    contact_phone = models.CharField(verbose_name='Контактный телефон', max_length=12, null=True, blank=True)
    contact_email = models.EmailField(verbose_name='Контактный email', max_length=48, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True)

    class Meta:
        db_table = 'partnerslist'
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(PartnersList, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('partnersapp:update', kwargs={'slug': self.slug})
