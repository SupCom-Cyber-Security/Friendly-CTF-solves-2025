from flask import Flask, request, session, redirect, url_for, render_template
import sqlite3, bcrypt, os, secrets, string

ID_NUM = "5423-6865-7421-9853"
PREFIX = "uixx-twix-sezd111-azer123-78789id-5656"



TAIL_LENGTH = 100
TAIL = ''.join(secrets.choice(string.digits) for _ in range(TAIL_LENGTH))

ADMIN_PASSWORD = "admin-password" + PREFIX + ID_NUM + TAIL


DB_FILE = 'challenge.db'
FLAG = 'SC2{fl45k_sql1t3_bcrypt_4dm1n}' 

def init_db():


    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash BLOB)''')

    c.execute('DELETE FROM users WHERE username = ?', ('admin',))
    admin_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt())
    c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('admin', admin_hash))
    conn.commit()
    conn.close()


def get_user_hash(username):
    if not os.path.exists(DB_FILE):
        return None
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

app = Flask(__name__, template_folder=os.path.join(os.getcwd(),'templates'), static_folder=os.path.join(os.getcwd(),'static'))
app.secret_key = os.urandom(16)

@app.route('/', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        if username == 'admin':
            stored = get_user_hash('admin')
            if stored is None:
                msg = 'Invalid credentials.'
            else:
                if bcrypt.checkpw(password.encode('utf-8'), stored):
                    session['user'] = 'admin'
                    return redirect(url_for('flag'))
                else:
                    msg = 'Invalid credentials.'
        else:
            msg = 'Invalid credentials.'
    return render_template('login.html', msg=msg)

@app.route('/flag')
def flag():
    if session.get('user') == 'admin':
        return render_template('flag.html', flag=FLAG)
    return redirect(url_for('login'))

if __name__ == '__main__':
   
    init_db()
    app.run(host='0.0.0.0', port=20001, debug=False)
