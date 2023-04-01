document.addEventListener("DOMContentLoaded", function() {

  const navbarMenu = document.querySelector(".navbar-menu");
    const navbarToggle = document.querySelector(".navbar-toggle");

    navbarToggle.addEventListener("click", function() {
    navbarToggle.classList.toggle("active");
    navbarMenu.classList.toggle("show");
    });


  localStorage.removeItem("loggedUser");
  localStorage.removeItem("isStudent");
  var loginButton = document.getElementById("login");
  loginButton.addEventListener("click", function() {
    var emailField = document.getElementsByName("userId")[0];
    var passwordField = document.getElementsByName("password")[0];
    var p = document.getElementById("access")
    var loggedUser = emailField.value;
    var password = passwordField.value;
    var access = "";
    $.ajax({
      url: "/informer/",
      data: {"loggedUser": loggedUser, "password": password, "calledFor": "login"},
      dataType: "json",
      success: function(response) {
        if (!response.error) {
          access = response.access;
          if (access == "Granted") {
            localStorage.setItem('loggedUser', loggedUser);
            localStorage.setItem('isStudent', response.isStudent);
            window.location = '/timeline';
          } else {
            p.innerText = "Log In failed. Please try again...";
          }
        } else {
            p.innerText = response.error;
        }
      },
      error: function(xhr, status, error) {
          console.log(xhr.responseText);
      }
    });
});
});
