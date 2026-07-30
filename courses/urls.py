from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, CourseViewSet, CategoryViewSet, SubjectViewSet, ClassScheduleViewSet, BatchViewSet, AttendanceRecordViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='department')
router.register('courses', CourseViewSet, basename='course')
router.register('categories', CategoryViewSet, basename='category')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('schedules', ClassScheduleViewSet, basename='schedule')
router.register('batches', BatchViewSet, basename='batch')
router.register('attendance', AttendanceRecordViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]
