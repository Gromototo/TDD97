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

               
