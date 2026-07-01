// Function to switch between sections
function showSection(event, sectionId) {
    // 1. Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(sec => sec.classList.remove('active'));

    // 2. Remove active class from all menu items
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => item.classList.remove('active'));

    // 3. Show the selected section
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.add('active');
    }

    // 4. Highlight the clicked menu item
    event.currentTarget.classList.add('active');
}

// Function to handle Profile Picture Upload
const imageInput = document.getElementById('imageInput');
const profileDisplay = document.getElementById('profileDisplay');
const plusIcon = document.getElementById('plusIcon');

if (imageInput) {
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profileDisplay.src = e.target.result;
                profileDisplay.style.display = 'block';
                plusIcon.style.display = 'none';
            }
            reader.readAsDataURL(file);
        }
    });
}