from rest_framework import serializers
from .models import User, Account, Transaction, Policy

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'number', 'balance', 'type', 'is_active']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'from_account', 'to_account', 'type', 'amount', 'created_at', 'description', 'status']

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['id', 'account', 'amount', 'term', 'interest', 'start_date', 'end_date', 'status']