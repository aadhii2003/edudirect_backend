from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'faculty':
            return Assignment.objects.filter(created_by=user).order_by('-created_at')
        elif user.role == 'student':
            # Students see assignments assigned to their batches
            return Assignment.objects.filter(batch__students=user).order_by('-due_date')
        return Assignment.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return AssignmentSubmission.objects.filter(student=user)
        elif user.role == 'faculty':
            # Teachers see submissions for assignments they created
            return AssignmentSubmission.objects.filter(assignment__created_by=user)
        return AssignmentSubmission.objects.all()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['patch'])
    def grade(self, request, pk=None):
        submission = self.get_object()
        if request.user.role != 'faculty' and not request.user.is_superuser:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
            
        status_val = request.data.get('status')
        feedback = request.data.get('teacher_feedback', '')

        if status_val not in ['Complete', 'Rewrite']:
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        submission.status = status_val
        submission.teacher_feedback = feedback
        submission.save()

        serializer = self.get_serializer(submission)
        return Response(serializer.data)
