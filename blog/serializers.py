from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    featuredImage = serializers.SerializerMethodField()
    authorAvatar = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = "__all__"

    def _build_url(self, file):
        if not file:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(file.url)

        return file.url

    def get_featuredImage(self, obj):
        return self._build_url(obj.featuredImage)

    def get_authorAvatar(self, obj):
        return self._build_url(obj.authorAvatar)