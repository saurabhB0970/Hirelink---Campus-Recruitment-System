// Use backend interviews if available, fallback to mock list
const interviews = window.backendInterviews || [
    {
        id: 1,
        company: "SAP Labs",
        role: "ABAP Developer Intern",
        date: "March 05, 2026",
        time: "11:00 AM",
        interviewer: "Rahul Sharma (Sr. Architect)",
        status: "Confirmed",
        currentRound: 2,
        rounds: ["Aptitude", "Technical Interview 1", "Technical Interview 2", "HR Round"],
        prep: ["Revise SAP BTP basics", "Practice SQL Queries", "Understand OData services"]
    },
    {
        id: 2,
        company: "Google",
        role: "Associate Software Engineer",
        date: "March 12, 2026",
        time: "03:30 PM",
        interviewer: "Jessica Chen",
        status: "Confirmed",
        currentRound: 1,
        rounds: ["Online Coding", "Phone Screen", "Onsite Round 1", "Onsite Round 2"],
        prep: ["Graph Algorithms", "System Design Basics", "Dynamic Programming"]
    }
];


function init() {
    const listContainer = document.getElementById('interviewList');
    interviews.forEach(int => {
        const card = document.createElement('div');
        card.className = 'int-card';
        card.onclick = () => showInterview(int.id, card);
        card.innerHTML = `
            <h4>${int.company}</h4>
            <p>${int.role}</p>
            <p><strong>${int.date} | ${int.time}</strong></p>
        `;
        listContainer.appendChild(card);
    });
}

function showInterview(id, cardElement) {
    // UI Updates
    document.querySelectorAll('.int-card').forEach(c => c.classList.remove('active'));
    cardElement.classList.add('active');
    document.getElementById('placeholder').style.display = 'none';
    document.getElementById('contentArea').style.display = 'block';

    const data = interviews.find(i => i.id === id);

    // Data Binding
    document.getElementById('compName').innerText = data.company;
    document.getElementById('roleName').innerText = data.role;
    document.getElementById('meetDate').innerText = data.date;
    document.getElementById('meetTime').innerText = data.time;
    document.getElementById('interviewer').innerText = data.interviewer;
    document.getElementById('statusTag').innerText = data.status;

    const meetRoundEl = document.getElementById('meetRound');
    if (meetRoundEl) {
        meetRoundEl.innerText = data.round_name || "Technical";
    }

    const meetLinkEl = document.getElementById('meetLink');
    if (meetLinkEl) {
        const details = data.meeting_details || "";
        if (details.startsWith('http') || details.startsWith('www.')) {
            const url = details.startsWith('http') ? details : 'https://' + details;
            meetLinkEl.innerHTML = `<a href="${url}" target="_blank" style="color: #007bff; font-weight: bold; text-decoration: underline;">Join Interview Link</a>`;
        } else {
            meetLinkEl.innerText = details || "N/A";
        }
    }

    // Roadmap logic
    const roadmap = document.getElementById('roadmapSteps');
    roadmap.innerHTML = data.rounds.map((round, idx) => {
        let statusClass = "";
        if (idx + 1 < data.currentRound) statusClass = "completed";
        if (idx + 1 === data.currentRound) statusClass = "current";
        return `
            <div class="step ${statusClass}">
                <div class="step-circle">${idx + 1}</div>
                <div class="step-label">${round}</div>
            </div>
        `;
    }).join('');

    // Preparation Checklist logic
    const prepList = document.getElementById('prepList');
    prepList.innerHTML = data.prep.map(item => `<li>✅ ${item}</li>`).join('');
}

init();