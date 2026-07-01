import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone
from .models import (
    CustomUser, StudentProfile, StudentInternship, StudentSkill,
    StudentProject, StudentCertification, StudentActivity, StudentResume,
    RecruiterProfile, InstituteProfile, Job, JobApplication, Interview,
    Alumni, PlacementDrive
)

STATUS_DISPLAY_MAP = {
    'Under Review': 'Under Review',
    'shortlisted': 'Shortlisted',
    'technical_cleared': 'Interviewed',
    'hr_cleared': 'Interviewed',
    'hired': 'Hired',
    'rejected': 'Rejected',
}

def serialize_job(job, student_profile=None):
    applied = False
    if student_profile:
        applied = JobApplication.objects.filter(job=job, student=student_profile).exists()
    company = job.company_name or (job.recruiter.company_name if job.recruiter else "N/A")
    return {
        'id': job.id,
        'title': job.title,
        'company': company,
        'location': job.location,
        'type': job.job_type,
        'posted': 'Just now' if (timezone.now() - job.created_at).days == 0 else f"{(timezone.now() - job.created_at).days} days ago",
        'ctc': job.ctc,
        'category': job.category,
        'description': job.description,
        'workflow': job.workflow,
        'criteria': job.criteria,
        'applied': applied,
        'min_cgpa': job.min_cgpa,
        'min_tenth_marks': job.min_ssc_marks,
        'min_twelfth_marks': job.min_hsc_marks,
        'max_backlogs': job.max_backlogs,
        'required_skills': job.skills_required,
        'deadline': job.deadline.strftime('%Y-%m-%d') if job.deadline else ""
    }

def serialize_alumni(alumni):
    initials = "".join([part[0].upper() for part in alumni.name.split() if part])[:2] if alumni.name else "AL"
    return {
        'id': alumni.id,
        'name': alumni.name,
        'year': alumni.batch or alumni.year or "",
        'company': alumni.company,
        'role': alumni.role,
        'linkedin': alumni.linkedin or "",
        'image': alumni.image.url if alumni.image else None,
        'testimonial': alumni.testimonial or "",
        'initials': initials
    }

def serialize_interview(interview):
    # Query the JobApplication matching the student and job
    app = None
    if interview.job and interview.student:
        app = JobApplication.objects.filter(student=interview.student, job=interview.job).first()
    if not app and interview.student and interview.recruiter:
        app = JobApplication.objects.filter(student=interview.student, job__recruiter=interview.recruiter).first()
        
    status_mapping = {
        'Under Review': 1,
        'shortlisted': 2,
        'technical_cleared': 3,
        'hr_cleared': 4,
        'hired': 5,
        'rejected': 1,
    }
    
    current_status = app.status if app else 'Under Review'
    curr_round = status_mapping.get(current_status, 1)

    prep_list = interview.preparation_checklist if interview.preparation_checklist else interview.prep_checklist
    if not prep_list:
        prep_list = ["Revise basics", "Prepare resume walkthrough"]
    
    job_role = interview.job.title if interview.job else "Software Engineer"
    
    return {
        'id': interview.id,
        'company': interview.company_name or (interview.recruiter.company_name if interview.recruiter else "N/A"),
        'role': job_role,
        'round_name': interview.round_name,
        'date': interview.date.strftime('%B %d, %Y') if interview.date else "",
        'time': interview.time.strftime('%I:%M %p') if interview.time else "",
        'interviewer': interview.recruiter.user.full_name if (interview.recruiter and interview.recruiter.user.full_name) else "Recruiter",
        'status': interview.status,
        'meeting_details': interview.meeting_details or "",
        'currentRound': curr_round,
        'rounds': ["Shortlist", "Technical Interview", "HR Interview", "Final Selection"],
        'prep': prep_list
    }

def index(request):
    # Student index.html is the landing page
    return render(request, 'Student/index.html')

def institute(request):
    return render(request, 'Student/institute.html')

def recruiter_landing(request):
    return render(request, 'Student/recruiter.html')

def admin_landing(request):
    return render(request, 'Student/admin.html')

def student_landing(request):
    return render(request, 'Student/student.html')

def role_selector(request):
    return render(request, 'Student/role.html')

