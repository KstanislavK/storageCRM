from django.contrib import admin

from transportapp.models import RideList, MileageList, CarList


@admin.register(RideList)
class RideListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'title', 'delivered')
    list_display_links = ('pk', 'created_at', 'title', 'delivered')
    search_fields = ('pk', 'created_at', 'title', 'delivered')


@admin.register(MileageList)
class RideListAdmin(admin.ModelAdmin):
    pass


@admin.register(CarList)
class RideListAdmin(admin.ModelAdmin):
    pass
