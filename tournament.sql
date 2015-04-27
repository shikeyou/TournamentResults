-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create a players table
CREATE TABLE players (
    id serial primary key,                  --id of a player
    name text                               --name of a player
);

-- Create a matches table
CREATE TABLE matches (
    id serial primary key,                  --id of a match
    winner integer references players(id),  --id of the winner for a match
    loser integer references players(id)    --id of the loser for a match
);

-- Create a score view that tallies up the total wins & loses for each player.
-- The query needs a triple left join because the matches table references the
-- player table twice.
CREATE VIEW score AS
SELECT p.id as id, p.name as name, COUNT(m1.winner) as wins, COUNT(m2.loser) as loses
FROM players as p LEFT JOIN matches as m1 ON p.id = m1.winner
LEFT JOIN matches as m2 on p.id = m2.loser
GROUP BY p.id
ORDER BY p.id ASC;
