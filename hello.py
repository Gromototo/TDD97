from flask import Flask, request
import uuid
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/signin', methods=['GET'])
def signIn():
    email = request.args.get('email')
    password = request.args.get('password')

    #HERE WE NEED TO CHECK IF THE USER IS IN THE DATABASE

    #AND IF THE PASSWORD IS CORRECT.

        #return {"success": true, "message": "Successfully signed in.", "data": token};

    #IF one of the conditions is false we end up here, return {"success": false, "message": "Wrong username or password."};

    return {
        "token": str(uuid.uuid4()),
    }


@app.route('/signup', methods=['GET'])
def signUp():
    email = request.args.get('email')
    password = request.args.get('password')
    passwordConfirmaiton = request.args.get('passwordConfirmation')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    gender = request.args.get('gender')
    city = request.args.get('city')
    country = request.args.get('country')
    

    #We need to check that all fiels are present

        #if not return {"success": true, "message": "Form data missing or incorrect type."};

    #HERE WE NEED TO CHECK IF THE email alredy exists
        #If YES,  return {"success": false, "message": "User already exists."}
        
    #Try to create user in the databse if successful 
    #            return {"success": true, "message": "Successfully created a new user."};

    
    return {
        "token": str(uuid.uuid4()),
    }

@app.route('/signout', methods=['GET'])
def signOut():
    email = request.args.get('token')

    """    
      syncStorage();
      if (loggedInUsers[token] != null){
        delete loggedInUsers[token];
        persistLoggedInUsers();
        return {"success": true, "message": "Successfully signed out."};
      } else {
        return {"success": false, "message": "You are not signed in."};
      }
    """

@app.route('/changePassword', methods=['GET'])
def changePassword():
    email = request.args.get('email')
    oldPassword = request.args.get('oldPassword')
    newPassword = request.args.get('newPassword')   

    """
        syncStorage();
      if (loggedInUsers[token] != null){
        var email = tokenToEmail(token);
        if (users[email].password == oldPassword){
          users[email].password = newPassword;
          persistUsers();
          return {"success": true, "message": "Password changed."};
        } else {
          return {"success": false, "message": "Wrong password."};
        }
      } else {
        return {"success": false, "message": "You are not logged in."};
      }
    }"""

@app.route('/getUserDataByToken', methods=['GET'])
def getUserDataByToken():
    token = request.args.get('token')

    """
          var email = tokenToEmail(token);

          return serverstub.getUserDataByEmail(token, email);
    """

@app.route('/getUserDataByEmail', methods=['GET'])
def getUserDataByEmail():
    token = request.args.get('token')
    email = request.args.get('email')

    """
        syncStorage();
            if (loggedInUsers[token] != null){
                if (users[email] != null) {
                var match = copyUser(users[email]);
                delete match.messages;
                delete match.password;
                return {"success": true, "message": "User data retrieved.", "data": match};
                } else {
                return {"success": false, "message": "No such user."};
                }
            } else {
                return {"success": false, "message": "You are not signed in."};
            }
            },
    """

@app.route('/getUserMessagesByToken', methods=['GET'])
def getUserMessagesByToken():
    token = request.args.get('token')

    """
        syncStorage();
      var email = tokenToEmail(token);
      return serverstub.getUserMessagesByEmail(token,email);
    """

@app.route('/getUserMessagesByEmail', methods=['GET'])
def getUserMessagesByEmail():
    token = request.args.get('token')

    """
	syncStorage();
      if (loggedInUsers[token] != null){
        if (users[email] != null) {
          var match = copyUser(users[email]).messages;
          return {"success": true, "message": "User messages retrieved.", "data": match};
        } else {
          return {"success": false, "message": "No such user."};
        }
      } else {
        return {"success": false, "message": "You are not signed in."};
      }
    """

@app.route('/postMessage', methods=['GET'])
def postMessage():
    token = request.args.get('token')
    email = request.args.get('email')
    message = request.args.get('message')

    """
       syncStorage();
      var fromEmail = tokenToEmail(token);
      if (fromEmail != null) {
        if (toEmail == null) {
          toEmail = fromEmail;
        }
        if(users[toEmail] != null){
          var recipient = users[toEmail];
          var message = {"writer": fromEmail, "content": content};
          recipient.messages.unshift(message);
          persistUsers();
          return {"success": true, "message": "Message posted"};
        } else {
          return {"success": false, "message": "No such user."};
        }
      } else {
        return {"success": false, "message": "You are not signed in."};
      }
      """

if __name__ == '__main__':
    app.run(debug=True);