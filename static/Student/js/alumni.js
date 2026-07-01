// Use backend alumni if available, fallback to mock list
const alumniData = window.backendAlumni || [
    { name: "Saurabh Bhosale", year: "2023", company: "Microsoft", role: "Software Engineer", initials: "SB", linkedin: "https://linkedin.com", testimonial: "Highly motivated and driven." },
    { name: "Tanmay Dahivalikar", year: "2022", company: "Google", role: "System Engineer", initials: "TD", linkedin: "https://linkedin.com", testimonial: "Continuous learning is key." }
];


function displayAlumni(data) {
    const grid = document.getElementById('alumniGrid');
    if (!grid) return;
    
    grid.innerHTML = data.map(person => {
        let avatarHTML = `<div class="avatar-circle">${person.initials || 'AL'}</div>`;
        if (person.image) {
            avatarHTML = `<img src="${person.image}" class="avatar-circle" style="object-fit: cover; display: block;">`;
        }
        
        let linkedinHTML = '';
        if (person.linkedin) {
            linkedinHTML = `
                <button class="contact-btn" style="background: #0077b5; margin-top: 10px;" onclick="window.open('${person.linkedin}', '_blank')">
                    Connect on LinkedIn
                </button>
            `;
        }

        return `
            <div class="alumni-card">
                ${avatarHTML}
                <h3>${person.name}</h3>
                <span class="company-tag">${person.role || 'Alumnus'} at ${person.company}</span>
                <p class="info-row">🎓 Batch of ${person.year}</p>
                <p class="info-row text-testimonial" style="font-style: italic; color: #555; margin-top: 10px; min-height: 40px; font-size: 0.85rem;">
                    "${person.testimonial || 'No testimonial shared yet.'}"
                </p>
                ${linkedinHTML}
            </div>
        `;
    }).join('');
}

function filterAlumni() {
    const term = document.getElementById('alumniSearch').value.toLowerCase();
    const filtered = alumniData.filter(person => 
        person.name.toLowerCase().includes(term) || 
        person.company.toLowerCase().includes(term) ||
        (person.role && person.role.toLowerCase().includes(term))
    );
    displayAlumni(filtered);
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    displayAlumni(alumniData);
});