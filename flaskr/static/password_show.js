function password_show_hide() {
  let x = document.getElementById("password");
  let showEye = document.getElementById("show_eye");
  let hideEye = document.getElementById("hide_eye");
  showEye.classList.remove("d-none");
  if (x.type === "password") {
    x.type = "text";
    showEye.style.display = "block";
    hideEye.style.display = "none";
  } else {
    x.type = "password";
    showEye.style.display = "none";
    hideEye.style.display = "block";
  }
}