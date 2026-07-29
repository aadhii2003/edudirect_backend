from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduledExamViewSet, QuestionViewSet, ExamSubmissionViewSet, StudentAnswerViewSet

router = DefaultRouter()
router.register('scheduled-exams', ScheduledExamViewSet, basename='scheduled-exam')
router.register('questions', QuestionViewSet, basename='question')
router.register('submissions', ExamSubmissionViewSet, basename='submission')
router.register('answers', StudentAnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
]
