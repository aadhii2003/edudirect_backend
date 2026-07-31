from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    featuredImage = serializers.SerializerMethodField()
    authorAvatar = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    def get_featuredImage(self, obj):
        if obj.featuredImage:
            return obj.featuredImage.url
        return None

    def get_authorAvatar(self, obj):
        if obj.authorAvatar:
            return obj.authorAvatar.url
        return None