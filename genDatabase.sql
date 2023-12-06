DROP DATABASE IF EXISTS sharing;

CREATE DATABASE sharing;

USE sharing;

CREATE TABLE `groceries` (
  `groceryID` int(11) NOT NULL PRIMARY KEY,
  `name` varchar(14) DEFAULT NULL
);

INSERT INTO `groceries` (`groceryID`, `name`) VALUES
(1, 'Milo'),
(2, 'Butter'),
(3, 'Toilet Paper');

CREATE TABLE `purchasehistory` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `userID` int(11) DEFAULT NULL,
  `groceryID` int(11) DEFAULT NULL,
  `purchaseDate` date NOT NULL
);

CREATE TABLE `sharing` (
  `userID` int(11) NOT NULL,
  `groceryID` int(11) NOT NULL,

   PRIMARY KEY(userID, groceryID)
);

INSERT INTO `sharing` (`userID`, `groceryID`) VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 1),
(2, 2),
(2, 3),
(3, 1),
(3, 2),
(3, 3),
(4, 2),
(4, 3),
(5, 3);

CREATE TABLE `users` (
  `userID` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(10) DEFAULT NULL
);

INSERT INTO `users` (`userID`, `name`) VALUES
(1, 'Leo'),
(2, 'Lori'),
(3, 'Lex'),
(4, 'Matt'),
(5, 'Archie');