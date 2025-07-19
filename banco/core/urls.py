from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet, PolicyViewSet, user_profile
from django.urls import path

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'policies', PolicyViewSet, basename='policy')

urlpatterns = router.urls + [
    path('me/', user_profile, name='user_profile'),
]