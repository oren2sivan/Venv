import sqlite3 as sql



def connect_db():
    conn=sql.connect('userdb.db')
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT)""")
    return conn,cursor


def add_user(username,password):

    conn,cursor=connect_db()
    cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
    conn.commit()
    conn.close()


def find_user(username,password):
    conn,cursor=connect_db()
    user=cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    if user!=None:
        return True
    else:
        return False
    
