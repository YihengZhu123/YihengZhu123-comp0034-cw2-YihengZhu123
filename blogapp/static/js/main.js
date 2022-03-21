function change_login_btn_status() {
  var x = document.getElementById("user_btn");
  if (x.innerHTML === "Log In") {
    x.innerHTML = "Log Out";
  } else {
    x.innerHTML = "Log In";
  }
}