from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes')
def view_notes():
    note_id = request.args.get('id', '1')
    
    try:
        note_id = int(note_id)
    except ValueError:
        return "Invalid note ID! Please enter a number.", 400
    
    conn = get_db_connection()
    note = conn.execute('SELECT n.*, u.username FROM notes n JOIN users u ON n.user_id = u.id WHERE n.id = ?', (note_id,)).fetchone()
    conn.close()
    
    if note:
        return render_template('notes.html', note=note)
    else:
        return f"Note #{note_id} not found! Try a different ID between 0-10.", 404

def init_database():
    from init_db import init_database as init_db
    init_db()

if __name__ == '__main__':
    if not os.path.exists('database.sqlite'):
        init_database()
    
    app.run(debug=False, host='0.0.0.0', port=20001)
