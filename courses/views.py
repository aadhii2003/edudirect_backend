from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Department, Course, Category, Subject, ClassSchedule, Batch, AttendanceRecord
from .serializers import DepartmentSerializer, CourseSerializer, CategorySerializer, SubjectSerializer, ClassScheduleSerializer, BatchSerializer, AttendanceRecordSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def end_class(self, request, pk=None):
        schedule = self.get_object()
        user = request.user
        
        if user.role not in ['admin', 'superadmin', 'staff', 'faculty'] and user != schedule.staff:
            return Response({'error': 'You do not have permission to end this class.'}, status=status.HTTP_403_FORBIDDEN)
            
        schedule.status = 'Completed'
        schedule.save()
        
        # Notify students
        from core.models import Notification
        from accounts.models import User
        if schedule.batch:
            students = User.objects.filter(role='student', student_profile__batch=schedule.batch)
            notifications = []
            for st in students:
                notifications.append(Notification(
                    user=st,
                    title=f"Class Ended: {schedule.subject.title}",
                    message=f"The class {schedule.subject.title} has ended.",
                    link="/student-portal/dashboard"
                ))
            if notifications:
                Notification.objects.bulk_create(notifications)
                
        return Response({'message': 'Class marked as completed successfully.'}, status=status.HTTP_200_OK)

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = AttendanceRecord.objects.all()
        schedule = self.request.query_params.get('schedule', None)
        if schedule:
            queryset = queryset.filter(schedule_id=schedule)
        return queryset

