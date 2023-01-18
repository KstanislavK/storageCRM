from django.contrib import admin

from .models import ToDoList


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('date', 'user_posted', 'title', 'is_active', 'slug')
    list_filter = ('date', 'user_posted', 'is_active')
    search_fields = ('date', 'user_posted', 'title', 'slug')
    prepopulated_fields = {'slug': ('title', )}

