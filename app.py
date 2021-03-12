from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)
app.secret_key = "key"

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
    else:
        return render_template('users.html')


@app.route('/bet_slips', methods=['GET','POST'])
def bet_slips():
    if request.method == 'POST':
        # fetch form data
        betSlips = request.form
        if betSlips.get('wager', False) and betSlips.get('bet_type', False) and betSlips.get('game_id', False) and betSlips.get('user_id', False):
            wager = betSlips['wager']
            bet_type = betSlips['bet_type']
            game_id = betSlips['game_id']
            user_id = betSlips['user_id']
            cur = mysql.connection.cursor()
            #check if bet_slip exists or must be added
            resultValue = cur.execute("SELECT slip_id FROM Bet_slips WHERE wager = %s AND bet_type = %s AND game_id = %s", (wager, bet_type, game_id))
            mysql.connection.commit()
            if resultValue > 0:
                slip = cur.fetchall()
                cur.execute("INSERT INTO Users_bet_slips (user_id, slip_id) VALUES (%s, %s)", (user_id,slip))
                mysql.connection.commit()
            else:
                cur.execute("INSERT INTO Bet_slips(wager, bet_type, game_id) VALUES(%s, %s, %s)", (wager, bet_type, game_id))
                mysql.connection.commit()
                cur.execute("INSERT INTO Users_bet_slips (user_id, slip_id) VALUES (%s, (SELECT slip_id FROM Bet_slips \
                    WHERE wager = %s AND bet_type = %s AND game_id = %s))", (user_id,wager, bet_type, game_id))
                mysql.connection.commit()
            cur.close()
            return redirect('/bet_slips')

    cur = mysql.connection.cursor()
    gamesValue = cur.execute("SELECT game_id, team_a, team_b FROM Games")
    games=None
    if gamesValue > 0:
        games = cur.fetchall()
        cur.close()

    cur = mysql.connection.cursor()
    usersValue = cur.execute("SELECT user_id, username FROM Users")
    users=None
    if usersValue > 0:
        users = cur.fetchall()
        cur.close()

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT Bet_slips.slip_id, wager, bet_type, bet_won, payout_status, team_a, team_b, Users_bet_slips.user_id \
                                FROM Bet_slips \
                                INNER JOIN Games ON Games.game_id = Bet_slips.game_id \
                                INNER JOIN Users_bet_slips ON Users_bet_slips.slip_id = Bet_slips.slip_id")
    if resultValue > 0:
        betSlips = cur.fetchall()
        return render_template('bet_slips.html', users=users, games=games, betSlips=betSlips)
    else:
        return render_template('bet_slips.html', users=users, games=games)

@app.route('/filter_bet_slips', methods=['GET','POST'])
def filter_bet_slips():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        gamesValue = cur.execute("SELECT game_id, team_a, team_b FROM Games")
        games = None
        if gamesValue > 0:
            games = cur.fetchall()
            cur.close()

        cur = mysql.connection.cursor()
        usersValue = cur.execute("SELECT user_id, username FROM Users")
        users = None
        if usersValue > 0:
            users = cur.fetchall()
            cur.close()
        betSlips = request.form
        if betSlips.get('game_id', False):
            game_id = betSlips['game_id']
            cur = mysql.connection.cursor()
            resultValue = cur.execute("SELECT Bet_slips.slip_id, wager, bet_type, bet_won, payout_status, team_a, team_b, Users_bet_slips.user_id \
                                FROM Bet_slips \
                                INNER JOIN Games ON Games.game_id = Bet_slips.game_id \
                                INNER JOIN Users_bet_slips ON Users_bet_slips.slip_id = Bet_slips.slip_id \
                                WHERE Games.game_id = %s", (game_id))
            mysql.connection.commit()
            if resultValue > 0:
                betSlips = cur.fetchall()
                return render_template('bet_slips.html', users=users, games=games, betSlips=betSlips)
            else:
                 return render_template('bet_slips.html', users=users, games=games)
        else:
            return render_template('bet_slips.html', users=users, games=games)

