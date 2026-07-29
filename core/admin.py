from django.contrib import admin
from .models import Enquiry, Testimonial, HomePageSetting

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course_name', 'created_at')
    search_fields = ('name', 'email', 'course_name')
    list_filter = ('created_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_name', 'rating')
    search_fields = ('name', 'course_name')

@admin.register(HomePageSetting)
class HomePageSettingAdmin(admin.ModelAdmin):
    list_display = ('hero_title_main', 'stat_students', 'stat_courses')
