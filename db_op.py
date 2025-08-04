import sqlite3

# Initialize the database table
def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

# Initialize database when module is imported
init_db()

def add_chat(chat):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO chats(id) VALUES(?)', (chat,))
        conn.commit()
    except sqlite3.Error:
        return 'Database error', 500
    finally:
        conn.close()
    return 'Chat added successfully', 200

def chat_exists(chat):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM chats WHERE id=(?)', (chat,))
        result = cur.fetchone()
        return result is not None
    finally:
        conn.close()