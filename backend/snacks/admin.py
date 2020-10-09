from django.contrib import admin
from snacks.models import Snack


@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
