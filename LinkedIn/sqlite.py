from flask import g, current_app
import sqlite3


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('user_authenticate.db')
        create_table(db)
    return db


def create_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password text NOT NULL,
            type text NOT NULL
        )
''')
    db.commit()

def close_db(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def authenticate(username):
    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT id, username, password, email, type FROM users WHERE username = ?', (username,))
    user = cur.fetchone()

    if user:
        return user


def getUserById(id):
    db = get_db()
    cur = db.cursor()

    cur.execute(f'SELECT id, username, password, email, type from users where id = {id}')
    db.commit()
    data = cur.fetchall()
    return data


def insertDataIntoUsers(username, email, password, pro_type):
    db = get_db()
    cur = db.cursor()

    cur.execute(f'''INSERT INTO users (username, email, password, type)
VALUES ('{username}','{email}','{password}','{pro_type}');
''')
    db.commit()

def getUsername():
    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT username from users')
    db.commit()
    data = [row[0] for row in cur.fetchall()]
    return data


