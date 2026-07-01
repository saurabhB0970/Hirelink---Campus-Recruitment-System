import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hirelink.settings')
django.setup()

from django.contrib.auth import get_user_model
from portal.models import (
    StudentProfile, RecruiterProfile, InstituteProfile,
    Job, JobApplication, Interview, Alumni, PlacementDrive,
    StudentSkill, StudentProject, StudentInternship
)

User = get_user_model()

def populate():
    print("Populating database...")

    # 1. Create Superuser
    if not User.objects.filter(username='admin@hirelink.com').exists():
        admin_user = User.objects.create_superuser(
            username='admin@hirelink.com',
            email='admin@hirelink.com',
            password='password123',
            full_name='System Admin',
            phone_number='1234567890',
            user_type='institute'
        )
        print("Superuser created (admin@hirelink.com / password123)")

    # 2. Create Student User & Profile
    student_user, created = User.objects.get_or_create(
        username='student@hirelink.com',
        defaults={
            'email': 'student@hirelink.com',
            'full_name': 'Tanmay Dahivalikar',
            'phone_number': '+91 99887 76655',
            'user_type': 'student'
        }
    )
    if created:
        student_user.set_password('password123')
        student_user.save()
        
    student_profile, created = StudentProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'roll_number': 'Roll-101',
            'college': 'K J College of Engineering and Management Research, Pune',
            'major': 'Computer Engineering',
            'cgpa': 8.92,
            'ssc_percentage': 85.5,
            'hsc_percentage': 88.0,
            'backlogs': 0,
            'location': 'Pune, India'
        }
    )
    
    # Add skills, projects, internships to Tanmay
    StudentSkill.objects.get_or_create(student_profile=student_profile, name="Django")
    StudentSkill.objects.get_or_create(student_profile=student_profile, name="Python")
    StudentSkill.objects.get_or_create(student_profile=student_profile, name="Flutter")
    StudentSkill.objects.get_or_create(student_profile=student_profile, name="JavaScript")
    
    StudentProject.objects.get_or_create(
        student_profile=student_profile,
        title="HireLink TPO Portal",
        defaults={
            'description': "A smart and dynamic placement cell automation web application.",
            'link': "https://github.com/hirelink/hirelink"
        }
    )
    
    StudentInternship.objects.get_or_create(
        student_profile=student_profile,
        company="Google",
        defaults={
            'role': "STEP Intern",
            'duration': "3 Months",
            'description': "Worked on core Search infrastrucutre tools using C++."
        }
    )
    
    print("Student user & profile created (student@hirelink.com / password123)")

    # 3. Create Recruiter User & Profile
    recruiter_user, created = User.objects.get_or_create(
        username='recruiter@hirelink.com',
        defaults={
            'email': 'recruiter@hirelink.com',
            'full_name': 'Priya Sharma',
            'phone_number': '+91 98765 43210',
            'user_type': 'recruiter'
        }
    )
    if created:
        recruiter_user.set_password('password123')
        recruiter_user.save()

    recruiter_profile, created = RecruiterProfile.objects.get_or_create(
        user=recruiter_user,
        defaults={
            'company_name': 'SAP Labs',
            'position': 'HR Manager',
            'company_email': 'priya@sap.com',
            'description': 'SAP Labs is a global leader in enterprise software solutions.'
        }
    )
    print("Recruiter user & profile created (recruiter@hirelink.com / password123)")

    # 4. Create Institute User & Profile
    institute_user, created = User.objects.get_or_create(
        username='institute@hirelink.com',
        defaults={
            'email': 'institute@hirelink.com',
            'full_name': 'Dr. Aryan Khanna',
            'phone_number': '+91 90000 11111',
            'user_type': 'institute'
        }
    )
    if created:
        institute_user.set_password('password123')
        institute_user.save()

    institute_profile, created = InstituteProfile.objects.get_or_create(
        user=institute_user,
        defaults={
            'institute_name': 'K J College of Engineering and Management Research, Pune',
            'designation': 'Training & Placement Officer',
            'department': 'Computer Engineering'
        }
    )
    print("Institute user & profile created (institute@hirelink.com / password123)")

    # 5. Create Jobs
    job1, created = Job.objects.get_or_create(
        recruiter=recruiter_profile,
        title='Technical Business Analyst / Android / Flutter Developer',
        defaults={
            'location': 'Noida',
            'job_type': 'Full Time',
            'ctc': '₹ 6,10,000 - ₹ 10,00,000 per Annum',
            'category': 'Engineering - Web / Software',
            'description': 'Join Chetu Inc., a world-class software services provider. We are looking for talented developers to work on cutting-edge technologies.',
            'skills_required': 'Flutter, Android, Dart, Java',
            'workflow': ["Aptitude Round", "Technical MCQ Test", "Coding Interview", "Technical Interview 1", "HR Interview"],
            'criteria': ["No active backlogs", "Minimum 60% in 10th & 12th", "B.Tech preferred", "Knowledge of Flutter/Dart"],
            'min_cgpa': 6.0,
            'min_ssc_marks': 60.0,
            'min_hsc_marks': 60.0,
            'max_backlogs': 2
        }
    )

    job2, created = Job.objects.get_or_create(
        recruiter=recruiter_profile,
        title='MERN Stack Developer Intern',
        defaults={
            'location': 'Pune',
            'job_type': 'Internship',
            'ctc': '₹ 15,000 - ₹ 20,00,00 per Month',
            'category': 'Web Development',
            'description': 'Exciting opportunity to work on live projects using React, Node.js, and MongoDB.',
            'skills_required': 'React, Node.js, Express, MongoDB',
            'workflow': ["Task-based Assessment", "Technical Interview", "Final Selection"],
            'criteria': ["Available for 6 months", "Strong JavaScript knowledge", "Pune local preferred"],
            'min_cgpa': 6.5,
            'min_ssc_marks': 65.0,
            'min_hsc_marks': 65.0,
            'max_backlogs': 0
        }
    )
    print("Sample Jobs created")

    # 6. Job Applications
    JobApplication.objects.get_or_create(
        job=job2,
        student=student_profile,
        defaults={'status': 'Under Review', 'score': 78}
    )
    print("Sample Job Applications created")

    # 7. Create Alumni Data
    alumni_list = [
        {"name": "Saurabh Bhosale", "year": "2023", "company": "Microsoft", "phone": "+91 98765 43210"},
        {"name": "Tanmay Dahivalikar", "year": "2022", "company": "Google", "phone": "+91 99887 76655"},
        {"name": "Bhageshree Giri", "year": "2024", "company": "TCS", "phone": "+91 91234 56789"},
        {"name": "Omkar Ingale", "year": "2021", "company": "Amazon", "phone": "+91 90000 11111"},
        {"name": "Vikram Singh", "year": "2023", "company": "SAP Labs", "phone": "+91 88888 99999"}
    ]
    for a in alumni_list:
        Alumni.objects.get_or_create(
            name=a['name'],
            defaults={
                'year': a['year'],
                'company': a['company'],
                'phone': a['phone']
            }
        )
    print("Alumni data populated")

    # 8. Create Interview Schedules
    import datetime
    Interview.objects.get_or_create(
        recruiter=recruiter_profile,
        student=student_profile,
        company_name='SAP Labs',
        round_name='Technical',
        defaults={
            'meeting_details': 'Block 3 - Room 102',
            'date': datetime.date(2026, 2, 28),
            'time': datetime.time(11, 0),
            'prep_checklist': ["Revise SAP BTP basics", "Practice SQL Queries", "Understand OData services"],
            'status': 'Confirmed',
        }
    )
    Interview.objects.get_or_create(
        recruiter=recruiter_profile,
        student=student_profile,
        company_name='Google',
        round_name='Shortlist',
        defaults={
            'meeting_details': 'https://meet.google.com/abc-defg-hij',
            'date': datetime.date(2026, 2, 15),
            'time': datetime.time(15, 30),
            'prep_checklist': ["Graph Algorithms", "System Design Basics", "Dynamic Programming"],
            'status': 'Confirmed',
        }
    )
    print("Interview schedules populated")

    # 9. Create Placement Drives
    PlacementDrive.objects.get_or_create(
        company_name='Zscaler',
        defaults={
            'title': 'Zscaler Tech Drive',
            'date': 'Feb 28, 2026',
            'eligibility': 'B.Tech (All) / 7.0 CGPA+',
            'max_applications': 500,
            'applied_count': 420,
            'status': 'Active'
        }
    )
    PlacementDrive.objects.get_or_create(
        company_name='Microsoft',
        defaults={
            'title': 'Microsoft India',
            'date': 'March 12, 2026',
            'eligibility': 'CSE & IT / 8.5 CGPA+',
            'max_applications': 200,
            'applied_count': 150,
            'status': 'Active'
        }
    )
    print("Placement drives populated")
    print("Database population complete!")

if __name__ == '__main__':
    populate()
