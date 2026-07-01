from django.urls import path
from . import views

urlpatterns = [
    # Landing Pages
    path('', views.index, name='home'),
    path('institute/', views.institute, name='institute'),
    path('recruiter-landing/', views.recruiter_landing, name='recruiter_landing'),
    path('admin-landing/', views.admin_landing, name='admin_landing'),
    path('student-landing/', views.student_landing, name='student_landing'),
    path('role/', views.role_selector, name='role_selector'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Student Dashboard
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/jobs/', views.student_jobs, name='student_jobs'),
    path('student/interview/', views.student_interviews, name='student_interviews'),
    path('student/calendar/', views.student_calendar, name='student_calendar'),
    path('student/alumni/', views.student_alumni, name='student_alumni'),
    path('student/ats/', views.student_ats, name='student_ats'),

    # Student Profile CRUD URLs
    path('student/profile/photo/', views.update_profile_photo, name='update_profile_photo'),
    path('student/profile/basic/', views.update_profile_basic, name='update_profile_basic'),
    path('student/profile/education/', views.update_profile_education, name='update_profile_education'),
    
    path('student/profile/internship/add/', views.add_profile_internship, name='add_profile_internship'),
    path('student/profile/internship/delete/<int:pk>/', views.delete_profile_internship, name='delete_profile_internship'),
    
    path('student/profile/skill/add/', views.add_profile_skill, name='add_profile_skill'),
    path('student/profile/skill/delete/<int:pk>/', views.delete_profile_skill, name='delete_profile_skill'),
    
    path('student/profile/project/add/', views.add_profile_project, name='add_profile_project'),
    path('student/profile/project/delete/<int:pk>/', views.delete_profile_project, name='delete_profile_project'),
    
    path('student/profile/certification/add/', views.add_profile_certification, name='add_profile_certification'),
    path('student/profile/certification/delete/<int:pk>/', views.delete_profile_certification, name='delete_profile_certification'),
    
    path('student/profile/activity/add/', views.add_profile_activity, name='add_profile_activity'),
    path('student/profile/activity/delete/<int:pk>/', views.delete_profile_activity, name='delete_profile_activity'),
    
    path('student/profile/resume/upload/', views.upload_profile_resume, name='upload_profile_resume'),
    path('student/profile/resume/delete/<int:pk>/', views.delete_profile_resume, name='delete_profile_resume'),

    # Student APIs
    path('api/apply/', views.api_apply_job, name='api_apply_job'),

    # Recruiter Dashboard
    path('recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/jobs/', views.recruiter_job_management, name='recruiter_jobs'),
    path('recruiter/job/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('recruiter/applicants/', views.recruiter_applicants, name='recruiter_applicants'),
    path('recruiter/interviews/', views.recruiter_interviews, name='recruiter_interviews'),
    path('recruiter/analytics/', views.recruiter_analytics, name='recruiter_analytics'),
    path('recruiter/profile/', views.recruiter_company_profile, name='recruiter_company_profile'),
    path('recruiter/settings/', views.recruiter_settings, name='recruiter_settings'),

    # Recruiter APIs
    path('api/jobs/create/', views.api_create_job, name='api_create_job'),
    path('api/jobs/delete/<int:pk>/', views.api_delete_job, name='api_delete_job'),
    path('api/applicants/update-status/', views.api_update_applicant_status, name='api_update_applicant_status'),
    path('api/interviews/create/', views.api_schedule_interview, name='api_schedule_interview'),
    path('api/interviews/delete/<int:pk>/', views.api_delete_interview, name='api_delete_interview'),

    # Admin TPO Console
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    path('admin-portal/post-job/', views.admin_post_job, name='admin_post_job'),
    path('api/update-round/', views.api_update_student_round, name='api_update_student_round'),
    path('admin-portal/alumni/add/', views.admin_add_alumni, name='admin_add_alumni'),
    path('admin-portal/alumni/edit/<int:pk>/', views.admin_edit_alumni, name='admin_edit_alumni'),
    path('admin-portal/alumni/delete/<int:pk>/', views.admin_delete_alumni, name='admin_delete_alumni'),
    path('api/admin/company-pipeline/', views.api_company_pipeline, name='api_company_pipeline'),
]
