from rest_framework import serializers
from .models import Department, Course, Category, Subject, ClassSchedule, Batch, AttendanceRecord

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class BatchSerializer(serializers.ModelSerializer):
    main_instructor_name = serializers.CharField(source='main_instructor.username', read_only=True)
    
    class Meta:
        model = Batch
        fields = '__all__'

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = '__all__'

class ClassScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.username', read_only=True)
    subject_title = serializers.CharField(source='subject.title', read_only=True)
    
    class Meta:
        model = ClassSchedule
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    departmentId = serializers.CharField(source='department.id', read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    batches = BatchSerializer(many=True, read_only=True)
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'slug', 'name', 'shortDescription', 'longDescription', 
            'department', 'departmentId', 'mode', 'duration', 'fee', 'startDates', 
            'certification', 'eligibility', 'syllabus', 'examPattern', 'examSchedule',
            'image_url', 'category', 'subjects', 'batches', 'instructor', 'instructor_name'
        ]

    def to_representation(self, instance):
        """Include category details in GET requests."""
        rep = super().to_representation(instance)
        if instance.category:
            rep['category_name'] = instance.category.name
        else:
            rep['category_name'] = None
        return rep
