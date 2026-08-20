# HireLink - Hybrid Campus Placement System

Project Authors(Team members and contribution)
### 1. Saurabh Bhosale
**Role:** Recruiter/Employer Module & Frontend Development

- Developed the Recruiter/Employer module
- Designed and developed recruiter login
- Developed recruiter dashboard
- Developed job posting and job management pages
- Developed applicant management functionality
- Developed interview management pages
- Developed company profile and settings pages
- Worked with HTML, CSS and JavaScript
- Git/GitHub collaboration and frontend integration

### 2. Tanmay Dahivalikar
**Role:** Student Module & Frontend Development

- Developed the Student module
- Student registration and login
- Student profile management
- Job browsing and searching
- Job filtering
- Job application functionality
- Resume upload functionality
- Student-side frontend development

### 3. Bhageshree Giri
**Role:** TPO Module & Placement Management

- Developed the TPO module
- TPO dashboard
- Job posting approval/rejection
- Student and recruiter management
- Application monitoring
- Placement monitoring
- TPO-side frontend development

### 4. Omkar Ingale
**Role:** Backend & Database Development

- Developed Django backend functionality
- Designed database models
- Implemented authentication and authorization
- Database integration
- Django migrations
- Backend logic and integration
- Testing and debugging

HireLink is a unified, secure campus recruitment and placement drive management portal designed to streamline interactions between **Students**, **Recruiters**, and **TPO Admins (Training and Placement Officers)**. It automates registration, job postings, eligibility vetting, application processing, interview scheduling, and placement analytics.

---

## 🚀 Key Features

### 1. Student Portal
* **Profile Management**: Build resume details, academic criteria (CGPA, 10th and 12th marks, active backlogs count).
* **Strict Eligibility Checker**: Enforces requirements dynamically based on recruiter-specified criteria (e.g. minimum CGPA, maximum backlogs) to restrict applications to eligible students only.
* **Interview Progress Roadmap**: Real-time status roadmap visualization corresponding to backend applicant transitions:
  * *Shortlist* ➔ *Technical Interview* ➔ *HR Interview* ➔ *Final Selection*
* **Interview Calendar**: Automatically populates scheduled interviews and upcoming recruiter visits on a student calendar.
*** * Alumni Connect
*** ATS resume score**

### 2. Recruiter Portal
* **Job Management**: Create, edit, and post job profiles with detailed salary packages, skill requirements, and criteria.
* **Applicant Pipeline**: Review candidates, view matching scores, and transition applicant stages (*Shortlist*, *Interview*, *Hire*, *Reject*) in real-time.
* **Custom SMTP Integration**: Recruiters can save their own Gmail addresses and App Passwords to dispatch personalized interview invitation emails directly from their own accounts rather than system notifications.
* **Funnel Analytics**: Visualize placement drive funnels, hire ratios, and monthly recruitment trends.

### 3. TPO Admin Dashboard
* **Analytics Telemetry**: High-level tracking of campus placement statistics, including overall placement rates, hired vs. rejected student funnels, and department-wise counts.
* **Placement Drive Creator**: Post placement drives on behalf of companies that render directly on student boards.
* **Enrollment Management**: Manage student data, check active recruitment rounds, and track placement status across departments.

---

## 🛠️ Technology Stack
* **Backend**: Django (Python 3), Django ORM, SQLite
* **Frontend**: HTML5, CSS3 (Vanilla Custom Styles), JavaScript (Vanilla ES6)
* **Services**: SMTP Relay server (Google) for dynamic emails

---

## 💻 Setup & Installation Instructions

### Prerequisites
* Python 3.8+ installed
* Pip (Python package manager)

### 1. Clone the repository and navigate to folder
```bash
git clone <your-github-repo-url>
cd hirelink/campus-backup
```

### 2. Set up the Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. Install dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### 4. Run Migrations
Generate database tables in SQLite:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Mock Data (Optional)
Populate the database with default recruiters, students, and admins:
```bash
python populate.py
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit the site at: `http://127.0.0.1:8000/`


