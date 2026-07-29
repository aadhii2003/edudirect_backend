import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_backend.settings')
django.setup()

from core.models import AboutUsSetting, ContactUsSetting, HomePageSetting
from blog.models import BlogPost

def seed_public_content():
    print("Seeding Home Page Settings...")
    home, _ = HomePageSetting.objects.get_or_create(pk=1)
    home.hero_label = "Learn • Grow • Succeed"
    home.hero_title_main = "Your Future"
    home.hero_title_highlight = "Starts Here"
    home.hero_description = "Discover world-class courses, learn from experts, and achieve your academic and career goals at EduDirect."
    home.save()

    print("Seeding About Us Settings...")
    about, _ = AboutUsSetting.objects.get_or_create(pk=1)
    about.mission_statement = "Our mission is to provide accessible, high-quality education to empower learners globally. We strive to break down barriers and make premium education available to everyone."
    about.vision_statement = "To be the leading global platform for professional and academic growth, setting the gold standard for online and offline learning."
    about.history_content = "Founded in 2026, EduDirect started as a small initiative to bring high-quality technical education to the masses. Today, we have grown to serve thousands of students across multiple disciplines, partnering with top universities worldwide."
    about.save()

    print("Seeding Contact Us Settings...")
    contact, _ = ContactUsSetting.objects.get_or_create(pk=1)
    contact.address = "123 Education Street, Learning City, 10101"
    contact.phone = "1234567890"  # For WhatsApp WA.me
    contact.email = "contact@edudirect.com"
    contact.working_hours = "Mon - Fri: 9:00 AM - 6:00 PM"
    contact.save()

    print("Seeding Blog Posts...")
    # Clear existing posts
    BlogPost.objects.all().delete()
    
    posts = [
        {
            "title": "The Future of AI in Education",
            "excerpt": "How artificial intelligence is reshaping the way we learn and teach.",
            "content": "<h2>The Rise of AI Tutors</h2><p>Artificial intelligence is no longer a futuristic concept; it is actively reshaping our classrooms today. From personalized learning paths to automated grading, AI is freeing up educators to focus on what matters most: human connection.</p><p><strong>Key benefits include:</strong></p><ul><li>24/7 Availability</li><li>Personalized feedback</li><li>Adaptive pacing</li></ul>",
            "category": "Technology",
            "authorName": "Dr. Alan Turing",
            "authorRole": "AI Researcher",
            "isDraft": False
        },
        {
            "title": "Top 10 Web Development Frameworks in 2026",
            "excerpt": "A comprehensive guide to the best tools for building modern web applications.",
            "content": "<h2>Choosing the Right Framework</h2><p>With so many options available, picking a web framework can be daunting. We have analyzed the top contenders for 2026.</p><ol><li><strong>Next.js:</strong> Unmatched for React-based full-stack apps.</li><li><strong>Django:</strong> The 'batteries-included' choice for Python developers.</li><li><strong>SvelteKit:</strong> For those who love zero-overhead reactive programming.</li></ol>",
            "category": "Programming",
            "authorName": "Ada Lovelace",
            "authorRole": "Senior Developer",
            "isDraft": False
        },
        {
            "title": "Mastering Time Management for Online Students",
            "excerpt": "Proven strategies to balance your studies with work and personal life.",
            "content": "<h2>The Myth of Multitasking</h2><p>Many online students struggle because they try to do everything at once. True productivity comes from focus.</p><blockquote><p>\"Do one thing, and do it well.\"</p></blockquote><p>Try using the <strong>Pomodoro Technique</strong>: 25 minutes of intense focus followed by a 5-minute break.</p>",
            "category": "Student Life",
            "authorName": "Marcus Aurelius",
            "authorRole": "Student Counselor",
            "isDraft": False
        }
    ]

    for data in posts:
        BlogPost.objects.create(**data)

    print("Seeding complete!")

if __name__ == '__main__':
    seed_public_content()
