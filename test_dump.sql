SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Users_bet_slips;
DROP TABLE IF EXISTS Bet_slips;
DROP TABLE IF EXISTS Parlay;
DROP TABLE IF EXISTS Games;
SET FOREIGN_KEY_CHECKS = 1;

--
-- Table structure for table `Users`
--
CREATE TABLE `Users` (
`user_id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(255) NOT NULL,
`balance` int(11) DEFAULT NULL,
PRIMARY KEY (`user_id`),
UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`username`) VALUES
('vince'),
('tate');

--
-- Table structure for table `Bet_slips`
--
CREATE TABLE `Bet_slips` (
`slip_id` int(11) NOT NULL AUTO_INCREMENT,
`wager` decimal(4,2) NOT NULL,
`bet_type` varchar(255) NOT NULL,
`bet_won` boolean DEFAULT NULL,
`payout_status` boolean DEFAULT NULL,
`game_id` int(11) NOT NULL,
`parlay_id` int(11) DEFAULT NULL,
PRIMARY KEY (`slip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Bet_slips`
--

INSERT INTO `Bet_slips` (`wager`,`bet_type`,`game_id`) VALUES
('10.00', 'spreadA',1),
('10.00', 'over',1);

--
-- Table structure for table `Parlay`
--
CREATE TABLE `Parlay` (
`primary_key` int(11) NOT NULL AUTO_INCREMENT,
`parlay_id` int(11) NOT NULL,
`slip_id` int(11) NOT NULL,
PRIMARY KEY (`primary_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Parlay`
--
INSERT INTO `Parlay` (`parlay_id`,`slip_id`) VALUES
(1,1),
(1,2);
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
('03.0','Chiefs','Buccaneers','149','-169','56.5');

--
-- Table structure for table `Users_bet_slips`
--

CREATE TABLE `Users_bet_slips` (
`primary_key` int(11) NOT NULL AUTO_INCREMENT,
`slip_id` int(11) NOT NULL,
`user_id` int(11),
PRIMARY KEY (`primary_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Dumping data for table `Users_bet_slips`
--
INSERT INTO `Users_bet_slips` (`slip_id`, `user_id`) VALUES
(1,1);