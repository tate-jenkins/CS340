-- inserting users
INSERT INTO Users(username, balance) VALUES(username, balance)
-- deleting users
DELETE FROM Users WHERE username = username
-- updating users balance
UPDATE Users SET balance = balance_adjustment WHERE username = username_adjustment
-- selecting users for html table
SELECT user_id, username, balance FROM Users
-- inserting new bet slips
INSERT INTO Bet_slips(wager, bet_type, game_id) VALUES(wager, bet_type, game_id)
-- selecting bet slips for html table
SELECT team_a, team_b, slip_id, bet_type, parlay_id, wager, payout_status \
                                FROM Games \
                                INNER JOIN Bet_slips ON Games.game_id = Bet_slips.game_id
-- inserting new games
INSERT INTO Games(team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line) VALUES(team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line)
-- updating games
UPDATE Games SET game_winner_margin = margin where game_id = game_id
-- selecting games for html table
SELECT team_a, team_a_odds, team_b, team_b_odds, spread, over_under_line, game_id, game_winner_margin FROM Games
-- inserting new parlay
INSERT INTO Parlay(parlay_1, parlay_2) VALUES(parlay_1, parlay_2)
-- selecting parlays for html table
SELECT * FROM Parlay