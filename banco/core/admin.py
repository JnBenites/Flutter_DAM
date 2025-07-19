from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Transaction, Policy

# Configuración del usuario personalizado
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Configuración de cuentas bancarias
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'type', 'balance', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('number', 'user__username', 'user__email')
    list_editable = ('balance', 'is_active')
    readonly_fields = ('number',)  # El número de cuenta no se puede editar una vez creado
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un objeto nuevo
            # Generar número de cuenta automáticamente si no existe
            if not obj.number:
                import random
                obj.number = f"{random.randint(1000000000, 9999999999)}"
        super().save_model(request, obj, form, change)

# Configuración de transacciones
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'from_account', 'to_account', 'amount', 'status', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('from_account__number', 'to_account__number', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        # Mostrar todas las transacciones para superusuarios
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Para staff, mostrar solo transacciones relacionadas con sus cuentas
        return qs.filter(from_account__user=request.user)

# Configuración de pólizas
@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account', 'amount', 'term', 'interest', 'status', 'start_date')
    list_filter = ('status', 'start_date', 'term')
    search_fields = ('user__username', 'account__number')
    readonly_fields = ('start_date', 'end_date')
    list_editable = ('status',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un objeto nuevo
            # Calcular fecha de finalización automáticamente
            from datetime import datetime, timedelta
            if obj.start_date and obj.term:
                obj.end_date = obj.start_date + timedelta(days=obj.term)
        super().save_model(request, obj, form, change)