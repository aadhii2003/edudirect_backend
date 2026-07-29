from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import ScheduledExam, Question, ExamSubmission, StudentAnswer, MalpracticeLog
from .serializers import ScheduledExamSerializer, QuestionSerializer, ExamSubmissionSerializer, StudentAnswerSerializer

class ScheduledExamViewSet(viewsets.ModelViewSet):
    queryset = ScheduledExam.objects.all().order_by('-scheduled_date')
    serializer_class = ScheduledExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from core.models import Notification
        from accounts.models import User
        exam = serializer.save(created_by=self.request.user)
        
        # Notify Teachers if created by admin
        if self.request.user.role == 'admin':
            if exam.batch:
                teachers = User.objects.filter(role='teacher', faculty_profile__batches=exam.batch)
            else:
                teachers = User.objects.filter(role='teacher', faculty_profile__courses=exam.course)
                
            notifications = []
            for t in teachers:
                notifications.append(Notification(
                    user=t,
                    title=f"New Exam Assigned: {exam.title}",
                    message=f"An admin has scheduled a new exam for your batch.",
                    link="/teacher/dashboard/exams"
                ))
            if notifications:
                Notification.objects.bulk_create(notifications)

    @action(detail=True, methods=['post'])
    def submit_exam(self, request, pk=None):
        import json
        exam = self.get_object()
        student = request.user
        
        # Check if already submitted
        if ExamSubmission.objects.filter(exam=exam, student=student).exists():
            return Response({'error': 'You have already submitted this exam.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            answers_data_str = request.data.get('answers', '[]')
            answers_data = json.loads(answers_data_str)
        except json.JSONDecodeError:
            answers_data = []
            
        # Create submission
        submission = ExamSubmission.objects.create(
            exam=exam,
            student=student,
            status='Submitted'
        )
        
        total_mcq_score = 0.0
        
        for ans in answers_data:
            question_id = ans.get('question_id')
            try:
                question = Question.objects.get(id=question_id, exam=exam)
                
                selected_option = ans.get('selected_option', '')
                written_text = ans.get('written_text', '')
                attachment = request.FILES.get(f'attachment_{question_id}')
                
                marks_awarded = 0.0
                
                # Auto grade MCQ
                if question.question_type == 'MCQ':
                    if selected_option and selected_option == question.correct_answer:
                        marks_awarded = float(question.marks)
                        total_mcq_score += marks_awarded
                
                StudentAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_option=selected_option,
                    written_text=written_text,
                    attachment=attachment,
                    marks_awarded=marks_awarded
                )
            except Question.DoesNotExist:
                pass
        
        submission.total_score = total_mcq_score
        submission.save()
        
        return Response({'message': 'Exam submitted successfully.', 'submission_id': submission.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        from core.models import Notification
        from accounts.models import User
        exam = self.get_object()
        
        if exam.status == 'Published':
            return Response({'detail': 'Exam is already published.'}, status=status.HTTP_400_BAD_REQUEST)
            
        unevaluated = ExamSubmission.objects.filter(exam=exam).exclude(status='Evaluated')
        if unevaluated.exists():
            return Response({'detail': 'Cannot publish results until all student submissions have been evaluated by a teacher.'}, status=status.HTTP_400_BAD_REQUEST)
            
        exam.status = 'Published'
        exam.save()
        
        # Notify all students in this batch or course
        if exam.batch:
            students = User.objects.filter(role='student', student_profile__batch=exam.batch)
        else:
            students = User.objects.filter(role='student', student_profile__course=exam.course)
            
        notifications = []
        for st in students:
            notifications.append(Notification(
                user=st,
                title=f"Exam Results Published: {exam.title}",
                message=f"The results for your exam '{exam.title}' have been published. Check your portal to view your score.",
                link="/student-portal/exams"
            ))
        if notifications:
            Notification.objects.bulk_create(notifications)
            
        return Response({'message': 'Exam published successfully and students notified.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def log_malpractice(self, request, pk=None):
        exam = self.get_object()
        student = request.user
        violation_type = request.data.get('violation_type')
        description = request.data.get('description', '')
        evidence_image = request.FILES.get('evidence_image')

        if not violation_type:
            return Response({'error': 'violation_type is required'}, status=status.HTTP_400_BAD_REQUEST)

        MalpracticeLog.objects.create(
            exam=exam,
            student=student,
            violation_type=violation_type,
            description=description,
            evidence_image=evidence_image
        )
        return Response({'message': 'Malpractice logged successfully'}, status=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from django.utils import timezone
        user = self.request.user
        qs = super().get_queryset()
        
        # Filter by exam if provided
        exam_id = self.request.query_params.get('exam')
        if exam_id:
            qs = qs.filter(exam_id=exam_id)
            
        if user.role == 'student':
            # Students can only see questions if the exam is Scheduled or Published 
            # and the current time is past the scheduled_date
            now = timezone.now()
            qs = qs.filter(exam__status__in=['Scheduled', 'Published'], exam__scheduled_date__lte=now)
            
        return qs

class ExamSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ExamSubmission.objects.all().order_by('-submitted_at')
    serializer_class = ExamSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return ExamSubmission.objects.filter(student=user).order_by('-submitted_at')
        return super().get_queryset()
        
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """
        Expects payload:
        {
            "grades": [
                {"answer_id": 1, "marks_awarded": 5.0, "feedback": "Good job"},
                ...
            ]
        }
        """
        submission = self.get_object()
        grades_data = request.data.get('grades', [])
        
        for g in grades_data:
            ans_id = g.get('answer_id')
            marks = float(g.get('marks_awarded', 0))
            feedback = g.get('feedback', '')
            try:
                ans = StudentAnswer.objects.get(id=ans_id, submission=submission)
                ans.marks_awarded = marks
                ans.teacher_feedback = feedback
                ans.save()
            except StudentAnswer.DoesNotExist:
                continue
                
        # Recalculate total score
        total = sum(ans.marks_awarded for ans in submission.answers.all())
        submission.total_score = total
        submission.status = 'Evaluated'
        submission.save()
        
        return Response({'message': 'Grades updated successfully.', 'total_score': total}, status=status.HTTP_200_OK)


class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
