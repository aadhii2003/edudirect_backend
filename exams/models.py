from django.db import models

class ScheduledExam(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Published', 'Published'),
    )
    title = models.CharField(max_length=255)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='exams')
    batch = models.ForeignKey('courses.Batch', on_delete=models.SET_NULL, null=True, blank=True, related_name='exams')
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    total_marks = models.IntegerField(default=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_exams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"

class Question(models.Model):
    TYPE_CHOICES = (
        ('MCQ', 'Multiple Choice'),
        ('Written', 'Written Answer'),
        ('Photo', 'Photo Upload'),
    )
    exam = models.ForeignKey(ScheduledExam, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='MCQ')
    question_text = models.TextField()
    marks = models.IntegerField(default=1)
    
    # For MCQ only
    options = models.JSONField(blank=True, null=True, help_text="List of options strings")
    correct_answer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.exam.title} - Q{self.id}"

class ExamSubmission(models.Model):
    STATUS_CHOICES = (
        ('Missed', 'Missed'),
        ('Submitted', 'Submitted - Pending Evaluation'),
        ('Evaluated', 'Evaluated'),
    )
    exam = models.ForeignKey(ScheduledExam, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='exam_submissions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    total_score = models.FloatField(default=0.0, help_text="Calculated total score")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"

class StudentAnswer(models.Model):
    submission = models.ForeignKey(ExamSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    
    # For MCQ
    selected_option = models.CharField(max_length=255, blank=True, null=True)
    # For Written
    written_text = models.TextField(blank=True, null=True)
    # For Photo
    attachment = models.FileField(upload_to='exam_answers/', blank=True, null=True)
    
    marks_awarded = models.FloatField(default=0.0)
    teacher_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Ans: {self.submission.id} - Q: {self.question.id}"

class MalpracticeLog(models.Model):
    exam = models.ForeignKey(ScheduledExam, on_delete=models.CASCADE, related_name='malpractice_logs')
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='malpractice_logs')
    violation_type = models.CharField(max_length=100) # e.g., 'Cell Phone Detected', 'Multiple People', 'Looking Away', 'No Face Detected'
    timestamp = models.DateTimeField(auto_now_add=True)
    evidence_image = models.ImageField(upload_to='proctoring_evidence/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.violation_type} - {self.student.username} ({self.timestamp})"

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

@receiver(post_save, sender=ExamSubmission)
def update_student_gpa(sender, instance, **kwargs):
    if instance.status == 'Evaluated':
        # Calculate average percentage across all evaluated submissions for this student
        submissions = ExamSubmission.objects.filter(student=instance.student, status='Evaluated')
        
        total_percentage = 0
        count = 0
        for sub in submissions:
            if sub.exam.total_marks > 0:
                total_percentage += (sub.total_score / sub.exam.total_marks) * 100
                count += 1
                
        if count > 0:
            avg_percent = total_percentage / count
            # Convert to 4.0 scale (simplified logic: 100% = 4.0, 90=3.6 etc. (avg/25))
            gpa = avg_percent / 25.0
            gpa = round(min(4.0, max(0.0, gpa)), 2)
            
            if hasattr(instance.student, 'student_profile'):
                instance.student.student_profile.gpa = gpa
                instance.student.student_profile.save(update_fields=['gpa'])

