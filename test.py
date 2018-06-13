import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

user = (1,'jose','asdf')
insert_query = "INSERT INTO users VALUES(?,?,?)"
cursor.execute(insert_query,user)

users = [
    (2,'rolf','asdf'),
    (3,'anne','xyz')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"



connection.commit()

connection.close()
