# lms_backend/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
# from academics.views import DepartmentViewSet, CourseViewSet

# router = DefaultRouter()
# router.register('departments', DepartmentViewSet)
# router.register('courses', CourseViewSet)


urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    path('api/core/', include('core.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('blog.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/', include('assignments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)