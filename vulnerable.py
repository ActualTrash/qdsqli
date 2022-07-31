# ---------------------------------------------------------------- #
# Made with Love by Chase Hildebrand and Eric Miller on 7/28/2022  #
# ---------------------------------------------------------------- #

from flask import Flask, request, render_template, redirect
import sqlite3
import hashlib
import re

app = Flask(__name__)

DB_NAME = 'vulnerable.sqlite3'

# Setup the database
con = sqlite3.connect(DB_NAME)
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS users')
cur.execute('DROP TABLE IF EXISTS classes')
cur.execute('''
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    affiliation VARCHAR NOT NULL
);
''')

cur.execute('''
CREATE TABLE classes (
        id INT PRIMARY KEY,
        class_name VARCHAR NOT NULL,
        teacher_name VARCHAR NOT NULL,
        teacher_phone_number VARCHAR NOT NULL,
        room_number VARCHAR NOT NULL,
        num_students_enrolled INT NOT NULL
);
''')

#INSERT INTO users (username, password, affiliation) VALUES ('admin', 'super_omega_chiapet69420!', 'administrator');
cur.execute('''
        INSERT INTO users (
            username,
            password,
            affiliation
        ) VALUES (
            'admin',
            'a8705051da419e0bedda2e9bbe4c90a04da5001a2c8af24526c1120cb9a0a927',
            'administrator'
        );
''')

classes_data = (
        ('History', 'Joe Misetta', '(571) 568-7817', '215', 26),
        ('Biology', 'Alyssa Martinez', '(703) 570-2761', '412', 18),
        ('Chemistry', 'Walter Greene', '(202) 953-2888', '430', 20),
        ('Calculus', 'Suzanne Car', '(703) 484-0980', '404', 15),
        ('Algebra', 'Kara Erickson', '(571) 956-4884', '470', 22),
        ('English', 'John Brown', '(202) 315-6253', '201', 19),
        ('Geometry', 'Jessie Whiteman', '(571) 212-3487', '411', 27),
        ('Spanish', 'Isabella Garcia', '(571) 288-9939', '342', 30),
)

cur.executemany('''
        INSERT INTO classes (
            class_name,
            teacher_name,
            teacher_phone_number,
            room_number,
            num_students_enrolled
        ) VALUES (?, ?, ?, ?, ?)''', classes_data)

con.commit()

@app.route('/level0', methods=['GET', 'POST'])
def level0():
    logged_in = False
    error = ''
    if request.method == 'POST':
        # probably bad to make a new connection each time!?
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        try:
            resp = cur.execute(query).fetchall()
        except:
            return f'<h1>ERROR 500 - INTERNAL SERVER ERROR</h1><p>Invalid syntax in SQL query: {query}</p>'
        if len(resp) >= 1:
            logged_in = True
        else:
            error = 'Invalid credentials'
    return render_template('level0.html', error=error, logged_in=logged_in)

@app.route('/level1', methods=['GET', 'POST'])
def level1():
    logged_in = False
    error = ''
    if request.method == 'POST':
        # probably bad to make a new connection each time!?
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        try:
            resp = cur.execute(query).fetchall()
        except:
            return f'<h1>ERROR 500 - INTERNAL SERVER ERROR</h1><p>Invalid syntax in SQL query: {query}</p>'
        if len(resp) >= 1:
            logged_in = True
        else:
            error = 'Invalid credentials'
    return render_template('level1.html', error=error, logged_in=logged_in)


@app.route('/level2', methods=['GET', 'POST'])
def level2():
    logged_in = False
    error = ''
    if request.method == 'POST':
        # probably bad to make a new connection each time!?
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        query = re.sub('OR', '', query, flags=re.IGNORECASE)  # remove 'OR' from query
        try:
            resp = cur.execute(query).fetchall()
        except:
            return f'<h1>ERROR 500 - INTERNAL SERVER ERROR</h1><p>Invalid syntax in SQL query: {query}</p>'
        if len(resp) >= 1:
            logged_in = True
        else:
            error = 'Invalid credentials'
    return render_template('level2.html', error=error, logged_in=logged_in)


@app.route('/level3', methods=['GET', 'POST'])
def level3():
    logged_in = False
    error = ''
    if request.method == 'POST':
        # probably bad to make a new connection each time!?
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        affiliation = request.form['affiliation']
        query = f"SELECT * FROM users WHERE username=? AND password=? AND affiliation='{affiliation}';"
        try:
            resp = cur.execute(query, (username, password)).fetchall()
        except:
            return f'<h1>ERROR 500 - INTERNAL SERVER ERROR</h1><p>Invalid syntax in SQL query: {query}</p>'
        if len(resp) >= 1:
            logged_in = True
        else:
            error = 'Invalid credentials'
    return render_template('level3.html', error=error, logged_in=logged_in)

'''
        class_name VARCHAR NOT NULL,
        teacher_name VARCHAR NOT NULL,
        teacher_phone_number VARCHAR NOT NULL,
        room_number VARCHAR NOT NULL,
        num_students_enrolled INT NOT NULL
        '''
@app.route('/level4', methods=['GET', 'POST'])
def level4():
    error = ''
    if request.method == 'POST' and 'formtype' in request.form and request.form['formtype'] == 'phonesubmit':
        if check_phone():
            return render_template('/win.html')
        error = 'Incorrect phone number. Keep trying!'

    # probably bad to make a new connection each time!?
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    teacher = request.form['search'] if request.method == 'POST' and request.form['formtype'] == 'search' else ''
    teacher = f'%{teacher}%'
    query = f"SELECT class_name, teacher_name, room_number, num_students_enrolled FROM classes WHERE teacher_name LIKE '{teacher}'"
    try:
        resp = cur.execute(query).fetchall()
    except:
        return f'<h1>ERROR 500 - INTERNAL SERVER ERROR</h1><p>Invalid syntax in SQL query: {query}</p>'
    return render_template('level4.html', resp=resp, error=error)


def check_phone():
    return request.form['phone'].strip().replace(' ', '') in ('(571)568-7817', '571-568-7817', '5715687817')


#app.run('localhost', 8888)
