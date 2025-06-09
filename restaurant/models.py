import uuid
from django.db import models

#Table Model
class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    qr_code = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    capacity = models.IntegerField(default=4)
    is_occupied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    #uuid lew kunai empty xa vane automaitcally stirng haru generate garxa mathi like [11hjhjdkhf-dhhfjh]
    
    def __str__(self):
        return f"Table {self.table_number}"
    

#Category Model
class Category(models.Model):
    CATEGORY_CHOICES = [
        ('starters', 'Starters'),
        ('mains', 'Mains'),
        ('desserts', 'Desserts'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.display_name
    
#MenuItem Model   
class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    preparation_time = models.IntegerField(help_text="Preparation time in minutes")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.category.display_name}"
    
#Order Model
class Order(models.Model):
     ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ]
     order_id = models.UUIDField(default=uuid.uuid4, editable=False,unique= True)
     table = models.ForeignKey(Table, on_delete=models.CASCADE)
     customer_name= models.CharField(max_length=100,blank=True)
     status = models.CharField(max_length=20,choices=ORDER_STATUS,default='pending')
     total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
     notes = models.TextField(blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
         ordering =['-created_at']

     def __str__(self):
        return f"Order {self.order_id} - Table {self.table.table_number}"
     

#OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price at time of order
    special_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    @property
    def subtotal(self):
        return self.quantity * self.price

    















