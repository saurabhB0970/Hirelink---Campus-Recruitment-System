// Use backend jobs if available, fallback to mock list
const jobs = window.backendJobs || [
    {
        id: 1,
        title: "Technical Business Analyst / Android / Flutter Developer",
        company: "CHETU Inc.",
        location: "Noida",
        type: "Full Time",
        posted: "10 days ago",
        ctc: "₹ 610000 - ₹ 1000000 per Annum",
        category: "Engineering - Web / Software",
        description: "Join Chetu Inc., a world-class software services provider. We are looking for talented developers to work on cutting-edge technologies.",
        workflow: ["Aptitude Round", "Technical MCQ Test", "Coding Interview", "Technical Interview 1", "HR Interview"],
        criteria: ["No active backlogs", "Minimum 60% in 10th & 12th", "B.Tech/BE Computer Science preferred", "Knowledge of Flutter/Dart"],
        applied: false
    },
    {
        id: 2,
        title: "MERN Stack Developer Intern",
        company: "DataDynamx Pvt Ltd",
        location: "Pune",
        type: "Internship",
        posted: "23 days ago",
        ctc: "₹ 15000 - ₹ 20000 per Month",
        category: "Web Development",
        description: "Exciting opportunity to work on live projects using React, Node.js, and MongoDB.",
        workflow: ["Task-based Assessment", "Technical Interview", "Final Selection"],
        criteria: ["Available for 6 months", "Strong JavaScript knowledge", "Pune local preferred"],
        applied: false
    }
];


let selectedJobId = null;
let currentListView = 'all';

// Initialize
function init() {
    renderJobList();
}

function renderJobList() {
    const container = document.getElementById('jobCardsContainer');
    container.innerHTML = '';

    const filteredJobs = currentListView === 'all' 
        ? jobs 
        : jobs.filter(j => j.applied);

    filteredJobs.forEach(job => {
        const card = document.createElement('div');
        card.className = `job-card ${selectedJobId === job.id ? 'selected' : ''}`;
        card.onclick = () => selectJob(job.id);
        card.innerHTML = `
            <h4>${job.title}</h4>
            <p>${job.company} | ${job.location}</p>
            <p>${job.type}</p>
            <p class="time">${job.posted}</p>
        `;
        container.appendChild(card);
    });
}

function selectJob(id) {
    selectedJobId = id;
    const job = jobs.find(j => j.id === id);
    
    // Update Header
    document.getElementById('viewTitle').innerText = job.title;
    document.getElementById('viewMeta').innerText = `${job.company} | ${job.location} | ${job.type}`;
    
    const banner = document.getElementById('statusBanner');
    const applyFooter = document.getElementById('applyFooter');
    
    if(job.applied) {
        banner.innerHTML = "✅ You have already applied for this position.";
        applyFooter.style.display = 'none';
    } else {
        const student = window.studentProfile;
        let eligible = true;
        let reasons = [];

        if (student) {
            const minCgpa = parseFloat(job.min_cgpa) || 0;
            const minTenth = parseFloat(job.min_tenth_marks) || 0;
            const minTwelfth = parseFloat(job.min_twelfth_marks) || 0;
            const maxBacklogs = parseInt(job.max_backlogs) || 0;

            const studentCgpa = parseFloat(student.cgpa) || 0;
            const studentTenth = parseFloat(student.tenth_marks) || 0;
            const studentTwelfth = parseFloat(student.twelfth_marks) || 0;
            const studentBacklogs = parseInt(student.backlogs) || 0;

            if (studentCgpa < minCgpa) {
                eligible = false;
                reasons.push(`CGPA requirement: minimum ${minCgpa} (yours: ${studentCgpa})`);
            }
            if (studentTenth < minTenth) {
                eligible = false;
                reasons.push(`10th marks requirement: minimum ${minTenth}% (yours: ${studentTenth}%)`);
            }
            if (studentTwelfth < minTwelfth) {
                eligible = false;
                reasons.push(`12th marks requirement: minimum ${minTwelfth}% (yours: ${studentTwelfth}%)`);
            }
            if (studentBacklogs > maxBacklogs) {
                eligible = false;
                reasons.push(`Backlogs requirement: maximum ${maxBacklogs} allowed (yours: ${studentBacklogs})`);
            }
        }

        if (!eligible) {
            banner.innerHTML = "<span style='color: #dc3545; font-weight: bold;'>❌ You are not eligible for this job.</span>";
            applyFooter.style.display = 'none';
        } else {
            banner.innerHTML = "! Applications are currently open. Check eligibility before applying.";
            applyFooter.style.display = 'block';
        }
    }

    // Update Description Tab
    document.getElementById('jobSummaryText').innerHTML = `
        <p><strong>Category:</strong> ${job.category}</p>
        <p><strong>Job Profile CTC:</strong> ${job.ctc}</p>
    `;
    document.getElementById('jobDescText').innerText = job.description;

    // Update Workflow Tab
    const wList = document.getElementById('workflowList');
    wList.innerHTML = job.workflow.map((step, index) => `<li><strong>Round ${index+1}:</strong> ${step}</li>`).join('');

    // Update Criteria Tab
    const cList = document.getElementById('criteriaList');
    cList.innerHTML = job.criteria.map(c => `<li>${c}</li>`).join('');

    renderJobList(); // Re-render to show selection
}

function switchList(view) {
    currentListView = view;
    document.querySelectorAll('.list-tab').forEach(t => t.classList.toggle('active'));
    renderJobList();
}

function switchDetailTab(event, tabId) {
    document.querySelectorAll('.det-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    
    event.currentTarget.classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

function applyToJob() {
    const job = jobs.find(j => j.id === selectedJobId);
    
    // Send application request to backend
    fetch('/api/apply/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': typeof getCookie === 'function' ? getCookie('csrftoken') : ''
        },
        body: JSON.stringify({ job_id: selectedJobId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            job.applied = true;
            alert(data.message || "Application submitted successfully!");
            selectJob(selectedJobId);
        } else {
            alert(data.error || "Failed to submit application.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}

init();