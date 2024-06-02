import Connections
import sqlite3
conn = sqlite3.connect(Connections.connection[1])
print ("Opened database successfully")
conn.execute('''CREATE TABLE THINGS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         One TEXT NOT NULL,
         Two TEXT NOT NULL);''')
conn.commit()
print ("Records created successfully")
conn.close()
