# models.py
from django.db import models
from django.contrib.auth.models import User

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_symbol = models.CharField(max_length=10)
    share_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    broker_rate = models.DecimalField(max_digits=5, decimal_places=2)
