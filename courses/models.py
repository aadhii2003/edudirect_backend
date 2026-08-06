from django.db import models
from django.utils.text import slugify

class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    facility_location = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_column='dept_slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_MODES = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Hybrid', 'Hybrid'),
    )

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image_url = models.CharField(max_length=500, blank=True, null=True, help_text="URL to the course banner image")
    name = models.CharField(max_length=255)
    shortDescription = models.TextField()
    longDescription = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    mode = models.CharField(max_length=20, choices=COURSE_MODES)
    instructor = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_courses')
    duration = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    startDates = models.JSONField(default=list, help_text="List of start dates (strings)")
    certification = models.CharField(max_length=255)
    eligibility = models.TextField()
    syllabus = models.JSONField(default=list, help_text="List of syllabus modules")
    examPattern = models.TextField(blank=True, null=True)
    examSchedule = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    module_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.module_name} - {self.title} ({self.course.name})"

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Specific fee for this batch")
    mode = models.CharField(max_length=20, choices=Course.COURSE_MODES, default='Offline')
    main_instructor = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='instructed_batches')

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class ClassSchedule(models.Model):
    SCHEDULE_TYPES = (
        ('Specific Date', 'Specific Date'),
        ('Recurring', 'Recurring'),
    )
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='schedules', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    staff = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    room = models.CharField(max_length=100)
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES, default='Recurring')
    scheduled_date = models.DateField(null=True, blank=True, help_text="For specific date schedules")
    day_of_week = models.CharField(max_length=20, null=True, blank=True, help_text="For recurring schedules")
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_link = models.URLField(blank=True, null=True, help_text="Zoom/Google Meet link for online classes")

    def __str__(self):
        if self.schedule_type == 'Specific Date' and self.scheduled_date:
            return f"{self.subject.title} - {self.scheduled_date} {self.start_time} (Batch: {self.batch.name if self.batch else 'None'})"
        return f"{self.subject.title} - {self.day_of_week} {self.start_time} (Batch: {self.batch.name if self.batch else 'None'})"

class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    )
    schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('schedule', 'student', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.status} on {self.date}"

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=AttendanceRecord)
@receiver(post_delete, sender=AttendanceRecord)
def update_student_attendance(sender, instance, **kwargs):
    # Calculate percentage: (Present + Late) / Total * 100
    records = AttendanceRecord.objects.filter(student=instance.student)
    total = records.count()
    if total > 0:
        attended = records.filter(status__in=['Present', 'Late']).count()
        percentage = int((attended / total) * 100)
    else:
        percentage = 100
        
    if hasattr(instance.student, 'student_profile'):
        instance.student.student_profile.attendance = percentage
        instance.student.student_profile.save(update_fields=['attendance'])

