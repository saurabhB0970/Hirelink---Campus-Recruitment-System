(function() {
    emailjs.init("YOUR_PUBLIC_KEY"); // REPLACE THIS
})();

const addBtn = document.getElementById('addInterviewBtn');
const modal = document.getElementById('scheduleModal');
const closeModal = document.getElementById('closeModal');
const interviewForm = document.getElementById('interviewForm');
const interviewList = document.getElementById('interviewList');
const modeSelect = document.getElementById('interviewMode');
const venueInput = document.getElementById('venue');
const meetingBox = document.getElementById('meetingBox');
const meetingLinkInput = document.getElementById('meetingLink');

// 1. Load data from Backend on startup
document.addEventListener('DOMContentLoaded', () => {
    const saved = window.backendInterviews || [];
    saved.forEach(item => renderInterviewCard(item, false));
});

// 2. Toggle Online/Offline Fields
modeSelect.addEventListener('change', (e) => {
    if (e.target.value === 'offline') {
        venueInput.classList.remove('hidden');
        venueInput.required = true;
        meetingBox.classList.add('hidden');
    } else {
        venueInput.classList.add('hidden');
        venueInput.required = false;
        meetingBox.classList.remove('hidden');
    }
});

function generateLink() {
    return `https://meet.google.com/${Math.random().toString(36).substring(2,5)}-${Math.random().toString(36).substring(5,9)}-${Math.random().toString(36).substring(9,12)}`;
}

addBtn.addEventListener('click', () => {
    meetingLinkInput.value = generateLink();
    modal.classList.replace('hidden', 'flex');
});

const hideModal = () => {
    modal.classList.replace('flex', 'hidden');
    interviewForm.reset();
    venueInput.classList.add('hidden'); // default state
    meetingBox.classList.remove('hidden');
};

closeModal.addEventListener('click', hideModal);

// 3. Form Submission
interviewForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById('submitBtn');

    const data = {
        id: Date.now(),
        candidate_name: document.getElementById('candidateName').value,
        candidate_email: document.getElementById('candidateEmail').value,
        position: document.getElementById('position').value,
        date: document.getElementById('interviewDate').value,
        time: document.getElementById('interviewTime').value,
        mode: modeSelect.value,
        venue: modeSelect.value === 'offline' ? venueInput.value : "Online Video Call",
        meeting_url: modeSelect.value === 'online' ? meetingLinkInput.value : "N/A"
    };

    submitBtn.innerText = "Processing...";
    submitBtn.disabled = true;

    const formData = new FormData();
    formData.append('candidate_name', data.candidate_name);
    formData.append('candidate_email', data.candidate_email);
    formData.append('position', data.position);
    formData.append('date', data.date);
    formData.append('time', data.time);
    formData.append('mode', data.mode);
    formData.append('venue', data.venue);
    formData.append('meeting_url', data.meeting_url);
    formData.append('preparation_checklist', document.getElementById('preparationChecklist').value);

    fetch('/api/interviews/create/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': typeof getCookie === 'function' ? getCookie('csrftoken') : ''
        },
        body: formData
    })
    .then(res => res.json())
    .then(resData => {
        if (resData.success) {
            data.id = resData.id;
            // Attempt EmailJS send, catch error to not block success
            emailjs.send("YOUR_SERVICE_ID", "YOUR_TEMPLATE_ID", data)
                .catch(err => console.log("EmailJS failed, but interview scheduled:", err));
            
            renderInterviewCard(data, true);
            hideModal();
        } else {
            alert("Error scheduling interview: " + resData.error);
        }
    })
    .catch(err => {
        console.error("Error:", err);
        alert("An error occurred while saving the interview.");
    })
    .finally(() => {
        submitBtn.innerText = "Send Invite";
        submitBtn.disabled = false;
    });
});

function saveToStorage(item) {
    const list = JSON.parse(localStorage.getItem('hirelink_interviews')) || [];
    list.push(item);
    localStorage.setItem('hirelink_interviews', JSON.stringify(list));
}

// 4. Render Card UI
function renderInterviewCard(data, animate) {
    const card = document.createElement('div');
    card.setAttribute('data-id', data.id);
    card.className = `bg-white rounded-2xl p-6 shadow-xl border border-slate-100 transition hover:scale-[1.02] ${animate ? 'animate-fade-in' : ''}`;
    
    const isOffline = data.mode === 'offline';
    const badgeClass = isOffline ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700';

    card.innerHTML = `
        <div class="flex justify-between items-start mb-4">
            <h4 class="font-bold text-xl text-slate-800">${data.candidate_name}</h4>
            <span class="${badgeClass} text-[10px] font-black px-2 py-1 rounded-md uppercase tracking-wider">
                ${data.mode}
            </span>
        </div>
        <p class="text-blue-600 text-sm font-bold mb-3">${data.position}</p>
        
        <div class="bg-slate-50 p-3 rounded-lg text-xs space-y-2 mb-4">
            <div class="flex justify-between">
                <span class="text-slate-400">Location:</span>
                <span class="font-bold text-slate-700">${data.venue}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-slate-400">Schedule:</span>
                <span class="font-bold text-slate-700">${data.date} @ ${data.time}</span>
            </div>
        </div>

        <div class="flex flex-col gap-2">
            ${!isOffline ? 
                `<a href="${data.meeting_url}" target="_blank" class="text-center bg-blue-600 text-white py-2.5 rounded-xl text-xs font-bold">Join Meeting</a>` : 
                `<span class="text-center bg-slate-100 text-slate-500 py-2.5 rounded-xl text-xs font-bold">Offline Drive</span>`
            }
            <button onclick="deleteCard(${data.id})" class="text-[10px] font-bold text-red-400 uppercase tracking-widest hover:text-red-600 transition">Remove Record</button>
        </div>
    `;
    interviewList.prepend(card);
}

// Global Delete Function
window.deleteCard = (id) => {
    if(confirm("Delete this schedule?")) {
        fetch(`/api/interviews/delete/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': typeof getCookie === 'function' ? getCookie('csrftoken') : ''
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.querySelector(`[data-id="${id}"]`).remove();
            } else {
                alert("Failed to delete record: " + data.error);
            }
        })
        .catch(err => {
            console.error("Error:", err);
            alert("An error occurred while deleting the schedule.");
        });
    }
};