from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

class FeeRecord(models.Model):
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='fee_records')
    batch = models.ForeignKey('courses.Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='fee_records')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='fee_records')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    @property
    def remaining_balance(self):
        return max(Decimal('0.00'), self.total_fee - self.amount_paid)

    def __str__(self):
        return f"{self.student.username} - Fee: {self.total_fee}, Remaining: {self.remaining_balance}"

    def update_student_outstanding(self):
        # Update outstandingFees in StudentProfile when this changes
        if hasattr(self.student, 'student_profile'):
            # Calculate total remaining across all records for this student
            total_remaining = sum(record.remaining_balance for record in self.student.fee_records.all())
            self.student.student_profile.outstandingFees = float(total_remaining)
            self.student.student_profile.save(update_fields=['outstandingFees'])

class PaymentTransaction(models.Model):
    fee_record = models.ForeignKey(FeeRecord, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='Cash')
    reference_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.fee_record.student.username} on {self.payment_date.strftime('%Y-%m-%d')}"

@receiver(post_save, sender=PaymentTransaction)
@receiver(post_delete, sender=PaymentTransaction)
def update_fee_record_amount_paid(sender, instance, **kwargs):
    # Recalculate amount paid whenever a transaction is added or deleted
    record = instance.fee_record
    total_paid = sum(t.amount for t in record.transactions.all())
    record.amount_paid = total_paid
    record.save(update_fields=['amount_paid'])
    # Update outstanding on profile
    record.update_student_outstanding()

@receiver(post_save, sender=FeeRecord)
def update_profile_on_fee_change(sender, instance, **kwargs):
    instance.update_student_outstanding()

# Create your models here.
