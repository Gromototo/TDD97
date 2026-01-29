from flask import Flask, request
import uuid
import sqlite3
import json
import validators

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as connect:
        connect.execute(
            '''
            CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
            firstname TEXT,
            lastname TEXT,
            gender TEXT,
            city TEXT,
            country TEXT,
            messages TEXT,
            token TEXT
        );''')
        connect.commit()

init_db()



@app.route('/sign_in', methods=['POST'])
def signIn():
    data = request.get_json()
    email = data.get('username')
    password = data.get('password')

    with sqlite3.connect("database.db") as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT password FROM user WHERE username = ?", (email,))
        user_data = cursor.fetchone()

        if user_data and user_data['password'] == password:
            token = str(uuid.uuid4())
            cursor.execute("UPDATE user SET token = ? WHERE username = ?", (token, email))
            users.commit()
            return {"success": True, "message": "Successfully signed in.", "data": token}

    return {"success": False, "message": "Wrong username or password."}



def assertSingUpData(email, password, firstName, lastName, gender, city, country):

    if not (email and password and firstName and lastName and gender and city and country) :
        return False

    if not validators.email(email) :
        return False

    #Given the tests.py we are apparently not expecte"d to send the second password (confirmation) in the payload. 
    #Therefore we cannot expect it to check that passwords == passwordConfirmation

    return True
    
@app.route('/sign_up', methods=['POST'])
def signUp():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    firstName = data.get('firstname')
    lastName = data.get('familyname')
    gender = data.get('gender')
    city = data.get('city')
    country = data.get('country')
    
    if not assertSingUpData(email, password, firstName, lastName, gender, city, country): 
        return {"success": False, "message": "Form data missing or incorrect type."}

    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE username = ?", (email,))
        if cursor.fetchone():
            return {"success": False, "message": "User already exists."}

        cursor.execute("INSERT INTO user \
        (username,password,firstname,lastname,gender,city,country) VALUES (?,?,?,?,?,?,?)", (email, password, firstName, lastName, gender, city, country))
        users.commit()

    return {"success": True, "message": "Successfully created a new user."}

@app.route('/sign_out', methods=['DELETE'])
def signOut():
    token = request.headers.get('Authorization')

    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE token = ?", (token,))
        if cursor.fetchone():
            cursor.execute("UPDATE user SET token = NULL WHERE token = ?", (token,))
            users.commit()
            return {"success": True, "message": "Successfully signed out."}

    return {"success": False, "message": "You are not signed in."}

@app.route('/change_password', methods=['PUT'])
def changePassword():
    token = request.headers.get('Authorization')
    data = request.get_json()
    oldPassword = data.get('oldpassword')
    newPassword = data.get('newpassword')
    if not (oldPassword and newPassword):
        return {"success": False, "message": "Invalid new password."}


    with sqlite3.connect("database.db") as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username, password FROM user WHERE token = ?", (token,))
        user = cursor.fetchone()

        if user:
            if user['password'] == oldPassword:
                cursor.execute("UPDATE user SET password = ? WHERE token = ?", (newPassword, token))
                users.commit()
                return {"success": True, "message": "Password changed."}
            else:
                return {"success": False, "message": "Wrong password."}

    return {"success": False, "message": "You are not logged in."}

@app.route('/get_user_data_by_token', methods=['GET'])
def getUserDataByToken():
    token = request.headers.get('Authorization')

    with sqlite3.connect("database.db") as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE token = ?", (token,))
        user = cursor.fetchone()
        if user:
            return getUserDataByEmail(user['username'], token)
    
    return {"success": False, "message": "You are not signed in."}

@app.route('/get_user_data_by_email/<email>', methods=['GET'])
def getUserDataByEmail(email, token=None):
    if not token:
        token = request.headers.get('Authorization')

    with sqlite3.connect("database.db") as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE token = ?", (token,))
        if cursor.fetchone():
            cursor.execute("SELECT username, firstname, lastname, gender, city, country FROM user WHERE username = ?", (email,))
            data = cursor.fetchone()
            if data:
                return {"success": True, "message": "User data retrieved.", "data": dict(data)}
            return {"success": False, "message": "No such user."}

    return {"success": False, "message": "You are not signed in."}

@app.route('/get_user_messages_by_token', methods=['GET'])
def getUserMessagesByToken():
    token = request.headers.get('Authorization')

    with sqlite3.connect("database.db") as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE token = ?", (token,))
        user = cursor.fetchone()
        if user:
            return getUserMessagesByEmail(user['username'], token)

    return {"success": False, "message": "You are not signed in."}

@app.route('/get_user_messages_by_email/<email>', methods=['GET'])
def getUserMessagesByEmail(email, token=None):
    if not token:
        token = request.headers.get('Authorization')

    with sqlite3.connect("database.db") as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE token = ?", (token,))
        if cursor.fetchone():
            cursor.execute("SELECT messages FROM user WHERE username = ?", (email,))
            data = cursor.fetchone()
            if data:
                messages = json.loads(data['messages']) if data['messages'] else []
                return {"success": True, "message": "User messages retrieved.", "data": messages}
            return {"success": False, "message": "No such user."}

    return {"success": False, "message": "You are not signed in."}

@app.route('/post_message', methods=['POST'])
def postMessage():
    token = request.headers.get('Authorization')
    data = request.get_json()
    email = data.get('email')
    message = data.get('message')
    if not (token and data and email and message):
        return {"success": False, "message": "Invalid payload"}


    with sqlite3.connect("database.db") as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        
        cursor.execute("SELECT username FROM user WHERE token = ?", (token,))
        sender = cursor.fetchone()
        
        if sender:
            from_email = sender['username']
            to_email = email if email else from_email
            
            cursor.execute("SELECT messages FROM user WHERE username = ?", (to_email,))
            recipient = cursor.fetchone()
            
            if recipient:
                current_messages = json.loads(recipient['messages']) if recipient['messages'] else []
                new_message = {"writer": from_email, "content": message}
                current_messages.insert(0, new_message)
                
                cursor.execute("UPDATE user SET messages = ? WHERE username = ?", (json.dumps(current_messages), to_email))
                users.commit()
                return {"success": True, "message": "Message posted"}
            else:
                return {"success": False, "message": "No such user."}

    return {"success": False, "message": "You are not signed in."}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
