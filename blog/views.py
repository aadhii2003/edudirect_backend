from rest_framework import permissions, viewsets
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by("-date")
    serializer_class = BlogPostSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context