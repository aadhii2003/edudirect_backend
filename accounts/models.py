from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Super Admin'
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'
        FACULTY = 'faculty', 'Faculty'
        STUDENT = 'student', 'Student'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='enrolled_students')
    batch = models.ForeignKey('courses.Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='enrolled_students')
    grade = models.CharField(max_length=10, blank=True, null=True)
    attendance = models.IntegerField(default=100)
    status = models.CharField(max_length=50, default='Active')
    enrollmentDate = models.DateField(auto_now_add=True)
    gpa = models.FloatField(default=0.0)
    outstandingFees = models.FloatField(default=0.0)
    
    # NEW: Delivery mode for this specific student
    enrollment_mode = models.CharField(max_length=20, choices=[('Online', 'Online'), ('Offline', 'Offline')], default='Offline')

    def __str__(self):
        return f"Profile: {self.user.username}"

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.ForeignKey('courses.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')

    def __str__(self):
        return f"Staff Profile: {self.user.username}"

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    department = models.ForeignKey('courses.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='faculty_members')
    title = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Professor, Assistant Lecturer")

    def __str__(self):
        return f"Faculty Profile: {self.user.username}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=StudentProfile)
def create_fee_record_for_student(sender, instance, created, **kwargs):
    if instance.batch:
        try:
            from billing.models import FeeRecord
            FeeRecord.objects.get_or_create(
                student=instance.user,
                batch=instance.batch,
                defaults={'course': instance.course, 'total_fee': instance.batch.fee}
            )
        except Exception as e:
            print(f"Error creating fee record: {e}")