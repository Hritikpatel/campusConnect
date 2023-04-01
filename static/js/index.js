
document.addEventListener('DOMContentLoaded', function() {
    // Your JavaScript code here
    const navbarMenu = document.querySelector(".navbar-menu");
    const navbarToggle = document.querySelector(".navbar-toggle");

    navbarToggle.addEventListener("click", function() {
    navbarToggle.classList.toggle("active");
    navbarMenu.classList.toggle("show");
    });
    console.log("Working");
  });
  