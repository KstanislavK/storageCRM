from django.db import models


class PartnersList(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    partner_city = models.CharField(verbose_name='Город', max_length=128, default='Москва')
    contact_person = models.CharField(verbose_name='Контактное лицо', max_length=256, null=True, blank=True)
    contact_phone = models.CharField(verbose_name='Контактный телефон', max_length=12, null=True, blank=True)
    contact_email = models.EmailField(verbose_name='Контактный email', max_length=48, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __str__(self):
        return self.name
