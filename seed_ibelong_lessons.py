import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
django.setup()

from courses.models import Course, Subject

def seed_lessons():
    # Get the 3 most recently created courses
    courses = Course.objects.all().order_by('-id')[:3]
    if not courses:
        print("No courses found.")
        return

    print(f"Adding lessons to {len(courses)} courses...")

    lessons_data = [
        {"week": 1, "title": "Introduction & Course + Assessment Overview (Focus Mainly on Task 1 - Storing Lesson Material)"},
        {"week": 1, "title": "Identifying and Making use of My Talents & Abilities in the Maltese Society"},
        {"week": 2, "title": "Personality Strengths & Weaknesses. Mediterranean Traits?"},
        {"week": 2, "title": "Temper & Behaviour. Awareness about Lifestyles and Different Backgrounds"},
        {"week": 3, "title": "Methods of Self Assessment in relation to Integration"},
        {"week": 3, "title": "Action Plan towards Self Improvement in a Local Context. My Place in the Community"},
        {"week": 4, "title": "Task 2 Tutorial - Public Speaking & Preparation for PowerPoint Presentation"},
        {"week": 4, "title": "CVs & Job Hunting"},
        {"week": 5, "title": "What is meant by Code of Conduct & Integrity?"},
        {"week": 5, "title": "Jobsplus Mission + Interpersonal skills + Communication skills"},
        {"week": 6, "title": "Learning Reflections + How to solve a conflict + Leadership Skills"},
        {"week": 6, "title": "Task 2 - (Presentations) Talents and Capabilities towards a Career/Profession."},
        {"week": 7, "title": "Exploring & Sharing own Background"},
        {"week": 7, "title": "Diversity - Race"},
        {"week": 8, "title": "Diversity - Sexuality & Gender Identities"},
        {"week": 8, "title": "Diversity - Different Abilities"},
        {"week": 9, "title": "Diversity - Creed"},
        {"week": 10, "title": "Equality & Equity - Similarities and Differences"},
        {"week": 10, "title": "Human Rights- Discussion"},
        {"week": 11, "title": "Rights & Duties"},
        {"week": 11, "title": "Freedom of Expression & its Responsibilities"},
        {"week": 12, "title": "NCPE + Human Rights in Malta"},
        {"week": 12, "title": "HR, Integration and Inclusion"},
        {"week": 13, "title": "Society & Civilisation"},
        {"week": 13, "title": "Recalling Maltese Historical Events (a selection)"},
        {"week": 14, "title": "Cultural Traditions and their Origins"},
        {"week": 14, "title": "Task 3 Tutorial (Explain last assessment)"},
        {"week": 15, "title": "Visit to Historical Museums (Selection) (Real or Virtual)"},
        {"week": 15, "title": "Visit Evaluation & Learning Reflections"},
        {"week": 16, "title": "Sharing of History & Traditions - Part 1"},
        {"week": 16, "title": "Sharing of History & Traditions - Part 2"},
        {"week": 17, "title": "Sharing of History & Traditions- Part 3"},
        {"week": 18, "title": "Task 3 (Presentations) Maltese history and Culture"},
        {"week": 19, "title": "Closure & Feedback Collection"}
    ]

    for course in courses:
        print(f"Seeding course: {course.name}")
        # Clear existing subjects to avoid duplicates if run multiple times
        Subject.objects.filter(course=course).delete()
        
        for index, lesson in enumerate(lessons_data):
            # Calculate module based on weeks
            if lesson['week'] <= 7:
                module = "Module 1: Personal Growth & Employability"
            elif lesson['week'] <= 12:
                module = "Module 2: Diversity, Equality & Rights"
            else:
                module = "Module 3: Maltese History & Culture"
                
            Subject.objects.create(
                course=course,
                module_name=module,
                title=f"Lecture {index + 1}: {lesson['title']}",
                description=f"Week {lesson['week']} Content"
            )
    print("Seeding complete.")

if __name__ == '__main__':
    seed_lessons()