@app.route('/remove_bet_slip', methods=['POST'])
def bet_slips_removal():
    if request.method == 'POST':
        removalSlip = request.form['slip_id_user_id']
        #print(type(removalSlip))
        list = [int(x) for x in removalSlip.split(",")]
        #print(list)
        slip_id = list[0]
        #print(slip_id)
        user_id = list[1]
        #print(user_id)
        cur = mysql.connection.cursor()
        #Check if bet is parlayed
        parlayValue = None
        parlayValue = cur.execute("SELECT Parlay.parlay_id FROM Parlay \
            INNER JOIN Parlay_bet_slips ON Parlay.parlay_id = Parlay_bet_slips.parlay_id WHERE Parlay.user_id = %s \
            AND Parlay_bet_slips.slip_id = %s",(slip_id, user_id))
        mysql.connection.commit()
        # print(parlayValue)
        # print(slip_id, user_id)
        if parlayValue > 0:
            parlayIDs = cur.fetchall()
            #print(parlayIDs)
            for parlayID in parlayIDs:
                print(parlayID[0])
                #cur.execute("DELETE * FROM Parlay WHERE parlay_id = %s",[parlayID])
                #mysql.connection.commit()
            message = "Parlays associated with this Bet Slip were also deleted"
            flash(message)
        #check if bet slip is associated with multiple bets
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT COUNT(user_id) FROM Users_bet_slips WHERE slip_id = %s", [slip_id])
        if resultValue > 0:
            slip_count = cur.fetchall()
            slip_count = slip_count[0][0]
            # if multiple bets associated with bet_slip, deleted only entry in Users_bet_slips
            if slip_count > 1:
                cur.execute("DELETE FROM Users_bet_slips WHERE slip_id = %s AND user_id = %s", (slip_id, user_id))
                mysql.connection.commit()
            #if only one bet associated with a bet_slip, delete bet_slip (users_bet_slips will delete on cascade)
            else:

                cur.execute("DELETE FROM Bet_slips WHERE slip_id = %s", [slip_id])
                mysql.connection.commit()
        cur.close()

        return redirect('/bet_slips')

@app.route('/users_bet_slips', methods=['GET','POST'])
def users_bet_slips():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Users_bet_slips")
    if resultValue > 0:
        usersBetSlips = cur.fetchall()
        return render_template('users_bet_slips.html', usersBetSlips=usersBetSlips)
    else:
        return render_template('users_bet_slips.html')

@app.route('/parlays_bet_slips', methods=['GET','POST'])
def parlays_bet_slips():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Parlay_bet_slips")
    if resultValue > 0:
        parlaysBetSlips = cur.fetchall()
        return render_template('parlays_bet_slips.html', parlaysBetSlips=parlaysBetSlips)
    else:
        return render_template('parlays_bet_slips.html')

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
    if gameDetails.get('game', False) and gameDetails.get('margin', False) and gameDetails.get('total', False):
        game_id = gameDetails['game']
        margin = gameDetails['margin']
        total = gameDetails['total']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Games SET game_winner_margin = %s, game_total = %s where game_id = %s", (margin, total, game_id))
        mysql.connection.commit()
        over_under_line = cur.execute("SELECT over_under_line FROM Games WHERE game_id = %s", (game_id))
        if over_under_line > 0:
            over_under_line = cur.fetchone()
            if (int(total) - int(over_under_line[0])) > 0:
                cur.execute("UPDATE Bet_slips SET bet_won = '1' WHERE game_id = %s AND bet_type = 'OVER'", (game_id))
                mysql.connection.commit()
                cur.execute("UPDATE Bet_slips SET bet_won = '0' WHERE game_id = %s AND bet_type = 'UNDER'", (game_id))
                mysql.connection.commit()
            elif (int(total) - int(over_under_line[0])) < 0:
                cur.execute("UPDATE Bet_slips SET bet_won = '0' WHERE game_id = %s AND bet_type = 'OVER'", (game_id))
                mysql.connection.commit()
                cur.execute("UPDATE Bet_slips SET bet_won = '1' WHERE game_id = %s AND bet_type = 'UNDER'", (game_id))
                mysql.connection.commit()
        if int(margin) < 0:
            cur.execute("UPDATE Games SET game_winner = team_a WHERE game_id = %s", (game_id))
            mysql.connection.commit()
            cur.execute("UPDATE Bet_slips SET bet_won = '1' WHERE game_id = %s AND bet_type = 'TEAM_A_MONEY_LINE'", (game_id))
            mysql.connection.commit()
            cur.execute("UPDATE Bet_slips SET bet_won = '0' WHERE game_id = %s AND bet_type = 'TEAM_B_MONEY_LINE'", (game_id))
            mysql.connection.commit()
        elif int(margin) > 0:
            cur.execute("UPDATE Games SET game_winner = team_b WHERE game_id = %s", (game_id))
            mysql.connection.commit()
            cur.execute("UPDATE Bet_slips SET bet_won = '0' WHERE game_id = %s AND bet_type = 'TEAM_A_MONEY_LINE'", (game_id))
            mysql.connection.commit()
            cur.execute("UPDATE Bet_slips SET bet_won = '1' WHERE game_id = %s AND bet_type = 'TEAM_B_MONEY_LINE'", (game_id))
            mysql.connection.commit()

        cur.close()
        cur = mysql.connection.cursor()
        spread = cur.execute("SELECT spread FROM Games WHERE game_id = %s", (game_id))
        if spread > 0:
            spread = cur.fetchone()

        if int(margin) < -int(spread[0]):
            cur.execute("UPDATE Bet_slips SET bet_won = '1' WHERE game_id = %s AND bet_type = 'TEAM_A_SPREAD'", (game_id))
            mysql.connection.commit()
            cur.execute("UPDATE Bet_slips SET bet_won = '0' WHERE game_id = %s AND bet_type = 'TEAM_B_SPREAD'", (game_id))
            mysql.connection.commit()
        elif int(margin) > -int(spread[0]):
            cur.execute("UPDATE Bet_slips SET bet_won = '0' WHERE game_id = %s AND bet_type = 'TEAM_A_SPREAD'", (game_id))
            mysql.connection.commit()
            cur.execute("UPDATE Bet_slips SET bet_won = '1' WHERE game_id = %s AND bet_type = 'TEAM_B_SPREAD'", (game_id))
            mysql.connection.commit()
        # Update user balances
        bets_to_be_paid = cur.execute("SELECT Users_bet_slips.user_id, Bet_slips.bet_type, Bet_slips.wager, Bet_slips.game_id \
                    FROM Bet_slips INNER JOIN Users_bet_slips ON \
                    Users_bet_slips.slip_id = Bet_slips.slip_id WHERE bet_won = 1 AND payout_status IS NULL")
        if bets_to_be_paid > 0:
            bets_to_be_paid = cur.fetchall()
            for bet in bets_to_be_paid:
                if bet[1] == 'TEAM_A_MONEY_LINE':
                    #calculate payout
                    odds = cur.execute("SELECT team_a_odds FROM Games WHERE game_id = %s", (str(bet[3])))
                    if odds > 0:
                        odds = cur.fetchone()[0]
                        if odds > 0:
                            payout = int(odds)/100.0 * int(bet[2])
                        elif odds < 0:
                            payout = abs(int(odds)) / 100.0 * int(bet[2])
                    payout_apply_to_balance(payout, str(bet[0]))
                elif bet[1] == 'TEAM_B_MONEY_LINE':
                    #calculate payout
                    odds = cur.execute("SELECT team_a_odds FROM Games WHERE game_id = %s", (bet[3]))
                    if odds > 0:
                        odds = cur.fetchone()[0]
                        if odds > 0:
                            payout = int(odds)/100.0 * int(bet[2])
                        elif odds < 0:
                            payout = abs(int(odds)) / 100.0 * int(bet[2])
                    payout_apply_to_balance(payout, str(bet[0]))
                else:
                    payout = int(bet[2])
                    payout_apply_to_balance(payout, str(bet[0]))
        return redirect('/games')
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line, game_id, game_winner_margin, game_winner, game_total FROM Games")
    if resultValue > 0:
        games = cur.fetchall()
        return render_template('games.html', games=games)

