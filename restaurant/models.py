import uuid
from django.db import models

# Create your models here.
class Table(models.Model):
    table_number = models.CharField(max_length=10, unique=True)
    qr_code = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    capacity = models.IntegerField(default=4)
    is_occupied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    #uuid lew kunai empty xa vane automaitcally stirng haru generate garxa mathi like [11hjhjdkhf-dhhfjh]
    
    def __str__(self):
        return f"Table {self.table_number}"