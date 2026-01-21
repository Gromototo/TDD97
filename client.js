function validatePassword() {
  var password = document.getElementById("signup_password").value;
  var passwordConfirmation = document.getElementById("signup_passwordConfirmation");
  
  if(password != passwordConfirmation.value) {
    passwordConfirmation.setCustomValidity("Passwords do not Match");
  } else {
    passwordConfirmation.setCustomValidity("");
  }
}