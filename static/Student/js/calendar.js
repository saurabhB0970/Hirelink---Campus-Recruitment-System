// Use backend events if available, fallback to mock list
const events = window.backendEvents || [
    { date: '2026-02-28', company: 'SAP Labs', type: 'Technical Interview', time: '11:00 AM' },
    { date: '2026-02-15', company: 'Google', type: 'Coding Test', time: '04:00 PM' }
];

let currentDate = new Date(); // default to today
// If there are events, let's default to the date of the first event so that the user sees it immediately
if (events.length > 0) {
    const firstEventDate = new Date(events[0].date);
    if (!isNaN(firstEventDate.getTime())) {
        currentDate = firstEventDate;
    }
}

const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

function generateCalendar() {
    const daysContainer = document.getElementById('calendarDays');
    daysContainer.innerHTML = ''; // clear first

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    // Set month display header
    document.getElementById('monthDisplay').innerText = `${monthNames[month]} ${year}`;

    // Get first day of the month
    const firstDayIndex = new Date(year, month, 1).getDay();

    // Get number of days in the month
    const totalDays = new Date(year, month + 1, 0).getDate();

    // Create empty cells for padding before the 1st of the month
    for (let x = 0; x < firstDayIndex; x++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'date-cell empty';
        daysContainer.appendChild(emptyCell);
    }

    // Populate actual days
    for (let i = 1; i <= totalDays; i++) {
        const monthStr = String(month + 1).padStart(2, '0');
        const dayStr = String(i).padStart(2, '0');
        const dateStr = `${year}-${monthStr}-${dayStr}`;

        const dayCell = document.createElement('div');
        dayCell.className = 'date-cell';
        dayCell.setAttribute('data-date', dateStr);

        let eventHTML = '';
        const dayEvent = events.find(e => e.date === dateStr);
        if (dayEvent) {
            eventHTML = `<div class="cal-event-tag">${dayEvent.company}</div>`;
        }

        dayCell.innerHTML = `
            <div class="date-num">${i}</div>
            ${eventHTML}
        `;
        daysContainer.appendChild(dayCell);
    }

    renderSidebar();
}

function renderSidebar() {
    const sidebar = document.getElementById('eventList');
    // Filter events to only show upcoming events or all events for the current month
    const currentMonthStr = String(currentDate.getMonth() + 1).padStart(2, '0');
    const currentYearStr = String(currentDate.getFullYear());
    const monthEvents = events.filter(e => {
        const parts = e.date.split('-');
        return parts[0] === currentYearStr && parts[1] === currentMonthStr;
    });

    if (monthEvents.length === 0) {
        sidebar.innerHTML = '<p style="text-align: center; color: #999; padding: 20px; font-size: 0.9rem;">No interviews scheduled for this month.</p>';
        return;
    }

    sidebar.innerHTML = monthEvents.map(e => `
        <div class="event-item" style="cursor: pointer;" onclick="alert('Company: ${e.company}\\nRound: ${e.type}\\nTime: ${e.time}')">
            <h4>${e.company} - ${e.type}</h4>
            <p>📅 ${e.date} | ⏰ ${e.time}</p>
        </div>
    `).join('');
}

function initNav() {
    const prevBtn = document.querySelectorAll('.cal-nav-btns .nav-btn')[0];
    const nextBtn = document.querySelectorAll('.cal-nav-btns .nav-btn')[1];

    if (prevBtn) {
        prevBtn.onclick = () => {
            currentDate.setMonth(currentDate.getMonth() - 1);
            generateCalendar();
        };
    }
    if (nextBtn) {
        nextBtn.onclick = () => {
            currentDate.setMonth(currentDate.getMonth() + 1);
            generateCalendar();
        };
    }
}

window.onload = () => {
    generateCalendar();
    initNav();
};