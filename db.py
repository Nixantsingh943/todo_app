# db.py
import sqlite3

DB_NAME = "todos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    completed INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def add_task(title, description, due_date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO todos (title, description, due_date) VALUES (?, ?, ?)",
              (title, description, due_date))
    conn.commit()
    conn.close()

def get_tasks(filter_by="all"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if filter_by == "active":
        c.execute("SELECT * FROM todos WHERE completed=0")
    elif filter_by == "completed":
        c.execute("SELECT * FROM todos WHERE completed=1")
    else:
        c.execute("SELECT * FROM todos")
    rows = c.fetchall()
    conn.close()
    return rows

def update_task(task_id, title, description, due_date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE todos SET title=?, description=?, due_date=? WHERE id=?",
              (title, description, due_date, task_id))
    conn.commit()
    conn.close()

def toggle_task(task_id, completed):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE todos SET completed=? WHERE id=?", (completed, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

