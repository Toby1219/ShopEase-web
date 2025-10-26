// Simple JavaScript to toggle between the forms
document.addEventListener('DOMContentLoaded', function () {
    const loginContainer = document.getElementById('login-form-container');
    const registerContainer = document.getElementById('register-form-container');
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    const submit_reg =  document.getElementById("submit-reg");
    const submit_log =  document.getElementById("submit-log");

    const log_emailInput = document.getElementById("loginEmail");
    
    const reg_emailInput = document.getElementById("registerEmail");

    // Function to show the Registration form
    if (showRegisterLink) {
        showRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = showRegisterLink.href
        });
    }

    // Function to show the Login form
    if (showLoginLink) {
        showLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = showLoginLink.href
        });
    }

    
    if (submit_log){
        submit_log.addEventListener("click", () => {
            localStorage.setItem("email", log_emailInput.value);
        })
    }

    if (submit_reg){
        localStorage.setItem("email", reg_emailInput.value);
    }

});