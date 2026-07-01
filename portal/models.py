from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('recruiter', 'Recruiter'),
        ('institute', 'Institute Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, blank=True)
    college = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255, blank=True)
    cgpa = models.FloatField(default=0.0)
    ssc_percentage = models.FloatField(default=0.0) # 10th
    hsc_percentage = models.FloatField(default=0.0) # 12th
    backlogs = models.IntegerField(default=0)
    location = models.CharField(max_length=255, default='Pune, India')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    @property
    def tenth_marks(self):
        return self.ssc_percentage

    @tenth_marks.setter
    def tenth_marks(self, value):
        self.ssc_percentage = value

    @property
    def twelfth_marks(self):
        return self.hsc_percentage

    @twelfth_marks.setter
    def twelfth_marks(self, value):
        self.hsc_percentage = value

    def __str__(self):
        return f"Student: {self.user.full_name or self.user.email}"

class StudentInternship(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='internships')
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    duration = models.CharField(max_length=100) # e.g. "6 months"
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role} at {self.company}"

class StudentSkill(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StudentProject(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class StudentCertification(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    authority = models.CharField(max_length=255) # Issuing body

    def __str__(self):
        return self.name

class StudentActivity(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='activities')
    description = models.TextField()

    def __str__(self):
        return self.description[:50]

class StudentResume(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume of {self.student_profile.user.full_name}"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, blank=True)
    company_email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    brochure = models.FileField(upload_to='company_brochures/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gmail_app_password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Recruiter: {self.user.full_name or self.user.email} ({self.company_name})"

class InstituteProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='institute_profile')
    institute_name = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Institute Admin: {self.user.full_name or self.user.email} ({self.institute_name})"

class Job(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    posted_by = models.CharField(max_length=20, choices=(('recruiter', 'Recruiter'), ('admin', 'Admin')), default='recruiter')
    deadline = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, default='Full Time') 
    ctc = models.CharField(max_length=100) 
    category = models.CharField(max_length=255, default='Engineering - Web / Software')
    description = models.TextField()
    skills_required = models.CharField(max_length=255, blank=True) 
    
    # Eligibility requirements
    min_cgpa = models.FloatField(default=0.0)
    min_ssc_marks = models.FloatField(default=0.0)
    min_hsc_marks = models.FloatField(default=0.0)
    max_backlogs = models.IntegerField(default=0)

    workflow = models.JSONField(default=list) 
    criteria = models.JSONField(default=list) 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=20, choices=(('recruiter', 'Recruiter'), ('admin', 'Admin')), default='recruiter')
    posted_by_type = models.CharField(max_length=20, choices=(('recruiter', 'Recruiter'), ('admin', 'Admin')), default='recruiter')
    preparation_checklist = models.JSONField(default=list)

    @property
    def min_tenth_marks(self):
        return self.min_ssc_marks

    @min_tenth_marks.setter
    def min_tenth_marks(self, value):
        self.min_ssc_marks = value

    @property
    def min_twelfth_marks(self):
        return self.min_hsc_marks

    @min_twelfth_marks.setter
    def min_twelfth_marks(self, value):
        self.min_hsc_marks = value

    def __str__(self):
        comp = self.company_name or (self.recruiter.company_name if self.recruiter else "N/A")
        return f"{self.title} at {comp}"

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('Under Review', 'Under Review'),
        ('shortlisted', 'shortlisted'),
        ('technical_cleared', 'technical_cleared'),
        ('hr_cleared', 'hr_cleared'),
        ('hired', 'hired'),
        ('rejected', 'rejected'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Under Review')
    score = models.IntegerField(default=75) 

    class Meta:
        unique_together = ('job', 'student')

    def __str__(self):
        return f"{self.student.user.full_name} for {self.job.title}"

class Interview(models.Model):
    ROUND_CHOICES = (
        ('Shortlist', 'Shortlist'),
        ('Technical', 'Technical'),
        ('HR', 'HR'),
        ('Final', 'Final Selection'),
    )
    STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    )
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='interviews')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='interviews')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, related_name='interviews')
    company_name = models.CharField(max_length=255)
    round_name = models.CharField(max_length=50, choices=ROUND_CHOICES, default='Shortlist')
    meeting_details = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    prep_checklist = models.JSONField(default=list)
    preparation_checklist = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')

    def __str__(self):
        return f"Interview: {self.student.user.full_name} with {self.company_name} ({self.round_name})"

class Alumni(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255, default='Software Engineer')
    batch = models.CharField(max_length=50, default='2026', blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='alumni_images/', blank=True, null=True)
    testimonial = models.TextField(blank=True)
    
    # Optional fields for backward compatibility
    year = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    initials = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Alumni: {self.name} ({self.company})"

class PlacementDrive(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('Completed', 'Completed'),
    )
    company_name = models.CharField(max_length=255)
    title = models.CharField(default="", max_length=255)
    date = models.CharField(max_length=50)
    eligibility = models.CharField(max_length=255)
    max_applications = models.IntegerField(default=500)
    applied_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"Drive: {self.title or self.company_name}"
