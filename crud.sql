/* All variables indicated with [varname] */

/* Query to find all results of a player */
select R.outcome, R.score from results R
inner join players P on R.player_id = P.id
where P.first_name = [fname] and P.last_name = [lname];

/* Query to find all results in a tournament */
select P.first_name, P.last_name, R.result, R.score from results R
inner join players P on R.player_id = P.id
inner join tournaments T on R.tournament_id = T.id
where T.name = [tname];


/* Query to find all players in a tournament */
select P.first_name, P.last_name from players P
inner join tournament_player TP on P.id = TP.pid
inner join tournaments T on TP.tid = T.id
where T.name = [tname];

/* Query to find all tournaments a player is enrolled in */
select c.name from players P
inner join tournament_player TP on P.id = TP.pid
inner join tournaments T on TP.tid = T.id
where P.first_name = [fname] and P.last_name = [lname];

/* Create New Player */
insert into players (first_name,last_name)
values ([fname],[lname]);

/* Create New Official */
insert into officials (first_name,last_name)
values ([fname],[lname]);

/* Create new tournament */
insert into tournaments (name, format, start_date, official_id)
values
([name], [format], [start_date], (select id from officals where id = [official_id]));

/* add player to tournament */
insert into tournament_player (tid, pid)
values
( (select id from tournaments where name = [tname]), (select id from players where first_name = [fname] and last_name = [lname]) );

/* add result to tournamet*/
insert into results (tournament_id, round_id, match_id, player_id, outcome, score)
values
( (select id from tournaments where name = [tname]), [roundid], [matchid], (select id from players where first_name = [fname] and last_name = [lname]), [outcome], [score]),

/* remove result from tournamet*/
delete from results where id = [id]

/* end a tourament*/
update tournaments
set end_date = [enddate]
where name = [tname]