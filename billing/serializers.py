from rest_framework import serializers
from .models import FeeRecord, PaymentTransaction
from accounts.models import User

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'
        read_only_fields = ('payment_date',)

class FeeRecordSerializer(serializers.ModelSerializer):
    transactions = PaymentTransactionSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    batch_name = serializers.CharField(source='batch.name', read_only=True)
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = FeeRecord
        fields = '__all__'
