document.addEventListener("DOMContentLoaded", () => {
  const applicantCards = document.getElementById("applicantCards");
  const shortlistedCards = document.getElementById("shortlistedCards");

  const filterName = document.getElementById("filterName");
  const filterSkill = document.getElementById("filterSkill");
  const filterStatus = document.getElementById("filterStatus");
  const applyFilter = document.getElementById("applyFilter");

  let applicants = window.backendApplicants || [
    { id: 1, name: "Riya Sharma", college: "PCCOE Pune", skills: "React, Node.js", cgpa: 8.9, status: "Under Review", score: 78 },
    { id: 2, name: "Amit Patil", college: "MIT WPU", skills: "Java, Spring", cgpa: 9.1, status: "Shortlisted", score: 88 },
    { id: 3, name: "Sneha Deshmukh", college: "COEP", skills: "Python, ML", cgpa: 9.3, status: "Interviewed", score: 92 },
    { id: 4, name: "Aditya Kulkarni", college: "VIT Pune", skills: "C++, SQL", cgpa: 8.5, status: "Under Review", score: 75 },
  ];

  // Render function
  function renderApplicants(list) {
    applicantCards.innerHTML = "";
    shortlistedCards.innerHTML = "";

    list.forEach((a, index) => {
      const card = document.createElement("div");
      card.classList.add("applicant-card");

      card.innerHTML = `
        <div class="applicant-header">
          <h4>${a.name} | ${a.job_title || 'Applied Candidate'}</h4>
          <span class="status-label status-${a.status.replace(" ", "")}">${a.status}</span>
        </div>
        <p><strong>College:</strong> ${a.college}</p>
        <p><strong>Skills:</strong> ${a.skills}</p>
        <p><strong>CGPA:</strong> ${a.cgpa}</p>
        <p class="score">ATS Resume Score: ${a.score}%</p>
        <div class="action-buttons">
          <button class="shortlist-btn" data-index="${index}">Shortlist</button>
          <button class="interview-btn" data-index="${index}">Interview</button>
          <button class="hire-btn" data-index="${index}">Hire</button>
          <button class="reject-btn" data-index="${index}">Reject</button>
        </div>
      `;

      applicantCards.appendChild(card);

      if (a.status === "Shortlisted") {
        const shortCard = card.cloneNode(true);
        shortlistedCards.appendChild(shortCard);
      }
    });
  }

  renderApplicants(applicants);

  // Filter logic
  applyFilter.addEventListener("click", () => {
    const name = filterName.value.toLowerCase();
    const skill = filterSkill.value.toLowerCase();
    const status = filterStatus.value;

    const filtered = applicants.filter(a =>
      a.name.toLowerCase().includes(name) &&
      a.skills.toLowerCase().includes(skill) &&
      (status === "" || a.status === status)
    );

    renderApplicants(filtered);
  });

  // Update status
  applicantCards.addEventListener("click", (e) => {
    if (e.target.tagName === "BUTTON") {
      const index = e.target.dataset.index;
      const btnClass = e.target.classList[0];
      const applicant = applicants[index];

      let newStatus = applicant.status;
      if (btnClass === "shortlist-btn") newStatus = "Shortlisted";
      if (btnClass === "interview-btn") newStatus = "Interviewed";
      if (btnClass === "hire-btn") newStatus = "Hired";
      if (btnClass === "reject-btn") newStatus = "Rejected";

      fetch('/api/applicants/update-status/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': typeof getCookie === 'function' ? getCookie('csrftoken') : ''
          },
          body: JSON.stringify({ applicant_id: applicant.id, status: newStatus })
      })
      .then(res => res.json())
      .then(data => {
          if (data.success) {
              applicant.status = newStatus;
              renderApplicants(applicants);
          } else {
              alert("Failed to update status: " + data.error);
          }
      })
      .catch(err => {
          console.error("Error updating status:", err);
          alert("An error occurred.");
      });
    }
  });
});
