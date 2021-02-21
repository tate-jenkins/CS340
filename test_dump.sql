SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Users_bet_slips;
DROP TABLE IF EXISTS Parlay;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Bet_slips;
DROP TABLE IF EXISTS Games;
DROP TABLE IF EXISTS Parlay_bet_slips;
SET FOREIGN_KEY_CHECKS = 1;

--
-- Table structure for table `Users`
--
CREATE TABLE Users (
user_id int NOT NULL AUTO_INCREMENT,
username varchar(255) NOT NULL, 
balance numeric(7,2) DEFAULT NULL,
PRIMARY KEY (user_id),
UNIQUE KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`username`) VALUES
('vince'),
('tate'),
('pete');

--
-- Table structure for table `Games`
--
CREATE TABLE `Games` (
`game_id` int(11) NOT NULL AUTO_INCREMENT,
`spread` decimal(3,1) NOT NULL,
`team_a` varchar(255) NOT NULL,
`team_b` varchar(255) NOT NULL,
`team_a_odds` int(11) NOT NULL,
`team_b_odds` int(11) NOT NULL,
`over_under_line` decimal(3,1) NOT NULL,
`game_winner` varchar(255) DEFAULT NULL,
`game_winner_margin` int(11) DEFAULT NULL,
PRIMARY KEY (`game_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Games`
--

INSERT INTO `Games` (`spread`,`team_a`,`team_b`,`team_a_odds`,`team_b_odds`,`over_under_line`) VALUES
('03.0','Chiefs','Buccaneers','149','-169','56.5'),
('07.0','Titans','Rams','142','-175','52.0'),
('06.5','Bears','Packers','144','-171','58.5');

--
-- Table structure for table `Bet_slips`
--
CREATE TABLE `Bet_slips` (
`slip_id` int(11) NOT NULL AUTO_INCREMENT,
`wager` numeric(7,2) NOT NULL,
`bet_type` varchar(255) NOT NULL,
`bet_won` boolean DEFAULT NULL,
`payout_status` boolean DEFAULT NULL,
`game_id` int(11) NOT NULL,
`parlay_id` int(11) DEFAULT NULL,
`user_id` int NOT NULL,
PRIMARY KEY (`slip_id`),
FOREIGN KEY games2bet_slips(`game_id`) 
REFERENCES Games(`game_id`) 
    ON UPDATE CASCADE 
    ON DELETE CASCADE,
    CHECK(Wager>=0),
FOREIGN KEY users2bet_slips(`user_id`) 
REFERENCES Users(`user_id`) 
    ON UPDATE CASCADE 
    ON DELETE CASCADE,
CONSTRAINT CHK_bet_type CHECK(UPPER(bet_type) = 'TEAM_A_MONEY_LINE' OR 
	UPPER(bet_type) = 'TEAM_B_MONEY_LINE' OR
	UPPER(bet_type) = 'TEAM_A_SPREAD' OR
	UPPER(bet_type) = 'TEAM_B_SPREAD' OR
	UPPER(bet_type) = 'OVER' OR
	UPPER(bet_type) = 'UNDER')
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



--
-- Table structure for table `Users_bet_slips`
--

CREATE TABLE `Users_bet_slips` (
`slip_id` int(11) NOT NULL,
`user_id` int(11) NOT NULL,
PRIMARY KEY (`slip_id`, `user_id`),
FOREIGN KEY fk_slip(`slip_id`) REFERENCES Bet_slips(`slip_id`) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY fk_user(`user_id`) REFERENCES Users(`user_id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




--
-- Table structure for table `Parlay`
--
CREATE TABLE `Parlay` (
`parlay_id` int(11) NOT NULL AUTO_INCREMENT,
`parlay_1` int(11) NOT NULL,
`parlay_2` int(11) NOT NULL,
PRIMARY KEY (`parlay_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Parlay_bet_slips` (
`slip_id` int(11) NOT NULL,
`parlay_id` int(11) NOT NULL,
PRIMARY KEY (`slip_id`, `parlay_id`),
FOREIGN KEY fk_p_slip(`slip_id`) REFERENCES Bet_slips(`slip_id`) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY fk_parlay(`parlay_id`) REFERENCES Parlay(`parlay_id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Bet_slips`
--

INSERT INTO `Bet_slips` (`wager`,`bet_type`,`game_id`, `parlay_id`, `user_id`) VALUES
('10.00', 'TEAM_A_SPREAD',1, 1, 1),
('10.00', 'TEAM_B_SPREAD',2, 1, 1),
('10.00', 'OVER',1, NULL, 2);
--
-- Dumping data for table `Users_bet_slips`
--
INSERT INTO `Users_bet_slips` (`slip_id`, `user_id`) VALUES
(33,22);
--
-- Dumping data for table `Parlay`
--
INSERT INTO `Parlay` (`parlay_1`, `parlay_2`) VALUES
(1,2),
(2,3);

INSERT INTO `Parlay_bet_slips` (`slip_id`, `parlay_id`) VALUES
(111,222);