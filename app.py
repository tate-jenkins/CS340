from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)

db = yaml.load(open('templates/dbv.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Users")
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
        cur.execute("INSERT INTO Users(username, balance) VALUES(%s, %s)", (username, balance))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT username, balance FROM Users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


@app.route('/bet_slips')
def bet_slips():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT team_a, team_b, slip_id, bet_type, parlay_id, wager, payout_status \
                                FROM Games \
                                INNER JOIN Bet_slips ON Games.game_id = Bet_slips.game_id")
    if resultValue > 0:
        betSlips = cur.fetchall()
        return render_template('bet_slips.html', betSlips=betSlips)

@app.route('/games')
def games():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line, game_id FROM Games")
    if resultValue > 0:
        games = cur.fetchall()
        return render_template('games.html', games=games)

if __name__ == "__main__":
    app.run(debug=True)