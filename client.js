function validatePassword() {
  var password = document.getElementById("signup_password").value;
  var passwordConfirmation = document.getElementById("signup_passwordConfirmation");
  
  if(password != passwordConfirmation.value) {
    passwordConfirmation.setCustomValidity("Passwords do not Match");
  } else {
    passwordConfirmation.setCustomValidity("");
  }
}

function signUpHandler(inputObject) {
  var signup = serverstub.signUp(inputObject);
  console.log(signup);
  if (!signup.success) {
    var submitButton = document.querySelector("#signup .submitButton");
    submitButton.setCustomValidity(signup.message)
    submitButton.reportValidity();
  }
  else {
    var login = serverstub.signIn(inputObject.email, inputObject.password);
    localStorage.setItem("token", login.data);
    synchronizeView();
  }
}

function signInHandler(inputObject) {
  var response = serverstub.signIn(inputObject.email, inputObject.password);
  
  if (!response.success) {
    var submitButton = document.querySelector("#login .submitButton");
    submitButton.setCustomValidity(response.message);
    submitButton.reportValidity();
  } else {
    localStorage.setItem("token", response.data);
    synchronizeView();
  }
}

  function refreshView(viewId, content) {
    const container = document.getElementById(viewId);
    container.innerHTML = content;
  }

  function getActiveTab() {
    const headerContainer = document.getElementById('headerContainer');
    const selectedTab = headerContainer.querySelector("input[type='radio']:checked");
    const activeTab = selectedTab ? selectedTab.value : "homeView";
    console.log(activeTab);
    return activeTab;
  }

  function synchronizeView() {
    const token = localStorage.getItem("token");
    const isLoggedIn = token && serverstub.getUserDataByToken(token).success;

    if (isLoggedIn) {
      if (document.getElementById("headerContainer").innerHTML === "") {
        const content = document.getElementById('headerView').innerHTML;
        refreshView('headerContainer', content);
      }
    } else {
      document.getElementById("headerContainer").innerHTML = "";
    }

    const viewId = isLoggedIn ? getActiveTab() : 'welcomeView';
    const content = document.getElementById(viewId).innerHTML;
    refreshView('viewContainer', content);
  };