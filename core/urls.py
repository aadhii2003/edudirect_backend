from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnquiryViewSet, TestimonialViewSet, HomePageSettingRetrieveUpdateView, AboutUsSettingRetrieveUpdateView, ContactUsSettingRetrieveUpdateView, ImageUploadView, NotificationViewSet

router = DefaultRouter()
router.register('enquiries', EnquiryViewSet, basename='enquiry')
router.register('testimonials', TestimonialViewSet, basename='testimonial')
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('home-settings/', HomePageSettingRetrieveUpdateView.as_view(), name='home-settings'),
    path('about-settings/', AboutUsSettingRetrieveUpdateView.as_view(), name='about-settings'),
    path('contact-settings/', ContactUsSettingRetrieveUpdateView.as_view(), name='contact-settings'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]
