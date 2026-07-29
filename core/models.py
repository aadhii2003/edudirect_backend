from django.db import models

class Enquiry(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Addressed', 'Addressed'),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    course_id = models.CharField(max_length=100, blank=True, null=True)
    course_name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    source_page = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course_name or 'General Enquiry'}"

class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(default=5)
    quote = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.course_name})"

class HomePageSetting(models.Model):
    """Singleton model to store home page banner and dynamic statistics."""
    hero_label = models.CharField(max_length=100, default="Learn • Grow • Succeed")
    hero_title_main = models.CharField(max_length=200, default="Your Future")
    hero_title_highlight = models.CharField(max_length=200, default="Starts Here")
    hero_description = models.TextField(default="Discover world-class courses, learn from experts, and achieve your academic and career goals.")
    hero_image_url = models.CharField(max_length=500, default="/edu_banner.png", blank=True)
    
    notice_alert = models.CharField(max_length=500, blank=True, null=True, default="Summer term registration deadlines have been extended.")
    active_announcement = models.CharField(max_length=500, blank=True, null=True, default="Dr. Foster appointed as Computer Science research head.")

    stat_students = models.IntegerField(default=50000, help_text="Students Enrolled")
    stat_courses = models.IntegerField(default=1200, help_text="Online Courses")
    stat_partners = models.IntegerField(default=150, help_text="University Partners")
    stat_rating = models.FloatField(default=4.8, help_text="Student Rating")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Home Page Settings"

class AboutUsSetting(models.Model):
    """Singleton model for About Us page content."""
    mission_statement = models.TextField(default="Our mission is to provide accessible, high-quality education to empower learners globally.")
    vision_statement = models.TextField(default="To be the leading platform for professional and academic growth.")
    history_content = models.TextField(default="Founded in 2026, EduConnect has grown to serve thousands of students.")
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "About Us Settings"

class ContactUsSetting(models.Model):
    """Singleton model for Contact Us page content."""
    address = models.TextField(default="123 Education Street, Learning City, 10101")
    phone = models.CharField(max_length=50, default="+1 234 567 8900")
    email = models.EmailField(default="contact@educonnect.com")
    working_hours = models.CharField(max_length=100, default="Mon - Fri: 9:00 AM - 6:00 PM")
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Contact Us Settings"

class Notification(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=500, blank=True, null=True, help_text="Optional URL to navigate when clicked")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
