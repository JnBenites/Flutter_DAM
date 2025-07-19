# Django REST Framework Serializers

Este archivo define los serializers utilizados en la API para convertir instancias de modelos en formatos como JSON y viceversa. Utilizamos `ModelSerializer` de `rest_framework` para simplificar el proceso de serialización y deserialización.

## 📦 Serializers definidos

### 🔹 `UserSerializer`

Representa al modelo `User`. Se encarga de exponer datos básicos del usuario.

**Campos:**
- `id`: ID del usuario.
- `username`: Nombre de usuario.
- `email`: Correo electrónico.
- `first_name`: Nombre.
- `last_name`: Apellido.

---

### 🔹 `AccountSerializer`

Representa una cuenta financiera asociada a un usuario.

**Campos:**
- `id`: ID de la cuenta.
- `number`: Número único de cuenta.
- `balance`: Saldo disponible.
- `type`: Tipo de cuenta (ej. ahorro, corriente).
- `is_active`: Estado de la cuenta (activa/inactiva).

---

### 🔹 `TransactionSerializer`

Representa una transacción entre cuentas.

**Campos:**
- `id`: ID de la transacción.
- `from_account`: Cuenta de origen.
- `to_account`: Cuenta de destino.
- `type`: Tipo de transacción (depósito, retiro, transferencia, etc.).
- `amount`: Monto de la transacción.
- `created_at`: Fecha y hora de creación.
- `description`: Descripción o referencia.
- `status`: Estado de la transacción (pendiente, completada, fallida).

---

### 🔹 `PolicySerializer`

Representa una política financiera o de ahorro vinculada a una cuenta.

**Campos:**
- `id`: ID de la política.
- `account`: Cuenta asociada.
- `amount`: Monto invertido o asegurado.
- `term`: Plazo en días o meses.
- `interest`: Porcentaje de interés.
- `start_date`: Fecha de inicio.
- `end_date`: Fecha de finalización.
- `status`: Estado actual de la política (activa, vencida, cancelada).

---

## 📁 Ubicación

Archivo: `serializers.py`  
Módulo relacionado: `from rest_framework import serializers`

---

## 🚀 Uso típico en vistas

Estos serializers se utilizan en las vistas basadas en clase (CBV) o vistas API para convertir datos del modelo en JSON y validar entradas:

```python
from .serializers import UserSerializer, AccountSerializer
