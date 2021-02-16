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
    resultValue = cur.execute("SELECT * FROM Users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('index.html', userDetails=userDetails)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        # fetch form data
        userDetails = request.form
        if userDetails.get('username', False):
            username = userDetails['username']
            balance = userDetails['balance']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Users(username, balance) VALUES(%s, %s)", (username, balance))
            mysql.connection.commit()
            cur.close()
            return redirect('/users')
        username_delete = userDetails.get('username_delete', '')
        if len(username_delete) > 0:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Users WHERE username = %s", (username_delete,))
            mysql.connection.commit()
            cur.close()
            return redirect('/users')
        username_adjustment = userDetails.get('username_adjustment', '')
        balance_adjustment = userDetails.get('balance_adjustment', 0)
        if int(balance_adjustment) > 0:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Users SET balance = %s WHERE username = %s", (balance_adjustment, username_adjustment))
            mysql.connection.commit()
            cur.close()
            return redirect('/users')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT user_id, username, balance FROM Users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)


@app.route('/bet_slips', methods=['GET','POST'])
def bet_slips():
    if request.method == 'POST':
        # fetch form data
        betSlips = request.form
        if betSlips.get('wager', False):
            wager = betSlips['wager']
            bet_type = betSlips['bet_type']
            game_id = betSlips['game_id']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Bet_slips(wager, bet_type, game_id) VALUES(%s, %s, %s)", (wager, bet_type, game_id))
            mysql.connection.commit()
            cur.close()
            return redirect('/bet_slips')

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT team_a, team_b, slip_id, bet_type, parlay_id, wager, payout_status \
                                FROM Games \
                                INNER JOIN Bet_slips ON Games.game_id = Bet_slips.game_id")
    if resultValue > 0:
        betSlips = cur.fetchall()
        return render_template('bet_slips.html', betSlips=betSlips)


@app.route('/games', methods=['GET','POST'])
def games():
    gameDetails = request.form
    if gameDetails.get('spread', False) and gameDetails.get('team_a', False) \
            and gameDetails.get('team_b', False) and gameDetails.get('team_a_odds', False) \
            and gameDetails.get('team_b_odds', False) and gameDetails.get('over_under_line', False):
        spread = gameDetails['spread']
        team_a = gameDetails['team_a']
        team_b = gameDetails['team_b']
        team_a_odds = gameDetails['team_a_odds']
        team_b_odds = gameDetails['team_b_odds']
        over_under_line = gameDetails['spread']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Games(team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line) VALUES(%s, %s, %s, %s, %s, %s)", (team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line))
        mysql.connection.commit()
        cur.close()
        return redirect('/games')
    if gameDetails.get('game', False) and gameDetails.get('margin', False):
        game_id = gameDetails['game']
        margin = gameDetails['margin']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Games SET game_winner_margin = %s where game_id = %s", (margin, game_id))
        mysql.connection.commit()
        cur.close()
        return redirect('/games')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line, game_id, game_winner_margin FROM Games")
    if resultValue > 0:
        games = cur.fetchall()
        return render_template('games.html', games=games)

@app.route('/parlays', methods=['GET', 'POST'])
def parlays():
    parlayDetails = request.form
    if parlayDetails.get('parlay_1', False) and parlayDetails.get('parlay_2', False):
        parlay_1 = parlayDetails['parlay_1']
        parlay_2 = parlayDetails['parlay_2']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Parlay(parlay_1, parlay_2) VALUES(%s, %s)", (parlay_1, parlay_2))
        mysql.connection.commit()
        cur.close()
        return redirect('/parlays')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Parlay")
    if resultValue > 0:
        parlays = cur.fetchall()
        return render_template('parlays.html', parlays=parlays)

if __name__ == "__main__":
    app.run(debug=True)