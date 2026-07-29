from django.db import models

class Assignment(models.Model):
    batch = models.ForeignKey('courses.Batch', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    question = models.TextField()
    due_date = models.DateField()
    due_time = models.TimeField()
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_assignments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.batch.name}"

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
        ('Rewrite', 'Rewrite'),
    )
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='assignment_submissions')
    written_text = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='assignments/submissions/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    teacher_feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"Submission by {self.student.get_full_name() or self.student.username} for {self.assignment.title}"
