console.log("Login script loaded.");

const loginText = document.querySelector(".title-text .login");
const loginFormStyle = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
signupBtn.onclick = (() => {
  loginFormStyle.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
});
loginBtn.onclick = (() => {
  loginFormStyle.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
});
signupLink.onclick = (() => {
  signupBtn.click();
  return false;
});

const loginForm = document.querySelector("#login-form");
const loginUsername = document.querySelector("#login-username");
const loginPassword = document.querySelector("#login-password");

loginForm.addEventListener("submit", function (event) {
  event.preventDefault();
  const username = loginUsername.value;
  const password = loginPassword.value;

  const credentials = {
    username: username,
    password: password
  };

  // Send credentials to the server for authentication
  fetch("http://localhost:3000/signin", {
    method: "POST",
    body: JSON.stringify(credentials),
    headers: {
      "Content-Type": "application/json"
    },
    mode: 'cors' // Enable CORS
  }).then(response => response.json())
    .then(data => {
      if (data.access_token) {
        // If the login is successful, store the token in localStorage
        localStorage.setItem("token", data.access_token);
        // Navigate to index.html or another protected page
        window.location.href = "index.html";
      } else {
        // If the login is unsuccessful, show an error message
        alert("Login failed. Please check your username and password.");
      }
    })
    .catch(error => {
      console.error("An error occurred:", error);
    });
});
const signupForm = document.querySelector("#signup-form");
const signupUsername = document.querySelector("#signup-username");
const signupPassword = document.querySelector("#signup-password");
const signupConfirmPassword = document.querySelector("#signup-confirm-password");

signupForm.addEventListener("submit", function (event) {
  event.preventDefault();
  const username = signupUsername.value;
  const password = signupPassword.value;
  const confirmPassword = signupConfirmPassword.value;

  // Check if password and confirm password match
  if (password !== confirmPassword) {
    alert("Passwords do not match. Please check again.");
    return; // Prevent submitting the form
  }

  const userData = {
    username: username,
    password: password
  };

  // Send signup data to the server
  fetch("http://localhost:3000/signup", {
    method: "POST",
    body: JSON.stringify(userData),
    headers: {
      "Content-Type": "application/json"
    },
    mode: 'cors' // Enable CORS
  }).then(response => response.json())
    .then(data => {
      // Handle the response
      if (data.message === "User registered successfully.") {
        alert("Signup successful! You can now log in.");
      } else {
        alert("Signup failed. Please try again later.");
      }
    })
    .catch(error => {
      console.error("An error occurred:", error);
    });
});
