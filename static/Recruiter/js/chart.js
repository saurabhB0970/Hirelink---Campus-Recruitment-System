document.addEventListener('DOMContentLoaded', () => {
  // Applicants per role (used on index.html)
  const applicantEl = document.getElementById('applicantChart');
  if (applicantEl) {
    const ctx = applicantEl.getContext('2d');
    
    let labels = ['Software Engineer', 'Web Dev', 'Data Analyst', 'QA Tester'];
    let data = [45, 30, 25, 15];
    if (window.backendChartRoles && window.backendChartRoles.length > 0) {
      labels = window.backendChartRoles.map(r => r.title);
      data = window.backendChartRoles.map(r => r.count);
    }

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Applicants',
          data: data,
          backgroundColor: '#2563EB'
        }]
      },
      options: { responsive: true }
    });
  }

  // === Applications per Job Role (analytics page) ===
  const appsEl = document.getElementById('applicationsChart');
  if (appsEl) {
    const ctx1 = appsEl.getContext('2d');
    new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: ['Frontend Dev', 'Backend Dev', 'Data Analyst', 'HR Intern', 'QA Engineer'],
        datasets: [{
          label: 'Applications',
          data: [45, 60, 30, 25, 40],
          backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8'],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } },
        plugins: { legend: { display: false } }
      }
    });
  }

 
});
