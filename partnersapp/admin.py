from django.contrib import admin
from .models import PartnersList


@admin.register(PartnersList)
class PartnersListAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_city', 'contact_person', 'contact_phone', 'slug')
    list_filter = ('name', 'partner_city')
    search_fields = ('name', 'partner_city', 'contact_person', 'contact_phone')
    prepopulated_fields = {'slug': ('name', )}