def register_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type', 'student')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'Registration.html')

        try:
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                full_name=fullname,
                phone_number=phone,
                user_type=user_type
            )
            # Create profiles based on user type
            if user_type == 'student':
                StudentProfile.objects.create(
                    user=user,
                    roll_number=request.POST.get('roll_number', ''),
                    college=request.POST.get('college', ''),
                    major=request.POST.get('major', '')
                )
            elif user_type == 'recruiter':
                RecruiterProfile.objects.create(
                    user=user,
                    company_name=request.POST.get('company', ''),
                    position=request.POST.get('position', ''),
                    company_email=request.POST.get('company_email', '')
                )
            elif user_type == 'institute':
                InstituteProfile.objects.create(
                    user=user,
                    institute_name=request.POST.get('institute_name', ''),
                    designation=request.POST.get('designation', ''),
                    department=request.POST.get('dept', '')
                )
            
            login(request, user)
            # Redirect based on type
            if user_type == 'student':
                return redirect('student_profile')
            elif user_type == 'recruiter':
                return redirect('recruiter_dashboard')
            else:
                return redirect('admin_portal')

        except IntegrityError:
            messages.error(request, "An account with this email already exists.")
            return render(request, 'Registration.html')
    
    return render(request, 'Registration.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'student':
                return redirect('student_profile')
            elif user.user_type == 'recruiter':
                return redirect('recruiter_dashboard')
            elif user.user_type == 'institute':
                return redirect('admin_portal')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Student Views
@login_required
def student_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    context = {
        'profile': profile,
        'internships': profile.internships.all(),
        'skills': profile.skills.all(),
        'projects': profile.projects.all(),
        'certifications': profile.certifications.all(),
        'activities': profile.activities.all(),
        'resumes': profile.resumes.all(),
    }
    return render(request, 'Student/profile.html', context)

@login_required
def update_profile_photo(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES.get('profile_pic')
            profile.save()
            messages.success(request, "Profile photo updated successfully!")
    return redirect('student_profile')

@login_required
def update_profile_basic(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        user = request.user
        user.full_name = request.POST.get('full_name', user.full_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()
        
        profile.location = request.POST.get('location', profile.location)
        profile.save()
        messages.success(request, "Basic information updated successfully!")
    return redirect('student_profile')

@login_required
def update_profile_education(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        profile.college = request.POST.get('college', profile.college)
        profile.major = request.POST.get('major', profile.major)
        profile.roll_number = request.POST.get('roll_number', profile.roll_number)
        
        try:
            profile.cgpa = float(request.POST.get('cgpa', 0.0) or 0.0)
            profile.ssc_percentage = float(request.POST.get('ssc_percentage', 0.0) or 0.0)
            profile.hsc_percentage = float(request.POST.get('hsc_percentage', 0.0) or 0.0)
            profile.backlogs = int(request.POST.get('backlogs', 0) or 0)
        except ValueError:
            messages.error(request, "Invalid input format for marks/backlogs.")
            return redirect('student_profile')
            
        profile.save()
        messages.success(request, "Education details updated successfully!")
    return redirect('student_profile')

@login_required
def add_profile_internship(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        company = request.POST.get('company')
        role = request.POST.get('role')
        duration = request.POST.get('duration')
        description = request.POST.get('description', '')
        
        if company and role and duration:
            StudentInternship.objects.create(
                student_profile=profile,
                company=company,
                role=role,
                duration=duration,
                description=description
            )
            messages.success(request, "Internship added successfully!")
        else:
            messages.error(request, "All fields are required to add an internship.")
    return redirect('student_profile')

@login_required
def delete_profile_internship(request, pk):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        item = get_object_or_404(StudentInternship, id=pk, student_profile=profile)
        item.delete()
        messages.success(request, "Internship removed.")
    return redirect('student_profile')

@login_required
def add_profile_skill(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        name = request.POST.get('skill_name')
        if name:
            StudentSkill.objects.create(student_profile=profile, name=name)
            messages.success(request, "Skill added.")
        else:
            messages.error(request, "Skill name cannot be empty.")
    return redirect('student_profile')

@login_required
def delete_profile_skill(request, pk):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        item = get_object_or_404(StudentSkill, id=pk, student_profile=profile)
        item.delete()
        messages.success(request, "Skill removed.")
    return redirect('student_profile')

@login_required
def add_profile_project(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        link = request.POST.get('link', '')
        if title:
            StudentProject.objects.create(
                student_profile=profile,
                title=title,
                description=description,
                link=link if link else None
            )
            messages.success(request, "Project added.")
        else:
            messages.error(request, "Project title is required.")
    return redirect('student_profile')

@login_required
def delete_profile_project(request, pk):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        item = get_object_or_404(StudentProject, id=pk, student_profile=profile)
        item.delete()
        messages.success(request, "Project removed.")
    return redirect('student_profile')

@login_required
def add_profile_certification(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        name = request.POST.get('name')
        authority = request.POST.get('authority')
        if name and authority:
            StudentCertification.objects.create(
                student_profile=profile,
                name=name,
                authority=authority
            )
            messages.success(request, "Certification added.")
        else:
            messages.error(request, "Both name and issuing authority are required.")
    return redirect('student_profile')

@login_required
def delete_profile_certification(request, pk):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        item = get_object_or_404(StudentCertification, id=pk, student_profile=profile)
        item.delete()
        messages.success(request, "Certification removed.")
    return redirect('student_profile')

@login_required
def add_profile_activity(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        description = request.POST.get('description')
        if description:
            StudentActivity.objects.create(student_profile=profile, description=description)
            messages.success(request, "Activity added.")
        else:
            messages.error(request, "Description is required.")
    return redirect('student_profile')

@login_required
def delete_profile_activity(request, pk):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        item = get_object_or_404(StudentActivity, id=pk, student_profile=profile)
        item.delete()
        messages.success(request, "Activity removed.")
    return redirect('student_profile')

@login_required
def upload_profile_resume(request):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        file = request.FILES.get('resume_file')
        if file:
            StudentResume.objects.create(student_profile=profile, file=file)
            messages.success(request, "Resume uploaded successfully.")
        else:
            messages.error(request, "No file uploaded.")
    return redirect('student_profile')

@login_required
def delete_profile_resume(request, pk):
    if request.method == 'POST':
        profile = get_object_or_404(StudentProfile, user=request.user)
        item = get_object_or_404(StudentResume, id=pk, student_profile=profile)
        item.delete()
        messages.success(request, "Resume removed.")
    return redirect('student_profile')

@login_required
def student_jobs(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    all_jobs = Job.objects.filter(is_active=True).distinct()
    serialized = [serialize_job(job, profile) for job in all_jobs]
    
    student_skills = list(profile.skills.values_list('name', flat=True))
    student_profile_data = {
        'cgpa': profile.cgpa,
        'tenth_marks': profile.ssc_percentage,
        'twelfth_marks': profile.hsc_percentage,
        'backlogs': profile.backlogs,
        'skills': student_skills
    }
    return render(request, 'Student/jobs.html', {
        'jobs_json': json.dumps(serialized),
        'student_profile_json': json.dumps(student_profile_data)
    })

@login_required
def student_interviews(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    schedules = Interview.objects.filter(student=profile)
    serialized = [serialize_interview(s) for s in schedules]
    return render(request, 'Student/interview.html', {
        'interviews_json': json.dumps(serialized)
    })

@login_required
def student_calendar(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    schedules = Interview.objects.filter(student=profile)
    events = []
    for s in schedules:
        events.append({
            'date': s.date.strftime('%Y-%m-%d') if s.date else "",
            'company': s.company_name or (s.recruiter.company_name if s.recruiter else "Company"),
            'type': s.round_name,
            'time': s.time.strftime('%I:%M %p') if s.time else ""
        })
    return render(request, 'Student/calendar.html', {
        'events_json': json.dumps(events)
    })

@login_required
def student_alumni(request):
    all_alumni = Alumni.objects.all()
    serialized = [serialize_alumni(a) for a in all_alumni]
    return render(request, 'Student/alumni.html', {
        'alumni_json': json.dumps(serialized)
    })

@login_required
def student_ats(request):
    return render(request, 'Student/ats.html')

def check_job_eligibility(student, job):
    if (
        student.cgpa >= job.min_cgpa and
        student.backlogs <= job.max_backlogs and
        student.tenth_marks >= job.min_tenth_marks and
        student.twelfth_marks >= job.min_twelfth_marks
    ):
        return True
    return False

@login_required
def api_apply_job(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            job_id = data.get('job_id')
            job = get_object_or_404(Job, id=job_id)
            profile = get_object_or_404(StudentProfile, user=request.user)
            
            # Eligibility validations
            if check_job_eligibility(profile, job):
                app, created = JobApplication.objects.get_or_create(
                    job=job,
                    student=profile,
                    defaults={'status': 'Under Review', 'score': 78} # Mock default ATS score
                )
                if created:
                    return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})
                else:
                    return JsonResponse({'success': False, 'error': 'You have already applied for this job.'})
            else:
                return JsonResponse({'success': False, 'error': 'You are not eligible for this job.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# Recruiter Views
@login_required
def recruiter_dashboard(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    
    # Calculate stats
    jobs_count = Job.objects.filter(recruiter=profile).count()
    applicants_count = JobApplication.objects.filter(job__recruiter=profile).count()
    shortlisted_count = JobApplication.objects.filter(job__recruiter=profile, status__in=['Shortlisted', 'shortlisted']).count()
    interviews_count = Interview.objects.filter(recruiter=profile).count()

    # Get data for charts
    roles_applicants = []
    recruiter_jobs = Job.objects.filter(recruiter=profile)
    for j in recruiter_jobs:
        roles_applicants.append({
            'title': j.title,
            'count': JobApplication.objects.filter(job=j).count()
        })

    return render(request, 'Recruiter/index.html', {
        'profile': profile,
        'jobs_count': jobs_count,
        'applicants_count': applicants_count,
        'shortlisted_count': shortlisted_count,
        'interviews_count': interviews_count,
        'roles_applicants_json': json.dumps(roles_applicants)
    })

@login_required
def recruiter_job_management(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    my_jobs = Job.objects.filter(recruiter=profile)
    
    # Add applicant counts to jobs
    jobs_with_stats = []
    for job in my_jobs:
        apps = JobApplication.objects.filter(job=job)
        jobs_with_stats.append({
            'job': job,
            'applicants_count': apps.count(),
            'in_review_count': apps.filter(status='Under Review').count()
        })
        
    return render(request, 'Recruiter/job-management.html', {
        'jobs_with_stats': jobs_with_stats,
        'profile': profile
    })

@login_required
def recruiter_applicants(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    apps = JobApplication.objects.filter(job__recruiter=profile)
    
    # Serialize applications
    applicants_list = []
    for app in apps:
        skills_str = ", ".join([s.name for s in app.student.skills.all()]) if app.student.skills.exists() else "No skills listed"
        applicants_list.append({
            'id': app.id,
            'name': app.student.user.full_name or app.student.user.email,
            'job_title': app.job.title,
            'college': app.student.college or "PCCOE Pune",
            'skills': skills_str,
            'cgpa': app.student.cgpa,
            'status': STATUS_DISPLAY_MAP.get(app.status, app.status),
            'score': app.score
        })
        
    return render(request, 'Recruiter/applicants.html', {
        'applicants_json': json.dumps(applicants_list)
    })

@login_required
def recruiter_interviews(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    schedules = Interview.objects.filter(recruiter=profile)
    
    interviews_list = []
    for s in schedules:
        is_online = 'http' in s.meeting_details.lower()
        interviews_list.append({
            'id': s.id,
            'candidate_name': s.student.user.full_name or s.student.user.email,
            'candidate_email': s.student.user.email,
            'position': s.round_name,
            'date': s.date.strftime('%Y-%m-%d') if s.date else "",
            'time': s.time.strftime('%H:%M') if s.time else "",
            'mode': 'online' if is_online else 'offline',
            'venue': "Online Video Call" if is_online else s.meeting_details,
            'meeting_url': s.meeting_details if is_online else "N/A"
        })
        
    return render(request, 'Recruiter/interviews.html', {
        'interviews_json': json.dumps(interviews_list)
    })

@login_required
def recruiter_analytics(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    
    active_jobs = Job.objects.filter(recruiter=profile, is_active=True).count()
    total_apps = JobApplication.objects.filter(job__recruiter=profile).count()
    interviews_count = Interview.objects.filter(recruiter=profile).count()
    total_placed = JobApplication.objects.filter(job__recruiter=profile, status__in=['Hired', 'hired']).count()
    
    # Calculate funnel data: [Applied, Screened, Interviewed, Placed]
    funnel_applied = total_apps
    funnel_screened = JobApplication.objects.filter(
        job__recruiter=profile, 
        status__in=['Shortlisted', 'Interviewed', 'Hired', 'shortlisted', 'technical_cleared', 'hr_cleared', 'hired']
    ).count()
    funnel_interviewed = Interview.objects.filter(recruiter=profile).values('student').distinct().count()
    funnel_placed = total_placed
    funnel_data = [funnel_applied, funnel_screened, funnel_interviewed, funnel_placed]
    
    # Hires by Department
    from django.db.models import Count
    hires_by_dept = JobApplication.objects.filter(
        job__recruiter=profile,
        status__in=['Hired', 'hired']
    ).values('student__major').annotate(count=Count('id'))
    
    dept_labels = []
    dept_data = []
    for item in hires_by_dept:
        major = item['student__major'] or 'General'
        dept_labels.append(major.upper())
        dept_data.append(item['count'])
        
    if not dept_labels:
        dept_labels = ['CS', 'Electrical', 'E&TC', 'Mech']
        dept_data = [0, 0, 0, 0]
        
    # Monthly Placement Trend (Jan - Jun)
    trend_data = [0, 0, 0, 0, 0, 0]
    for m in range(1, 7):
        trend_data[m-1] = JobApplication.objects.filter(
            job__recruiter=profile,
            status__in=['Hired', 'hired'],
            applied_at__month=m
        ).count()
        
    return render(request, 'Recruiter/analytics.html', {
        'profile': profile,
        'active_jobs': active_jobs,
        'total_apps': total_apps,
        'interviews_count': interviews_count,
        'total_placed': total_placed,
        'funnel_data': json.dumps(funnel_data),
        'dept_labels': json.dumps(dept_labels),
        'dept_data': json.dumps(dept_data),
        'trend_data': json.dumps(trend_data)
    })

@login_required
def recruiter_company_profile(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    if request.method == 'POST':
        profile.company_name = request.POST.get('companyName', profile.company_name)
        profile.description = request.POST.get('companyDescription', profile.description)
        profile.company_email = request.POST.get('contactEmail', profile.company_email)
        profile.email = request.POST.get('smtpEmail', profile.email)
        profile.gmail_app_password = request.POST.get('gmailAppPassword', profile.gmail_app_password)
        # Handle file uploads
        if request.FILES.get('logoUpload'):
            profile.logo = request.FILES.get('logoUpload')
        if request.FILES.get('brochureUpload'):
            profile.brochure = request.FILES.get('brochureUpload')
        profile.save()
        messages.success(request, "Company profile saved successfully!")
        return redirect('recruiter_company_profile')
        
    return render(request, 'Recruiter/company-profile.html', {'profile': profile})

@login_required
def recruiter_settings(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    if request.method == 'POST':
        current_p = request.POST.get('currentPassword')
        new_p = request.POST.get('newPassword')
        confirm_p = request.POST.get('confirmPassword')
        
        if request.user.check_password(current_p):
            if new_p == confirm_p:
                request.user.set_password(new_p)
                request.user.save()
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "New passwords do not match!")
        else:
            messages.error(request, "Incorrect current password!")
            
    return render(request, 'Recruiter/settings.html', {'profile': profile})

# API Endpoints for Recruiter
@login_required
def api_create_job(request):
    if request.method == 'POST':
        try:
            # Check user type to identify poster
            user = request.user
            if user.user_type == 'institute' or user.is_staff:
                posted_by = 'admin'
                recruiter = None
                company_name = request.POST.get('company_name')
            elif user.user_type == 'recruiter':
                profile = get_object_or_404(RecruiterProfile, user=user)
                posted_by = 'recruiter'
                recruiter = profile
                company_name = profile.company_name
            else:
                return JsonResponse({'success': False, 'error': 'Permission denied.'})

            title = request.POST.get('title')
            location = request.POST.get('location')
            ctc = request.POST.get('ctc', '₹ 610000 - ₹ 1000000 per Annum')
            skills = request.POST.get('skills', 'React, Python, SQL')
            description = request.POST.get('description', '')
            deadline_str = request.POST.get('deadline')
            
            deadline = None
            if deadline_str:
                try:
                    from datetime import datetime
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                except ValueError:
                    pass

            # Parse new eligibility criteria
            try:
                min_cgpa = float(request.POST.get('min_cgpa', 0.0) or 0.0)
                max_backlogs = int(request.POST.get('max_backlogs', 0) or 0)
                min_ssc_marks = float(request.POST.get('min_ssc_marks', 0.0) or 0.0)
                min_hsc_marks = float(request.POST.get('min_hsc_marks', 0.0) or 0.0)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid numeric values for eligibility criteria.'})
                
            round_shortlist = request.POST.get('round_shortlist', 'Shortlist Round')
            round_interview = request.POST.get('round_interview', 'Interview Round')
            round_final = request.POST.get('round_final', 'Final Selection Round')
            
            workflow = [round_shortlist, round_interview, round_final]
            criteria = [
                f"Minimum CGPA: {min_cgpa}",
                f"Maximum Allowed Backlogs: {max_backlogs}",
                f"Minimum 10th Marks: {min_ssc_marks}%",
                f"Minimum 12th Marks: {min_hsc_marks}%",
                f"Required Skills: {skills}"
            ]
            if deadline:
                criteria.append(f"Deadline: {deadline.strftime('%b %d, %Y')}")
            
            prep_checklist_raw = request.POST.get('preparation_checklist', '')
            if prep_checklist_raw:
                preparation_checklist = [x.strip() for x in prep_checklist_raw.split(',') if x.strip()]
            else:
                preparation_checklist = ["Revise basics", "Prepare resume walkthrough"]

            job = Job.objects.create(
                recruiter=recruiter,
                company_name=company_name,
                posted_by=posted_by,
                source=posted_by,
                posted_by_type=posted_by,
                deadline=deadline,
                title=title,
                location=location,
                ctc=ctc,
                skills_required=skills,
                description=description,
                min_cgpa=min_cgpa,
                max_backlogs=max_backlogs,
                min_ssc_marks=min_ssc_marks,
                min_hsc_marks=min_hsc_marks,
                workflow=workflow,
                criteria=criteria,
                preparation_checklist=preparation_checklist
            )
            return JsonResponse({'success': True, 'job_id': job.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def api_update_applicant_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            app_id = data.get('applicant_id')
            new_status = data.get('status')
            
            # Verify recruiter owns the job
            profile = get_object_or_404(RecruiterProfile, user=request.user)
            app = get_object_or_404(JobApplication, id=app_id, job__recruiter=profile)
            
            if new_status == 'Shortlisted':
                app.status = 'shortlisted'
            elif new_status == 'Interviewed':
                if app.status == 'technical_cleared':
                    app.status = 'hr_cleared'
                elif app.status == 'hr_cleared':
                    app.status = 'hr_cleared'
                else:
                    app.status = 'technical_cleared'
            elif new_status == 'Hired':
                app.status = 'hired'
            elif new_status == 'Rejected':
                app.status = 'rejected'
            else:
                app.status = new_status

            app.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def api_schedule_interview(request):
    if request.method == 'POST':
        try:
            profile = get_object_or_404(RecruiterProfile, user=request.user)
            candidate_email = request.POST.get('candidate_email')
            position = request.POST.get('position', 'Technical')
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            mode = request.POST.get('mode', 'online')
            venue = request.POST.get('venue', 'Online Video Call')
            meeting_url = request.POST.get('meeting_url', '')

            # Find matching student if exists
            student = StudentProfile.objects.filter(user__email=candidate_email).first()
            if not student:
                return JsonResponse({'success': False, 'error': f"No student with email '{candidate_email}' is registered in the system."})

            meeting_details = meeting_url if mode == 'online' else venue

            # Map position to round choices: 'Shortlist', 'Technical', 'HR', 'Final'
            round_name = 'Technical'
            pos_lower = position.lower() if position else ''
            if 'shortlist' in pos_lower:
                round_name = 'Shortlist'
            elif 'hr' in pos_lower:
                round_name = 'HR'
            elif 'final' in pos_lower or 'select' in pos_lower:
                round_name = 'Final'

            # Resolve job profile
            job_id = request.POST.get('job_id')
            job = None
            if job_id:
                job = Job.objects.filter(id=job_id).first()
            if not job:
                # Try by recruiter relation first
                app = JobApplication.objects.filter(student=student, job__recruiter=profile).first()
                if not app:
                    # Try by company name string match
                    app = JobApplication.objects.filter(
                        student=student, 
                        job__company_name__icontains=profile.company_name
                    ).first()
                if app:
                    job = app.job

            prep_checklist_raw = request.POST.get('preparation_checklist', '')
            if prep_checklist_raw:
                preparation_checklist = [x.strip() for x in prep_checklist_raw.split(',') if x.strip()]
            else:
                if job and job.preparation_checklist:
                    preparation_checklist = job.preparation_checklist
                else:
                    preparation_checklist = ["Revise basics", "Practice coding"]

            interview = Interview.objects.create(
                recruiter=profile,
                student=student,
                job=job,
                company_name=profile.company_name,
                round_name=round_name,
                meeting_details=meeting_details,
                date=date_str,
                time=time_str,
                prep_checklist=preparation_checklist,
                preparation_checklist=preparation_checklist,
                status='Confirmed'
            )

            # Send actual email to student registered email using Django Email Backend
            try:
                from django.conf import settings
                from django.core.mail import get_connection, EmailMessage, send_mail
                import traceback
                
                candidate_name = request.POST.get('candidate_name', '')
                student_name = student.user.full_name or candidate_name or student.user.email
                company_name = profile.company_name
                job_role = position
                round_val = round_name
                
                preparation_checklist_str = "\n".join([f"- {item}" for item in preparation_checklist])

                subject = f"Interview Invitation - {company_name}"
                message = f"Hello {student_name},\n\n" \
                          f"You have been invited for an interview.\n\n" \
                          f"Company: {company_name}\n" \
                          f"Job Role: {job_role}\n" \
                          f"Interview Round: {round_val}\n" \
                          f"Date: {date_str}\n" \
                          f"Time: {time_str}\n" \
                          f"Meeting Link: {meeting_details}\n\n" \
                          f"Preparation Checklist:\n{preparation_checklist_str}\n\n" \
                          f"Please be prepared.\n\n" \
                          f"Best Regards,\n{company_name}"

                # STEP 1 – DEBUG EVERYTHING
                print("--- SCHEDULE INTERVIEW SMTP DEBUGGING ---")
                print("Recruiter Email (profile.email):", repr(profile.email))
                print("Recruiter App Password (profile.gmail_app_password):", repr(profile.gmail_app_password))
                print("Student Email (candidate_email):", repr(candidate_email))
                print("Subject:", repr(subject))
                print("Message:", repr(message))

                email_sent = False

                # STEP 4 – VALIDATE APP PASSWORD
                if profile.email or profile.gmail_app_password:
                    if not profile.email:
                        print("SMTP Validation Error: Recruiter profile SMTP email is missing or blank.")
                    elif not profile.gmail_app_password:
                        print("SMTP Validation Error: Recruiter Gmail App Password is missing or blank.")
                    else:
                        clean_app_password = profile.gmail_app_password.strip()
                        if not clean_app_password:
                            print("SMTP Validation Error: Recruiter Gmail App Password is blank after stripping whitespace.")
                        elif ' ' in clean_app_password:
                            print("SMTP Validation Warning: Recruiter Gmail App Password contains spaces:", repr(profile.gmail_app_password))
                            # Clean the app password by removing all spaces to be robust
                            clean_app_password = clean_app_password.replace(" ", "")
                            print("Cleaned Recruiter App Password (no spaces):", repr(clean_app_password))
                        
                        if clean_app_password:
                            # STEP 2 – FORCE SMTP TEST & STEP 3 – SEND EMAIL WITH FULL ERROR TRACE
                            print("Attempting to connect to Gmail SMTP using recruiter credentials...")
                            try:
                                connection = get_connection(
                                    host='smtp.gmail.com',
                                    port=587,
                                    username=profile.email,
                                    password=clean_app_password,
                                    use_tls=True
                                )
                                connection.open()
                                print("SMTP Connected Successfully using recruiter credentials")
                                
                                email = EmailMessage(
                                    subject=subject,
                                    body=message,
                                    from_email=profile.email,
                                    to=[candidate_email],
                                    connection=connection
                                )
                                email.send(fail_silently=False)
                                print("Email Sent Successfully using recruiter credentials")
                                email_sent = True
                            except Exception as smtp_err:
                                print("SMTP Connection/Send Failed with recruiter credentials:", str(smtp_err))
                                traceback.print_exc()
                                print("Falling back to system SMTP...")

                # STEP 6 – FALLBACK SYSTEM
                if not email_sent:
                    print("Attempting fallback: sending email using system SMTP credentials...")
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            [candidate_email],
                            fail_silently=False,
                        )
                        print("Email Sent Successfully using system credentials")
                        email_sent = True
                    except Exception as fallback_err:
                        print("System SMTP Fallback Failed:", str(fallback_err))
                        traceback.print_exc()
                        raise fallback_err

            except Exception as mail_err:
                import logging
                logger = logging.getLogger(__name__)
                logger.error("SMTP error during scheduling interview:", exc_info=True)
                print("--- EMAIL SENDING ERROR START ---")
                traceback.print_exc()
                print("--- EMAIL SENDING ERROR END ---")

            return JsonResponse({'success': True, 'id': interview.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def api_delete_interview(request, pk):
    if request.method == 'POST':
        try:
            profile = get_object_or_404(RecruiterProfile, user=request.user)
            interview = get_object_or_404(Interview, id=pk, recruiter=profile)
            interview.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def api_delete_job(request, pk):
    if request.method == 'POST':
        try:
            profile = get_object_or_404(RecruiterProfile, user=request.user)
            job = get_object_or_404(Job, id=pk, recruiter=profile)
            job.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# Admin TPO views
@login_required
def admin_portal(request):
    # Verify user is institute admin or staff
    if request.user.user_type != 'institute' and not request.user.is_staff:
        return redirect('student_profile')
        
    # Get statistics
    total_students = StudentProfile.objects.count()
    placed_students = JobApplication.objects.filter(status__in=['Hired', 'hired']).values('student').distinct().count()
    unplaced_students = total_students - placed_students
    ongoing_rounds = Interview.objects.filter(status='Confirmed').count()
    
    rate = 0.0
    if total_students > 0:
        rate = round((placed_students / total_students) * 100, 1)

    # Get student enrollment records
    students_list = []
    all_students = StudentProfile.objects.all()
    for s in all_students:
        # Find if hired
        hired_app = JobApplication.objects.filter(student=s, status__in=['Hired', 'hired']).first()
        status_str = "Unplaced"
        status_class = "Unplaced"
        if hired_app:
            status_str = f"Placed - {hired_app.job.company_name or (hired_app.job.recruiter.company_name if hired_app.job.recruiter else 'N/A')}"
            status_class = "Placed"
        else:
            # Check if ongoing round
            int_sched = Interview.objects.filter(student=s, status='Confirmed').first()
            if int_sched:
                status_str = f"Round {int_sched.round_name} Ongoing"
                status_class = "Ongoing"

        students_list.append({
            'name': s.user.full_name or s.user.email,
            'dept': s.major or "CSE",
            'cgpa': s.cgpa,
            'status': status_str,
            'status_class': status_class
        })

    # Prepare chart data for department placements
    all_majors = list(StudentProfile.objects.exclude(major='').values_list('major', flat=True).distinct())
    if not all_majors:
        all_majors = ['CSE', 'IT', 'ECE', 'ME']
    dept_labels = [m.upper() for m in all_majors]
    dept_placed_data = []
    for m in all_majors:
        placed_count = JobApplication.objects.filter(status__in=['Hired', 'hired'], student__major=m).values('student').distinct().count()
        dept_placed_data.append(placed_count)

    # Prepare Selection Funnel: Shortlist, Interview, Hire, Reject
    shortlist_c = JobApplication.objects.filter(status__in=['Shortlisted', 'shortlisted']).count()
    interview_c = Interview.objects.filter(status='Confirmed').values('student').distinct().count() + JobApplication.objects.filter(status__in=['Interviewed', 'technical_cleared', 'hr_cleared']).count()
    hire_c = JobApplication.objects.filter(status__in=['Hired', 'hired']).count()
    reject_c = JobApplication.objects.filter(status__in=['Rejected', 'rejected']).count()
    round_chart_data = [shortlist_c, interview_c, hire_c, reject_c]

    # Placement drives list dynamically from Jobs
    active_jobs = Job.objects.filter(is_active=True)
    drives = []
    for job in active_jobs:
        drives.append({
            'company_name': job.company_name or (job.recruiter.company_name if job.recruiter else "N/A"),
            'date': job.created_at.strftime('%b %d, %Y'),
            'title': job.title,
            'eligibility': f"CGPA >= {job.min_cgpa}, SSC >= {job.min_ssc_marks}%, HSC >= {job.min_hsc_marks}%, Backlogs <= {job.max_backlogs}",
            'applied_count': job.applications.count(),
            'max_applications': 500,
            'status': 'Active' if job.is_active else 'Closed'
        })

    # New telemetry counters
    total_recruiters = RecruiterProfile.objects.count()
    total_companies = RecruiterProfile.objects.exclude(company_name='').values('company_name').distinct().count()
    active_jobs_count = Job.objects.filter(is_active=True).count()
    total_applications = JobApplication.objects.count()
    total_shortlisted = shortlist_c
    total_interviews = Interview.objects.count()
    total_hired = JobApplication.objects.filter(status__in=['Hired', 'hired']).count()
    total_rejected = JobApplication.objects.filter(status__in=['Rejected', 'rejected']).count()

    # Query alumni list and partner companies list
    alumni = Alumni.objects.all()
    company_names = list(RecruiterProfile.objects.exclude(company_name='').values_list('company_name', flat=True).distinct())

    return render(request, 'admin/admin.html', {
        'total_students': total_students,
        'placed_students': placed_students,
        'unplaced_students': unplaced_students,
        'ongoing_rounds': ongoing_rounds,
        'rate': rate,
        'students_list': students_list,
        'drives': drives,
        'dept_labels': json.dumps(dept_labels),
        'dept_placed_data': json.dumps(dept_placed_data),
        'round_chart_data': json.dumps(round_chart_data),
        
        # Aggregated Telemetry
        'total_recruiters': total_recruiters,
        'total_companies': total_companies,
        'active_jobs_count': active_jobs_count,
        'total_applications': total_applications,
        'total_shortlisted': total_shortlisted,
        'total_interviews': total_interviews,
        'total_hired': total_hired,
        'total_rejected': total_rejected,
        
        # Alumni and Companies lists
        'alumni': alumni,
        'company_names': company_names
    })

@login_required
def admin_post_job(request):
    if request.user.user_type != 'institute' and not request.user.is_staff:
        return redirect('student_profile')
        
    total_students = StudentProfile.objects.count()
    placed_students = JobApplication.objects.filter(status='Hired').values('student').distinct().count()
    unplaced_students = total_students - placed_students
    ongoing_rounds = Interview.objects.filter(status='Confirmed').count()
    
    shortlist_c = JobApplication.objects.filter(status='Shortlisted').count()
    total_recruiters = RecruiterProfile.objects.count()
    total_companies = RecruiterProfile.objects.exclude(company_name='').values('company_name').distinct().count()
    active_jobs_count = Job.objects.filter(is_active=True).count()
    total_applications = JobApplication.objects.count()
    total_shortlisted = shortlist_c
    total_interviews = Interview.objects.count()
    total_hired = JobApplication.objects.filter(status='Hired').count()
    total_rejected = JobApplication.objects.filter(status='Rejected').count()
    
    alumni = Alumni.objects.all()

    return render(request, 'admin/admin_post_job.html', {
        'total_students': total_students,
        'placed_students': placed_students,
        'unplaced_students': unplaced_students,
        'ongoing_rounds': ongoing_rounds,
        'total_recruiters': total_recruiters,
        'total_companies': total_companies,
        'active_jobs_count': active_jobs_count,
        'total_applications': total_applications,
        'total_shortlisted': total_shortlisted,
        'total_interviews': total_interviews,
        'total_hired': total_hired,
        'total_rejected': total_rejected,
        'alumni': alumni,
    })

@login_required
def edit_job(request, job_id):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id, recruiter=profile)
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            location = request.POST.get('location')
            ctc = request.POST.get('ctc')
            skills = request.POST.get('skills')
            description = request.POST.get('description')
            
            deadline_str = request.POST.get('deadline')
            deadline = None
            if deadline_str:
                try:
                    from datetime import datetime
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                except ValueError:
                    pass

            min_cgpa = float(request.POST.get('min_cgpa', 0.0) or 0.0)
            max_backlogs = int(request.POST.get('max_backlogs', 0) or 0)
            min_ssc_marks = float(request.POST.get('min_ssc_marks', 0.0) or 0.0)
            min_hsc_marks = float(request.POST.get('min_hsc_marks', 0.0) or 0.0)
            
            round_shortlist = request.POST.get('round_shortlist')
            round_interview = request.POST.get('round_interview')
            round_final = request.POST.get('round_final')
            
            workflow = [round_shortlist, round_interview, round_final]
            criteria = [
                f"Minimum CGPA: {min_cgpa}",
                f"Maximum Allowed Backlogs: {max_backlogs}",
                f"Minimum 10th Marks: {min_ssc_marks}%",
                f"Minimum 12th Marks: {min_hsc_marks}%",
                f"Required Skills: {skills}"
            ]
            if deadline:
                criteria.append(f"Deadline: {deadline.strftime('%b %d, %Y')}")
                
            prep_checklist_raw = request.POST.get('preparation_checklist', '')
            if prep_checklist_raw:
                preparation_checklist = [x.strip() for x in prep_checklist_raw.split(',') if x.strip()]
            else:
                preparation_checklist = ["Revise basics", "Prepare resume walkthrough"]

            job.title = title
            job.location = location
            job.ctc = ctc
            job.skills_required = skills
            job.description = description
            job.deadline = deadline
            job.min_cgpa = min_cgpa
            job.max_backlogs = max_backlogs
            job.min_ssc_marks = min_ssc_marks
            job.min_hsc_marks = min_hsc_marks
            job.workflow = workflow
            job.criteria = criteria
            job.preparation_checklist = preparation_checklist
            job.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    my_jobs = Job.objects.filter(recruiter=profile)
    jobs_with_stats = []
    for j in my_jobs:
        apps = JobApplication.objects.filter(job=j)
        jobs_with_stats.append({
            'job': j,
            'applicants_count': apps.count(),
            'in_review_count': apps.filter(status='Under Review').count()
        })
        
    return render(request, 'Recruiter/job-management.html', {
        'jobs_with_stats': jobs_with_stats,
        'profile': profile,
        'editing_job': job
    })

@login_required
def api_update_student_round(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_name = data.get('student_name')
            new_round = data.get('round')
            
            # Find the user by full_name
            user = CustomUser.objects.filter(full_name=student_name).first()
            if user:
                student_profile = StudentProfile.objects.get(user=user)
                # Update ongoing interview schedule if any
                sched = Interview.objects.filter(student=student_profile, status='Confirmed').first()
                if sched:
                    if new_round == 'Selected':
                        sched.status = 'Completed'
                        # Create a hired job application
                        job = Job.objects.filter(recruiter=sched.recruiter).first()
                        if job:
                            app, _ = JobApplication.objects.get_or_create(job=job, student=student_profile)
                            app.status = 'hired'
                            app.save()
                    elif new_round == 'Rejected':
                        sched.status = 'Cancelled'
                        job = Job.objects.filter(recruiter=sched.recruiter).first()
                        if job:
                            app = JobApplication.objects.filter(job=job, student=student_profile).first()
                            if app:
                                app.status = 'rejected'
                                app.save()
                    else:
                        # Move round
                        sched.round_name = new_round
                    sched.save()
                    return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Student or active schedule not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def admin_add_alumni(request):
    if request.user.user_type != 'institute' and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            company = request.POST.get('company')
            role = request.POST.get('role', 'Software Engineer')
            batch = request.POST.get('batch')
            linkedin = request.POST.get('linkedin', '')
            testimonial = request.POST.get('testimonial', '')
            image = request.FILES.get('image')
            
            Alumni.objects.create(
                name=name,
                company=company,
                role=role,
                batch=batch,
                linkedin=linkedin,
                testimonial=testimonial,
                image=image
            )
            return redirect('admin_portal')
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def admin_edit_alumni(request, pk):
    if request.user.user_type != 'institute' and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    if request.method == 'POST':
        try:
            alumni = get_object_or_404(Alumni, id=pk)
            alumni.name = request.POST.get('name', alumni.name)
            alumni.company = request.POST.get('company', alumni.company)
            alumni.role = request.POST.get('role', alumni.role)
            alumni.batch = request.POST.get('batch', alumni.batch)
            alumni.linkedin = request.POST.get('linkedin', alumni.linkedin)
            alumni.testimonial = request.POST.get('testimonial', alumni.testimonial)
            
            if request.FILES.get('image'):
                alumni.image = request.FILES.get('image')
                
            alumni.save()
            return redirect('admin_portal')
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def admin_delete_alumni(request, pk):
    if request.user.user_type != 'institute' and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    if request.method == 'POST':
        try:
            alumni = get_object_or_404(Alumni, id=pk)
            alumni.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def api_company_pipeline(request):
    if request.user.user_type != 'institute' and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    company_name = request.GET.get('company')
    if not company_name:
        return JsonResponse({'success': False, 'error': 'Company name is required.'})
        
    applications = JobApplication.objects.filter(job__recruiter__company_name=company_name)
    data = []
    for app in applications:
        sched = Interview.objects.filter(student=app.student, company_name=company_name, status='Confirmed').first()
        current_round = sched.round_name if sched else "None"
        data.append({
            'student_name': app.student.user.full_name or app.student.user.email,
            'job_title': app.job.title,
            'status': STATUS_DISPLAY_MAP.get(app.status, app.status),
            'current_round': current_round,
            'applied_at': app.applied_at.strftime('%Y-%m-%d'),
            'score': app.score
        })
    return JsonResponse({'success': True, 'applications': data})

