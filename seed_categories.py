import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_backend.settings")
django.setup()

from courses.models import Category

def seed():
    categories = [
        {"name": "Computer Science", "description": "Courses related to computing and software."},
        {"name": "Business", "description": "Business administration and management."},
        {"name": "Marketing", "description": "Digital and traditional marketing strategies."},
        {"name": "IT", "description": "Information Technology and systems."},
    ]

    for cat in categories:
        obj, created = Category.objects.get_or_create(name=cat['name'], defaults={'description': cat['description']})
        if created:
            print(f"Created category: {cat['name']}")
        else:
            print(f"Category already exists: {cat['name']}")

if __name__ == '__main__':
    seed()
