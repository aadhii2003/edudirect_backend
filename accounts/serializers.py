from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import StudentProfile, StaffProfile, FacultyProfile

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['user_id'] = self.user.id
        return data

class StudentProfileSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    batch_name = serializers.CharField(source='batch.name', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ('course', 'course_name', 'batch', 'batch_name', 'grade', 'attendance', 'status', 'enrollmentDate', 'gpa', 'outstandingFees')

class StaffProfileSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = StaffProfile
        fields = ('department', 'department_name')

class FacultyProfileSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = FacultyProfile
        fields = ('department', 'department_name', 'title')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    student_profile = StudentProfileSerializer(required=False)
    staff_profile = StaffProfileSerializer(required=False)
    faculty_profile = FacultyProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'password', 'student_profile', 'staff_profile', 'faculty_profile')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'role': {'required': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('student_profile', None)
        staff_data = validated_data.pop('staff_profile', None)
        faculty_data = validated_data.pop('faculty_profile', None)
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password('edudirect123!')
        
        # Ensure staff and faculty users have is_staff=True so they can pass DRF IsAdminUser checks in views
        if user.role in ['staff', 'faculty', 'admin', 'superadmin']:
            user.is_staff = True
            
        user.save()
        
        if profile_data:
            StudentProfile.objects.create(user=user, **profile_data)
        elif user.role == 'student':
            StudentProfile.objects.create(user=user)
            
        if staff_data:
            StaffProfile.objects.create(user=user, **staff_data)
        elif user.role == 'staff':
            StaffProfile.objects.create(user=user)
            
        if faculty_data:
            FacultyProfile.objects.create(user=user, **faculty_data)
        elif user.role == 'faculty':
            FacultyProfile.objects.create(user=user)
            
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('student_profile', None)
        staff_data = validated_data.pop('staff_profile', None)
        faculty_data = validated_data.pop('faculty_profile', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
        instance.save()
        
        if profile_data and hasattr(instance, 'student_profile'):
            profile = instance.student_profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        if staff_data and hasattr(instance, 'staff_profile'):
            profile = instance.staff_profile
            for attr, value in staff_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        if faculty_data and hasattr(instance, 'faculty_profile'):
            profile = instance.faculty_profile
            for attr, value in faculty_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        return instance