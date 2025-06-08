from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'is_occupied', 'qr_code']
    list_filter = ['is_occupied']
    readonly_fields = ['qr_code']