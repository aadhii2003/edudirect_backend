import re
from django.db import migrations

def parse_html_to_fields(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    for course in Course.objects.all():
        desc = course.longDescription
        if not desc:
            continue
            
        # Extract Headline
        headline_match = re.search(r'<h3>Headline</h3>\s*<p>(.*?)</p>', desc, re.IGNORECASE | re.DOTALL)
        if headline_match:
            course.headline = headline_match.group(1).strip()
            
        # Extract Overview
        overview_match = re.search(r'<h3>Overview</h3>\s*<p>(.*?)</p>', desc, re.IGNORECASE | re.DOTALL)
        if overview_match:
            course.overview = overview_match.group(1).strip()
            
        # Extract Format
        format_match = re.search(r'<h3>Format</h3>\s*<p>(.*?)</p>', desc, re.IGNORECASE | re.DOTALL)
        if format_match:
            course.format_description = format_match.group(1).strip()
            
        # Extract Outcomes
        outcomes_match = re.search(r'<h3>Outcomes</h3>\s*<p>(.*?)</p>', desc, re.IGNORECASE | re.DOTALL)
        if outcomes_match:
            course.outcomes = outcomes_match.group(1).strip()
            
        # Extract What You Will Learn
        learn_match = re.search(r'<h3>What You Will Learn</h3>\s*<ul[^>]*>(.*?)</ul>', desc, re.IGNORECASE | re.DOTALL)
        if learn_match:
            ul_content = learn_match.group(1)
            li_items = re.findall(r'<li>(.*?)</li>', ul_content, re.IGNORECASE | re.DOTALL)
            course.what_you_will_learn = [item.strip() for item in li_items]
            
        course.save()

def reverse_parse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_course_cta_text_course_format_description_and_more'),
    ]

    operations = [
        migrations.RunPython(parse_html_to_fields, reverse_parse)
    ]
