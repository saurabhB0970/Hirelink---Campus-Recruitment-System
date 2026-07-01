document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".type-btn");

    const studentFields = document.querySelector(".student-fields");
    const recruiterFields = document.querySelector(".recruiter-fields");
    const instituteFields = document.querySelector(".institute-fields");

    buttons.forEach(button => {
        button.addEventListener("click", () => {

            // Remove active button
            buttons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            // Hide all forms
            studentFields.classList.remove("active-fields");
            recruiterFields.classList.remove("active-fields");
            instituteFields.classList.remove("active-fields");

            // Show selected form
            const type = button.dataset.type;

            if (type === "student") {
                studentFields.classList.add("active-fields");
            }

            if (type === "recruiter") {
                recruiterFields.classList.add("active-fields");
            }

            if (type === "institute") {
                instituteFields.classList.add("active-fields");
            }
        });
    });
});