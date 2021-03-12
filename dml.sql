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
SELECT Bet_slips.slip_id, wager, bet_type, bet_won, payout_status, team_a, team_b, Users_bet_slips.user_id \
                                FROM Bet_slips \
                                INNER JOIN Games ON Games.game_id = Bet_slips.game_id \
                                INNER JOIN Users_bet_slips ON Users_bet_slips.slip_id = Bet_slips.slip_id
-- filtering bet slips for html table
SELECT Bet_slips.slip_id, wager, bet_type, bet_won, payout_status, team_a, team_b, Users_bet_slips.user_id \
                                FROM Bet_slips \
                                INNER JOIN Games ON Games.game_id = Bet_slips.game_id \
                                INNER JOIN Users_bet_slips ON Users_bet_slips.slip_id = Bet_slips.slip_id \
                                WHERE Games.game_id = :game_id
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
-- Select slip_id for specific bet. Used to check if a bet slip already exists for a particular bet
SELECT slip_id FROM Bet_slips WHERE wager = :wager AND bet_type = :bet_type AND game_id = :game_id
-- Find if bet is parlayed
SELECT Parlay.parlay_id FROM Parlay
INNER JOIN Parlay_bet_slips ON Parlay.parlay_id = Parlay_bet_slips.parlay_id
WHERE Parlay.user_id = :user_id AND Parlay_bet_slips.slip_id = :slip_id
-- Delete entry from Users_bet_slips
DELETE FROM Users_bet_slips WHERE slip_id = :slip_id AND user_id = :user_id
-- Check if bet slip is associated to multiple bets (multiple users)
SELECT COUNT(user_id) FROM Users_bet_slips WHERE slip_id = :slip_id AND user_id = :user_id

-- Get info on bet_slips that need to be paid out and user_id for balance of each bet
SELECT Users_bet_slips.user_id, Bet_slips.bet_type, Bet_slips.wager, Bet_slips.game_id
FROM Bet_slips
INNER JOIN Users_bet_slips ON Users_bet_slips.slip_id = Bet_slips.slip_id
WHERE bet_won = 1 and payout_status = `NULL`
--Get payout odds for specific wager
SELECT team_a_odds FROM Games WHERE game_id = :game_id
SELECT team_b_odds FROM Games WHERE game_id = :game_id
-- Update user balance
SELECT balance FROM Users WHERE user_id = :user_id
UPDATE Users SET balance = :old_balance+payout WHERE user_id = :user_id