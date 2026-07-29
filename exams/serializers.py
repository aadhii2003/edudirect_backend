from rest_framework import serializers
from .models import ScheduledExam, Question, ExamSubmission, StudentAnswer, MalpracticeLog

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ScheduledExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    batch_name = serializers.CharField(source='batch.name', read_only=True, default='')
    
    class Meta:
        model = ScheduledExam
        fields = '__all__'

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'

class MalpracticeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MalpracticeLog
        fields = '__all__'

class ExamSubmissionSerializer(serializers.ModelSerializer):
    answers = StudentAnswerSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.username', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    malpractice_logs = serializers.SerializerMethodField()

    class Meta:
        model = ExamSubmission
        fields = '__all__'

    def get_malpractice_logs(self, obj):
        logs = MalpracticeLog.objects.filter(exam=obj.exam, student=obj.student).order_by('-timestamp')
        return MalpracticeLogSerializer(logs, many=True).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        # Hide total score from students if exam is not published
        if request and request.user.role == 'student' and instance.exam.status != 'Published':
            ret['total_score'] = None
            ret['answers'] = []  # hide answers too so they don't see marks_awarded
        return ret
