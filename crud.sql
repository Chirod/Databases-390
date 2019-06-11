/* All variables indicated with [varname] */

/* Query to find all players */
select id, first_name, last_name from players;
 
/* Query to add a player */
insert into players (first_name, last_name) values ([fname], [lname]);

/* Query to update a player */
update players set first_name = [fname], last_name = [last_name] where id = [id];

/* Query to find a player with specific id */
SELECT id, first_name, last_name from players WHERE id = [id];

/* Sequence of queries to delete a player with given id */
delete from results where player_id = [id];
delete from tournament_player where pid = [id];
DELETE FROM players WHERE id = [id];

/* Query to find all tournaments for a given player id */
SELECT t.id, t.name, t.format, t.start_date, t.end_date, 
(SELECT o.first_name FROM officials o where o.id = t.official_id), 
(SELECT o.last_name FROM officials o where o.id = t.official_id) 
FROM tournaments t INNER JOIN tournament_player tp ON tp.tid = t.id WHERE tp.pid = [i];

/* Query to find all tournaments */
select id, name from tournaments;

/* Query to add a player to a tournament */
insert into tournament_player (tid, pid) values ([tid], [pid])

/* Query to remove a player from a tournament */
delete from tournament_player wher pid = [pid] and tid = [tid]

/* Query to get all results for a given player */
SELECT r.id, t.name, r.round_id, r.match_id, r.outcome, r.score, 
(SELECT o.first_name FROM officials o where o.id = t.official_id), 
(SELECT o.last_name FROM officials o where o.id = t.official_id) 
FROM results r INNER JOIN  tournaments t ON r.tournament_id = t.id WHERE r.player_id = [pid];

/* Query to get all tournaments a player is enrolled in */
SELECT id, name 
FROM tournaments t INNER JOIN tournament_player tp ON t.id = tp.tid WHERE tp.pid = [pid];

/* Query to add a result */
INSERT INTO results (tournament_id, player_id, round_id, match_id, outcome, score)
values ([tid], [pid], [rid], [mid], [outcome], [score]);

/* Delete a result */
delete from results where id = [id];

/* find all officials */
select id, first_name, last_name from officials;

/* add an official */
insert into officials (first_name, last_name) values ([fname],[lname])

/* find official with id */
select id, first_name, last_name from officials where id = [id]

/* update an official */
update officials set first_name = [fname], last_name = [lname] where id = [id]

/* delete an official queries */
update tournaments set official_id = NULL where official_id = [id];
delete from officials where id = [id];

/* find all results an official is a part of */
SELECT r.id, t.name, p.first_name, p.last_name, r.round_id, r.match_id, r.outcome, r.score 
FROM results r 
INNER JOIN  tournaments t ON r.tournament_id = t.id 
INNER JOIN players p ON p.id = r.player_id 
WHERE t.official_id = [id];

/* delete results */
delete from results where id = [id]

/* find all tournaments for an official */
SELECT t.id, t.name, t.format, t.start_date, t.end_date 
FROM tournaments t 
INNER JOIN officials o ON t.official_id = o.id 
WHERE t.official_id = [id];

/* new tournament */
INSERT INTO tournaments (name, format, start_date, official_id) 
VALUES ([name] [format], [start_date], [oid]);

/* select all tournaments */
SELECT t.id, t.name, t.format, t.start_date, t.end_date, o.first_name, o.last_name FROM tournaments t, officials o WHERE t.official_id = o.id 
UNION 
SELECT t.id, t.name, t.format, t.start_date, t.end_date, NULL, NULL FROM tournaments t WHERE t.official_id is NULL;

/* select tournament by id */
SELECT id, name, official_id, format, start_date, end_date from tournaments WHERE id = [id];

/* update tournament */
UPDATE tournaments 
SET name = [name], format = [format], official_id = [oid], start_date = [sd], end_date = [ed] 
WHERE id = [id]

/* delete a tournament, and related results/relations */
delete from results where tournament_id = [id];
delete from tournament_player where tid = [id];
DELETE FROM tournaments WHERE id = [id];

/* players in a tournament */
SELECT p.id, p.first_name, p.last_name 
from players p 
INNER JOIN tournament_player tp on p.id = tp.pid 
INNER JOIN tournaments t on tp.tid = t.id where t.id = [id];


/* all results for a tournament */
SELECT r.id, p.first_name, p.last_name, r.round_id, r.match_id, r.outcome, r.score, (SELECT o.first_name FROM officials o WHERE o.id = t.official_id), (SELECT o.last_name FROM officials o WHERE o.id = t.official_id) FROM results r INNER JOIN  tournaments t ON r.tournament_id = t.id INNER JOIN players p ON p.id = r.player_id WHERE r.tournament_id = [id];

/* all players enrolled in a tournament */
SELECT id, first_name, last_name FROM players p INNER JOIN tournament_player tp ON p.id = tp.pid WHERE tp.tid = [id];

/* find all un-ended tournaments */
select id, name from tournaments where id = [id] and end_date is null;

/* update a tournaments end_date */
update touraments set end_date = [ed] where id = [id]
