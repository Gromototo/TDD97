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

function changePasswordHandler(inputObject) {
  var response = serverstub.changePassword(inputObject.token, inputObject.password, inputObject.oldPassword);
  if (response.success) {
     document.querySelector("#changePasword form").reset();
  }

  var submitButton = document.querySelector("#changePasword .submitButton");
  submitButton.setCustomValidity(response.message);
  submitButton.reportValidity();
}

function signOutHandler(token) {
  var response = serverstub.signOut(token);
  if (response.success) {
    localStorage.removeItem("token");
  }
  synchronizeView();
}

function loadUserData() {
  const token = localStorage.getItem("token");
  const response = serverstub.getUserDataByToken(token);
  if (response.success) {
    const user = response.data;
    const infoContainer = document.getElementById("personalInfo");
    infoContainer.innerHTML = `
      <p>Name: ${user.firstname} ${user.familyname}</p>
      <p>Email: ${user.email}</p>
      <p>Gender: ${user.gender}</p>
      <p>City: ${user.city}</p>
      <p>Country: ${user.country}</p>
    `;
  }
}

function reloadWall() {
  const token = localStorage.getItem("token");
  const response = serverstub.getUserMessagesByToken(token);
  if (response.success) {
    const messages = response.data;
    const wallContainer = document.getElementById("wallMessages");
    wallContainer.innerHTML = messages.map(msg => `<div><strong>${msg.writer}:</strong> ${msg.content}</div>`).join("");
  }
}

function postMessageToWall() {
  const input = document.getElementById("messageInput");
  const content = input.value;
  if (content.trim() === "") return;

  const token = localStorage.getItem("token");
  if (serverstub.postMessage(token, content, null).success) {
    input.value = "";
    reloadWall();
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
  return activeTab;
}

function synchronizeView() {
  const token = localStorage.getItem("token");
  const isLoggedIn = token && serverstub.getUserDataByToken(token).success;

  if (isLoggedIn) {
    if (document.getElementById("headerContainer").innerHTML === "") {
      const content = document.getElementById('headerViewTemplate').innerHTML;
      refreshView('headerContainer', content);
    }

    if (!document.getElementById("loggedInView")) {
      const content = document.getElementById('loggedInViewTemplate').innerHTML;
      refreshView('viewContainer', content);
      loadUserData();
      reloadWall();
    }

    const activeTab = getActiveTab();
    const views = ["homeView", "browseView", "accountView"];
    views.forEach(function(view) {
        const el = document.getElementById(view);
        if (el) el.style.display = (view === activeTab) ? "block" : "none";
    });
  } else {
    document.getElementById("headerContainer").innerHTML = "";
    const content = document.getElementById('welcomeView').innerHTML;
    refreshView('viewContainer', content);
  }
}