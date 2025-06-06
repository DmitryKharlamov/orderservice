from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()

class Tariff(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} — {self.tariff.name}'
