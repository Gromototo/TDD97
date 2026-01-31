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

async function signUpHandler(inputObject) {
  const response = await fetch('/sign_up', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(inputObject)
  });
  const result = await response.json();

  if (!result.success) {
    var submitButton = document.querySelector("#signup .submitButton");
    submitButton.setCustomValidity(result.message)
    submitButton.reportValidity();
  }
  else {
    await signInHandler(inputObject);
  }
}

async function signInHandler(inputObject) {
  const response = await fetch('/sign_in', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: inputObject.email, password: inputObject.password })
  });
  const result = await response.json();
  
  if (!result.success) {
    var submitButton = document.querySelector("#login .submitButton");
    submitButton.setCustomValidity(result.message);
    submitButton.reportValidity();
  } else {
    localStorage.setItem("token", result.data);
    await synchronizeView();
  }
}

async function changePasswordHandler(inputObject) {
  const response = await fetch('/change_password', {
    method: 'PUT',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': inputObject.token 
    },
    body: JSON.stringify({ 
      oldpassword: inputObject.oldPassword, 
      newpassword: inputObject.newPassword 
    })
  });
  const result = await response.json();

  if (result.success) {
     document.querySelector("#changePasword form").reset();
  }

  var submitButton = document.querySelector("#changePasword .submitButton");
  submitButton.setCustomValidity(result.message);
  submitButton.reportValidity();
}

async function signOutHandler(token) {
  const response = await fetch('/sign_out', {
    method: 'DELETE',
    headers: { 'Authorization': token }
  });
  const result = await response.json();

  if (result.success) {
    localStorage.removeItem("token");
  }
  await synchronizeView();
}

async function loadUserData(token, email, containerId) {
  const loggedInToken = localStorage.getItem("token");
  let url = email ? `/get_user_data_by_email/${email}` : '/get_user_data_by_token';
  
  const response = await fetch(url, {
    headers: { 'Authorization': loggedInToken || token }
  });
  const result = await response.json();

  if (result.success) {
    const user = result.data;
    const infoContainer = document.getElementById(containerId);
    infoContainer.innerHTML = `
      <p>Name: ${user.firstname} ${user.lastname}</p>
      <p>Email: ${user.username}</p>
      <p>Gender: ${user.gender}</p>
      <p>City: ${user.city}</p>
      <p>Country: ${user.country}</p>
    `;
    return true;
  }
  return result.message;
}

async function reloadWall(token, email, containerId) {
  let url = email ? `/get_user_messages_by_email/${email}` : '/get_user_messages_by_token';
  
  const response = await fetch(url, {
    headers: { 'Authorization': token }
  });
  const result = await response.json();

  if (result.success) {
    const messages = result.data;
    const wallContainer = document.getElementById(containerId);
    wallContainer.innerHTML = messages.map((msg, index) => `
      <div id="msg_${index}" class="message-bubble">
        <div class="message-author">${msg.writer}</div>
        <div class="message-text">${msg.content}</div>
      </div>`
    ).join("");
  }
}

async function postMessageToWall(email = null) {
  const input = email ? document.getElementById("browseMessageInput") : document.getElementById("messageInput");
  const content = input.value;
  if (content.trim() === "") return;

  const token = localStorage.getItem("token");
  
  const response = await fetch('/post_message', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': token 
    },
    body: JSON.stringify({ email: email, message: content })
  });
  const result = await response.json();

  if (result.success) {
    input.value = "";
    const wallId = email ? "browseWallMessages" : "wallMessages";
    await reloadWall(token, email, wallId);
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

async function synchronizeView() {
  const token = localStorage.getItem("token");
  let isLoggedIn = false;

  if (token) {
    const response = await fetch('/get_user_data_by_token', { headers: { 'Authorization': token } });
    const result = await response.json();
    isLoggedIn = result.success;
  }

  if (isLoggedIn) {
    if (document.getElementById("headerContainer").innerHTML === "") {
      const content = document.getElementById('headerViewTemplate').innerHTML;
      refreshView('headerContainer', content);
    }

    if (!document.getElementById("loggedInView")) {
      const content = document.getElementById('loggedInViewTemplate').innerHTML;
      refreshView('viewContainer', content);
      await loadUserData(token, null, "personalInfo");
      await reloadWall(token, null, "wallMessages");
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

async function handleBrowseSearch() {
  const emailInput = document.getElementById("browseEmail");
  if (!emailInput.checkValidity()) {
    emailInput.reportValidity();
    return;
  }

  const email = emailInput.value;
  const resultContainer = document.getElementById("browseProfile");
  const searchButton = document.getElementById("browseSearchButton");

  const result = await loadUserData(null, email, "browsePersonalInfo");
  if (result === true) {
    currentBrowseEmail = email;
    resultContainer.style.display = "block";
    await reloadWall(localStorage.getItem("token"), email, "browseWallMessages");
    searchButton.setCustomValidity("");
  } else {
    resultContainer.style.display = "none";
    searchButton.setCustomValidity(result);
    searchButton.reportValidity();
  }
}