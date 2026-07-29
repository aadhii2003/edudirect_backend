from rest_framework import serializers
from .models import Assignment, AssignmentSubmission
from courses.models import Batch
from accounts.models import User

class AssignmentSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source='batch.name', read_only=True)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'batch', 'batch_name', 'title', 'question', 'due_date', 'due_time', 'created_by', 'created_by_name', 'created_at']
        read_only_fields = ['created_by']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return "Unknown"

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'assignment_title', 'student', 'student_name', 'written_text', 'attachment', 'status', 'teacher_feedback', 'submitted_at', 'updated_at']
        read_only_fields = ['student', 'status', 'teacher_feedback']

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
