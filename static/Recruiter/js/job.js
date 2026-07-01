document.addEventListener("DOMContentLoaded", function() {
  const jobForm = document.getElementById("jobForm");
  const jobTableBody = document.querySelector("#jobTable tbody");

  let jobs = JSON.parse(localStorage.getItem("jobs")) || [];

  // Function to render all jobs
  function renderJobs() {
    jobTableBody.innerHTML = "";
    jobs.forEach((job, index) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${job.title}</td>
        <td>${job.location}</td>
        <td>₹${job.salary}</td>
        <td>${job.skills}</td>
        <td>${job.status}</td>
        <td>
          <button class="action-btn edit-btn" data-index="${index}">Edit</button>
          <button class="action-btn delete-btn" data-index="${index}">Delete</button>
        </td>
      `;
      jobTableBody.appendChild(row);
    });
  }

  // Initial render
  renderJobs();

  // Handle form submission
  jobForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const newJob = {
      title: document.getElementById("title").value,
      location: document.getElementById("location").value,
      salary: document.getElementById("salary").value,
      skills: document.getElementById("skills").value,
      eligibility: document.getElementById("eligibility").value,
      status: "Active"
    };

    jobs.push(newJob);
    localStorage.setItem("jobs", JSON.stringify(jobs));
    renderJobs();
    jobForm.reset();
  });

  // Edit and Delete events
  jobTableBody.addEventListener("click", function(e) {
    if (e.target.classList.contains("delete-btn")) {
      const index = e.target.dataset.index;
      jobs.splice(index, 1);
      localStorage.setItem("jobs", JSON.stringify(jobs));
      renderJobs();
    }

    if (e.target.classList.contains("edit-btn")) {
      const index = e.target.dataset.index;
      const job = jobs[index];
      document.getElementById("title").value = job.title;
      document.getElementById("location").value = job.location;
      document.getElementById("salary").value = job.salary;
      document.getElementById("skills").value = job.skills;
      document.getElementById("eligibility").value = job.eligibility;

      jobs.splice(index, 1); // remove to re-add updated
      localStorage.setItem("jobs", JSON.stringify(jobs));
      renderJobs();
    }
  });
});
