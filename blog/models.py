from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    title = models.CharField(max_length=255)
    excerpt = models.TextField()
    content = models.TextField()
    featuredImage = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100)
    authorName = models.CharField(max_length=100)
    authorRole = models.CharField(max_length=100)
    authorAvatar = models.ImageField(upload_to='blog/avatars/', blank=True, null=True)
    isDraft = models.BooleanField(default=False)
    metaTitle = models.CharField(max_length=255, blank=True, null=True)
    metaDescription = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
