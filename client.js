currentBrowseEmail = null;

function validatePasswordMatch(passwordId, confirmationId) {
  var password = document.getElementById(passwordId).value;
  var passwordConfirmation = document.getElementById(confirmationId);
  
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
  var response = serverstub.changePassword(inputObject.token, inputObject.oldPassword, inputObject.newPassword);
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

function loadUserData(token, email, containerId) {
  const loggedInToken = localStorage.getItem("token");
  let response;
  if (email) {
    response = serverstub.getUserDataByEmail(loggedInToken, email);
  } else {
    response = serverstub.getUserDataByToken(token);
  }
  if (response.success) {
    const user = response.data;
    const infoContainer = document.getElementById(containerId);
    infoContainer.innerHTML = `
      <p>Name: ${user.firstname} ${user.familyname}</p>
      <p>Email: ${user.email}</p>
      <p>Gender: ${user.gender}</p>
      <p>City: ${user.city}</p>
      <p>Country: ${user.country}</p>
    `;
    return true;
  }
  return response.message;
}

function reloadWall(token, email, containerId) {
  const response = email ? serverstub.getUserMessagesByEmail(token, email) : serverstub.getUserMessagesByToken(token);
  if (response.success) {
    const messages = response.data;
    const wallContainer = document.getElementById(containerId);
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
    reloadWall(token, null, "wallMessages");
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
      loadUserData(token, null, "personalInfo");
      reloadWall(token, null, "wallMessages");
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

function handleBrowseSearch() {
  const emailInput = document.getElementById("browseEmail");
  if (!emailInput.checkValidity()) {
    emailInput.reportValidity();
    return;
  }

  const email = emailInput.value;
  const resultContainer = document.getElementById("browseProfile");
  const searchButton = document.getElementById("browseSearchButton");

  const result = loadUserData(null, email, "browsePersonalInfo");
  if (result === true) {
    currentBrowseEmail = email;
    resultContainer.style.display = "block";
    reloadWall(localStorage.getItem("token"), email, "browseWallMessages");
    searchButton.setCustomValidity("");
  } else {
    resultContainer.style.display = "none";
    searchButton.setCustomValidity(result);
    searchButton.reportValidity();
  }
}