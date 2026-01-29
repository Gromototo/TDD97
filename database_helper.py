import sqlite3

DATABASENAME = "database.db"

def getPasswordByEmail(email):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT password FROM user WHERE username = ?", (email,))
        return cursor.fetchone()
               
def getUserByEmail(email):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE username = ?", (email,))
        return cursor.fetchone()

def getUserByToken(token):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE token = ?", (token,))
        return cursor.fetchone()
    
def createUser(email, password, firstName, lastName, gender, city, country):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("INSERT INTO user \
        (username,password,firstname,lastname,gender,city,country) VALUES (?,?,?,?,?,?,?)", (email, password, firstName, lastName, gender, city, country))
        users.commit()

def updateUserToken(email, token):
    with sqlite3.connect(DATABASENAME) as users:
        cursor = users.cursor()
        cursor.execute("UPDATE user SET token = ? WHERE username = ?", (token, email))
        users.commit()
        return cursor.rowcount > 0

def removeUserToken(token):
    with sqlite3.connect(DATABASENAME) as users:
        cursor = users.cursor()
        cursor.execute("UPDATE user SET token = NULL WHERE token = ?", (token,))
        users.commit()
        return cursor.rowcount > 0

def updatePassword(token, newPassword):
    with sqlite3.connect(DATABASENAME) as users:
        cursor = users.cursor()
        cursor.execute("UPDATE user SET password = ? WHERE token = ?", (newPassword, token))
        users.commit()
        return cursor.rowcount > 0

def getUserData(email):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username, firstname, lastname, gender, city, country FROM user WHERE username = ?", (email,))
        return cursor.fetchone()

def getUserMessages(email):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT messages FROM user WHERE username = ?", (email,))
        return cursor.fetchone()

def updateUserMessages(email, messages):
    with sqlite3.connect(DATABASENAME) as users:
        cursor = users.cursor()
        cursor.execute("UPDATE user SET messages = ? WHERE username = ?", (messages, email))
        users.commit()
        return cursor.rowcount > 0

               
