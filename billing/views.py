from rest_framework import viewsets, permissions
from .models import FeeRecord, PaymentTransaction
from .serializers import FeeRecordSerializer, PaymentTransactionSerializer

class FeeRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FeeRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = FeeRecord.objects.all()
        # Filter by course/batch if provided
        course = self.request.query_params.get('course', None)
        batch = self.request.query_params.get('batch', None)
        
        if course:
            queryset = queryset.filter(course_id=course)
        if batch:
            queryset = queryset.filter(batch_id=batch)
            
        # If student, only see own
        if hasattr(self.request.user, 'role') and self.request.user.role == 'student':
            queryset = queryset.filter(student=self.request.user)
            
        return queryset

class PaymentTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = PaymentTransaction.objects.all()
        # If student, only see own
        if hasattr(self.request.user, 'role') and self.request.user.role == 'student':
            queryset = queryset.filter(fee_record__student=self.request.user)
        return queryset
