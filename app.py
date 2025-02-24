from flask import Flask, render_template,request,redirect,url_for,session,flash
import sqlite3
from flask_session import Session
from datetime import datetime

app=Flask(__name__)

app.secret_key='nithya@26'
app.config['SESSION_TYPE']='filesystem'
Session(app)


ADMIN_CREDENTIALS={
    'Admin':'admin123',
    'Varun':'12345',
    'Mega':'123'
}


def init_db():
    conn=sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute(''' create table if not exists users
                   (id integer primary key autoincrement,
                   name text not null,
                   mail text not null,
                   date text not null)''')
    conn.commit()
    conn.close()



@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mail = request.form['mail']
    date_str = request.form['date']


    appointment_date = datetime.strptime(date_str, '%y-%m-%d')
    current_date = datetime.now()

    if appointment_date<current_date:
        flash("Error: The appoinment data cannot be in the past.")
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, mail, date)VALUES(?, ?, ?)' (name, mail, date_str ))
    conn.commit()
    conn.close()

    flask(f"Appointment confirmed for {name} on {date_str}. A confirmation email will be send to {mail}.")
    
    
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['logged_in'] = True
            flash('Successfully logged in!')
            return redirect(url_for('result'))
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you have been logged out.')
    

    
if __name__ == '__main__':
    app.run(debug=True)
