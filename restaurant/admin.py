from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'is_occupied', 'qr_code']
    list_filter = ['is_occupied']
    readonly_fields = ['qr_code']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'is_active', 'order']
    list_filter = ['is_active']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name','category','price','is_available','rating']
    list_filter = ['category','is_available','is_vegetarian','is_vegan']
    search_fields = ['name','description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','table','customer_name','status','total_amount','created_at']
    list_filter=['status','created_at']
    search_fields= ['order_id','customer_name']
    inlines = [OrderItemInline]
    readonly_fields = ['order_id']
