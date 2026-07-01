// Load the shared navbar dynamically on each page
document.addEventListener("DOMContentLoaded", function () {
  const navbarContainer = document.getElementById("navbar-container");

  if (navbarContainer) {
    fetch("components/navbar.html")
      .then((response) => response.text())
      .then((data) => {
        navbarContainer.innerHTML = data;
      })
      .catch((error) => console.error("Error loading navbar:", error));
  }
});


// main.js
document.addEventListener("DOMContentLoaded", () => {
  fetch("components/navbar.html")
    .then(res => res.text())
    .then(data => {
      document.getElementById("navbar").innerHTML = data;
    })
    .catch(err => console.error("Navbar load error:", err));
});


