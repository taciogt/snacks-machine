from django.contrib import admin
from snacks.models import SnackModel


@admin.register(SnackModel)
class SnackAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available_quantity')
