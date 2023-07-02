var checkbox = document.getElementById("dn");
checkbox.addEventListener("change", toggleDarkMode);
//function to change the theme when the checkbox changes
function toggleDarkMode() {
    var checkbox = document.getElementById("dn");
    var form = document.getElementById("form")
    var body = document.body;
  
    if (checkbox.checked) {
      form.style.background= "#F8FBFE";
      body.style.backgroundColor = "#707070"; // Set background color to black
    } else {
      body.style.backgroundColor = "#efefef"; // Set background color to white
    }
  }