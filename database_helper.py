DATABASENAME = 'database.db'

def getUserByEmail(email):
  with sqlite3.connect(DATABASENAME) as users:
          cursor.execute("SELECT username FROM user WHERE username = ?", (email,))
          if cursor.fetchone():
               
def addNewUser() :
  cursor = users.cursor()
  with sqlite3.connect(DATABASENAME) as users:

          cursor.execute("INSERT INTO user \
    (username,password,firstname,lastname,gender,city,country) VALUES (?,?,?,?,?,?,?)", (email, password, firstName, lastName, gender, city, country))
    users.commit()