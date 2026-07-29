import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
django.setup()

from courses.models import Course

def update_courses():
    courses = Course.objects.all().order_by('-id')[:3]
    for idx, c in enumerate(courses):
        c.name = f'I Belong Programme Stage 2 Cultural Orientation - Cohort {3-idx}'
        c.shortDescription = 'Examine abilities, understand fair society, human rights, and Malta history.'
        c.longDescription = 'Learning Outcomes:\nL.O.1 – Examine your own abilities and how they can contribute to personal growth and development.\nL.O.2 – Understand the importance of achieving a fair and equitable society and its impact on individuals and communities.\nL.O.3 – Explain the significance of human rights and their effects on peoples lives.\nL.O.4 – Understand how Maltas history and culture have shaped its society.'
        c.save()
        print(f'Updated: {c.name}')

if __name__ == '__main__':
    update_courses()
