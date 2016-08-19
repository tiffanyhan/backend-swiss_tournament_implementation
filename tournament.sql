-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE Players (id serial primary key, name text);

CREATE TABLE Matches (id serial primary key, winner_id integer references Players(id), loser_id integer references Players(id));

CREATE VIEW wins AS SELECT players.id AS player_id, count(matches.winner_id) AS wins FROM players LEFT JOIN matches ON players.id = matches.winner_id GROUP BY players.id;

CREATE VIEW losses AS SELECT players.id AS player_id, count(matches.loser_id) AS losses FROM players LEFT JOIN matches ON players.id = matches.loser_id GROUP BY players.id;

CREATE VIEW matchesplayed AS SELECT wins.player_id AS player_id, wins.wins + losses.losses AS matches FROM wins join losses on wins.player_id = losses.player_id;

CREATE VIEW scores AS SELECT wins.player_id AS player_id, wins.wins, losses.losses, wins.wins + losses.losses AS matches FROM wins join losses ON wins.player_id = losses.player_id;