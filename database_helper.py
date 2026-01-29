import sqlite3

DATABASENAME = "database.db"

def getPasswordByEmail(email):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT password FROM user WHERE username = ?", (email,))
        return cursor.fetchone()
               
def getUser(email=None, token=None):

    #Either selects the email or the tokens. If none is defined ze don't query the DB.
    fieldName =  'username' if email else 'token' if token else None
    field = email if email else token
    if not fieldName :
        return Exception("One parameter should be defined")
    
    print(fieldName, field)
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("SELECT username FROM user WHERE username = ?", (field,))

        return cursor.fetchone()
    
def createUser(email, password, firstName, lastName, gender, city, country):
    with sqlite3.connect(DATABASENAME) as users:
        users.row_factory = sqlite3.Row
        cursor = users.cursor()
        cursor.execute("INSERT INTO user \
        (username,password,firstname,lastname,gender,city,country) VALUES (?,?,?,?,?,?,?)", (email, password, firstName, lastName, gender, city, country))
        users.commit()        

               
