from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Enquiry, Testimonial, HomePageSetting, AboutUsSetting, ContactUsSetting, Notification
from .serializers import EnquirySerializer, TestimonialSerializer, HomePageSettingSerializer, AboutUsSettingSerializer, ContactUsSettingSerializer, NotificationSerializer

class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class BaseSettingView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

class HomePageSettingRetrieveUpdateView(BaseSettingView):
    def get(self, request, *args, **kwargs):
        stat = HomePageSetting.load()
        serializer = HomePageSettingSerializer(stat)
        return Response(serializer.data)
        
    def patch(self, request, *args, **kwargs):
        stat = HomePageSetting.load()
        serializer = HomePageSettingSerializer(stat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

class AboutUsSettingRetrieveUpdateView(BaseSettingView):
    def get(self, request, *args, **kwargs):
        stat = AboutUsSetting.load()
        serializer = AboutUsSettingSerializer(stat)
        return Response(serializer.data)
        
    def patch(self, request, *args, **kwargs):
        stat = AboutUsSetting.load()
        serializer = AboutUsSettingSerializer(stat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

class ContactUsSettingRetrieveUpdateView(BaseSettingView):
    def get(self, request, *args, **kwargs):
        stat = ContactUsSetting.load()
        serializer = ContactUsSettingSerializer(stat)
        return Response(serializer.data)
        
    def patch(self, request, *args, **kwargs):
        stat = ContactUsSetting.load()
        serializer = ContactUsSettingSerializer(stat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)


from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class ImageUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=400)
        
        # Save file to media/uploads/
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_name = default_storage.get_valid_name(file_obj.name)
        # Handle file name duplicates by finding a unique name
        base_name, ext = os.path.splitext(file_name)
        counter = 1
        while default_storage.exists(os.path.join('uploads', file_name)):
            file_name = f"{base_name}_{counter}{ext}"
            counter += 1

        path = default_storage.save(os.path.join('uploads', file_name), ContentFile(file_obj.read()))
        # Get media URL
        media_url = f"{settings.MEDIA_URL}{path}"
        # Normalize slashes just in case on Windows
        media_url = media_url.replace('\\', '/')
        
        return Response({'url': media_url}, status=200)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
