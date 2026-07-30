from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeRecordViewSet, PaymentTransactionViewSet

router = DefaultRouter()
router.register('records', FeeRecordViewSet, basename='feerecord')
router.register('payments', PaymentTransactionViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
