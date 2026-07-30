# lms_backend/urls.py
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    path('api/core/', include('core.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('blog.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/', include('assignments.urls')),
]

# Force media serving even when DEBUG=False (Gunicorn)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