def payout_apply_to_balance(payout, user_id):
    print(payout, type(payout))
    print(user_id, type(user_id))
    cur = mysql.connection.cursor()
    current_balance = cur.execute("SELECT balance FROM Users WHERE user_id = %s",(user_id))
    if current_balance > 0:
        current_balance = float(cur.fetchone()[0])
        cur.execute("UPDATE Users SET balance = %s WHERE user_id = %s", (current_balance+payout, user_id))
        mysql.connection.commit()
    cur.close()

@app.route('/parlays', methods=['GET', 'POST'])
def parlays():
    if request.method == 'POST':
        parlayDetails = request.form
        if parlayDetails.get('parlay_1', False) and parlayDetails.get('parlay_2', False):
            parlay_1 = parlayDetails['parlay_1']
            parlay_2 = parlayDetails['parlay_2']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Parlay(payout_status, user_id) VALUES(NULL, (SELECT user_id FROM Users_bet_slips WHERE slip_id = %s LIMIT 1))", (parlay_1))
            mysql.connection.commit()
            cur.execute("INSERT INTO Parlay_bet_slips(slip_id, parlay_id) VALUES(%s, (SELECT parlay_id FROM Parlay ORDER BY parlay_id DESC LIMIT 1))", (parlay_1))
            mysql.connection.commit()
            cur.execute("INSERT INTO Parlay_bet_slips(slip_id, parlay_id) VALUES(%s, (SELECT parlay_id FROM Parlay ORDER BY parlay_id DESC LIMIT 1))", (parlay_2))
            mysql.connection.commit()
            cur.close()
            return redirect('/parlays')
        elif parlayDetails.get('parlay_delete', False):
            parlay_delete = parlayDetails['parlay_delete']
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Parlay_bet_slips WHERE parlay_id = %s", (parlay_delete))
            mysql.connection.commit()
            cur.execute("DELETE FROM Parlay WHERE parlay_id = %s", (parlay_delete))
            mysql.connection.commit()
            cur.close()
            return redirect('/parlays')

    cur = mysql.connection.cursor()
    betSlipsValue = cur.execute("SELECT Bet_slips.slip_id FROM Bet_slips")
    if betSlipsValue > 0:
        betSlips = cur.fetchall()
        cur.close()

    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Parlay")
    print(resultValue)
    if resultValue > 0:
        parlays = cur.fetchall()
        cur.close()
        print(parlays)
        return render_template('parlays.html', betSlips=betSlips, parlays=parlays)
    elif betSlipsValue > 0:
        return render_template('parlays.html', betSlips=betSlips)
    else: 
        return render_template('parlays.html')

if __name__ == "__main__":
    app.run(debug=True)