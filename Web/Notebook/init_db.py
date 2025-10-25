import sqlite3
import os

def init_database():
    if os.path.exists('database.sqlite'):
        os.remove('database.sqlite')
    
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    
    c.execute('''CREATE TABLE notes
                 (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, content TEXT)''')
    
    users = [
        (1, 'watari', 'password123', 'assistant'),
        (2, 'misa', 'light4ever', 'suspect'),
        (3, 'soichiro', 'justice123', 'investigator'),
        (4, 'matsuda', 'clumsy123', 'investigator'),
        (5, 'aizawa', 'serious123', 'investigator'),
        (0, 'L', 'shinigami', 'lead_investigator')
    ]
    
    c.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
    
    notes = [
        (0, 0, 'L: Final Conclusion - FLAG', 'After thorough investigation, I have determined that Light Yagami is Kira. The evidence is conclusive. FLAG: SC2{L_0f_L4w11}'),
        (1, 1, 'Watari: Surveillance Setup', 'Cameras installed in Yagami residence. Awaiting L\'s further instructions.'),
        (2, 2, 'Misa: Meeting Notes', 'Had coffee with Light-kun today! He seems so smart and handsome.'),
        (3, 3, 'Soichiro: Family Observations', 'Light has been acting strangely. Staying up late frequently.'),
        (4, 4, 'Matsuda: Suspicious Activity', 'Saw a student buying notebooks in bulk. Could be related?'),
        (5, 5, 'Aizawa: Pattern Analysis', 'Kira attacks follow school schedules. Student involvement likely.'),
        (6, 1, 'Watari: Technical Report', 'New hacking tools acquired. Ready for cyber investigation.'),
        (7, 2, 'Misa: Fan Club Activities', 'Organizing a fan event. Light-kun promised to attend!'),
        (8, 3, 'Soichiro: Police Coordination', 'Interpol notified. International cooperation established.'),
        (9, 4, 'Matsuda: Witness Interview', 'Interviewed convenience store clerk. No useful information.'),
        (10, 5, 'Aizawa: Profile Update', 'Kira shows strong sense of justice. Possibly law student.')
    ]
    
    c.executemany('INSERT INTO notes VALUES (?, ?, ?, ?)', notes)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()