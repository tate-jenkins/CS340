from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)

db = yaml.load(open('templates/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('index.html', userDetails=userDetails)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        username = userDetails['username']
        balance = userDetails['balance']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, balance) VALUES(%s, %s)", (username, balance))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


@app.route('/bet_slips')
def bet_slips():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('bet_slips.html', userDetails=userDetails)

@app.route('/games')
def games():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('games.html', userDetails=userDetails)

if __name__ == "__main__":
    app.run(debug=True)