from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    StudentProfile,
    StudentInternship,
    StudentSkill,
    StudentProject,
    StudentCertification,
    StudentActivity,
    StudentResume,
    RecruiterProfile,
    InstituteProfile,
    Job,
    JobApplication,
    Interview,
    Alumni,
    PlacementDrive
)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'user_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'full_name', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'full_name', 'phone_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(StudentInternship)
admin.site.register(StudentSkill)
admin.site.register(StudentProject)
admin.site.register(StudentCertification)
admin.site.register(StudentActivity)
admin.site.register(StudentResume)
admin.site.register(RecruiterProfile)
admin.site.register(InstituteProfile)
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(Interview)
admin.site.register(Alumni)
admin.site.register(PlacementDrive)
