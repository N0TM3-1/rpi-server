import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)''')

def add_user(user_id):
    try:
        cur.execute('INSERT INTO users(id) VALUES (?)', (user_id,))
        conn.commit()
    except sqlite3.Error as e:
        return(f"Database error: {e}")
    else:
        return("Opt-in successful")

def exists(user_id):
    cur.execute('SELECT * FROM users WHERE id=(?)', (user_id,))
    if cur.fetchone():
        return True
    else:
        return False