import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
django.setup()

from accounts.models import User

# Create superadmin
if not User.objects.filter(username='supercrudops').exists():
    User.objects.create_superuser(
        username='supercrudops',
        password='superadmin123',
        role='superadmin'
    )
    print("Created superadmin: supercrudops")
else:
    print("Superadmin supercrudops already exists")

# Create admin
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_user(
        username='admin',
        password='admin123',
        role='admin'
    )
    user.is_staff = True
    user.save()
    print("Created admin: admin")
else:
    print("Admin admin already exists")
