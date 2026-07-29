from rest_framework import serializers
from .models import Enquiry, Testimonial, HomePageSetting, AboutUsSetting, ContactUsSetting, Notification

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class HomePageSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSetting
        fields = '__all__'

class AboutUsSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsSetting
        fields = '__all__'

class ContactUsSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsSetting
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
