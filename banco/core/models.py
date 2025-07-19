from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    number = models.CharField(max_length=20, unique=True)
    balance = models.FloatField(default=0)
    type = models.CharField(max_length=20)  # 'savings', 'checking'
    is_active = models.BooleanField(default=True)

class Transaction(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing', null=True, blank=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incoming', null=True, blank=True)
    type = models.CharField(max_length=20)  # 'deposit', 'withdraw', 'transfer'
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='completed')

class Policy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policies')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    term = models.IntegerField()  # días
    interest = models.FloatField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active')