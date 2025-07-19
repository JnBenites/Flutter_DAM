from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Account, Transaction, Policy
from .serializers import AccountSerializer, TransactionSerializer, PolicySerializer, UserSerializer
from django.db import transaction as db_transaction

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(from_account__user=self.request.user)

    @action(detail=False, methods=['post'])
    def transfer(self, request):
        from_account_id = request.data.get('from_account')
        to_account_id = request.data.get('to_account')
        amount = float(request.data.get('amount', 0))
        description = request.data.get('description', '')

        if from_account_id == to_account_id:
            return Response({'error': 'No puedes transferir a la misma cuenta.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_account = Account.objects.get(id=from_account_id, user=request.user)
            to_account = Account.objects.get(id=to_account_id)
        except Account.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if from_account.balance < amount:
            return Response({'error': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

        with db_transaction.atomic():
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            transaction = Transaction.objects.create(
                from_account=from_account,
                to_account=to_account,
                type='transfer',
                amount=amount,
                description=description or f'Transferencia a {to_account.number}',
                status='completed'
            )
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

class PolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Policy.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']
        if account.user != self.request.user:
            raise serializers.ValidationError("La cuenta no pertenece al usuario.")
        if account.balance < amount:
            raise serializers.ValidationError("Saldo insuficiente en la cuenta.")
        with db_transaction.atomic():
            account.balance -= amount
            account.save()
            serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Devuelve la información del usuario autenticado"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)