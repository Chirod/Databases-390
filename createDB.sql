DROP TABLE IF EXISTS players, tournaments, tournament_player, results, officials;

create table players(
	id int(11) auto_increment,
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	primary key (id)
);

create table officials(
	id int(11) auto_increment,
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	primary key (id)
);

create table tournaments(
	id int(11) auto_increment,
	name varchar(100) not null,
	format varchar(50) not null,
	start_date date not null,
	end_date date,
	official_id int(11) null,
	primary key (id),
	foreign key (official_id) references officials(id)
);

create table results(
	id int(11) auto_increment,
	tournament_id int(11) not null,
	round_id int(11) not null,
	match_id int(11) not null,
	player_id int(11) not null,
	outcome varchar(50) not null,
	score int(11) default 0,
	primary key (id),
	foreign key (tournament_id) references tournaments(id),
	foreign key (player_id) references players(id)
);

create table tournament_player(
	tid int(11),
	pid int(11),
	primary key (tid, pid),
	foreign key (tid) references tournaments(id),
	foreign key (pid) references players(id)
);

insert into players (first_name, last_name)
values
	("Christopher", "Wohlwend"),
	("Brian", "Kibbler"),
	("Another", "Dude"),
	("Paulo", "Vitor");

insert into officials (first_name, last_name)
values
	("Official", "One"),
	("Guy", "Two"),
	("Judge", "Three");

insert into tournaments (name, format, start_date, official_id)
values
	("First", "Slalom", date "2019-5-11", (select id from officials where first_name = "Judge" and last_name = "Three"));

insert into tournaments (name, format, start_date, end_date, official_id)
values
	("Completed", "Modern", date "2019-4-30", date "2019-4-30", (select id from officials where first_name = "Judge" and last_name = "Three"));

insert into tournament_player (pid, tid)
values
	( (select id from players where first_name = "Christopher" and last_name = "Wohlwend"), (select id from tournaments where name = "First") ),
	( (select id from players where first_name = "Christopher" and last_name = "Wohlwend"), (select id from tournaments where name = "Completed") ),
	( (select id from players where first_name = "Brian" and last_name = "Kibbler"), (select id from tournaments where name = "Completed") ),
	( (select id from players where first_name = "Paulo" and last_name = "Vitor"), (select id from tournaments where name = "Completed") ),
	( (select id from players where first_name = "Another" and last_name = "Dude"), (select id from tournaments where name = "First") );

insert into results (tournament_id, round_id, match_id, player_id, outcome, score)
values
	( (select id from tournaments where name = "First"), 1, 1, (select id from players where first_name = "Christopher" and last_name = "Wohlwend"), "Winner", 98),
	( (select id from tournaments where name = "First"), 1, 1, (select id from players where first_name = "Another" and last_name = "Dude"), "Loser", 50),
	( (select id from tournaments where name = "First"), 2, 2, (select id from players where first_name = "Christopher" and last_name = "Wohlwend"), "Loser", 78),
	( (select id from tournaments where name = "First"), 2, 2, (select id from players where first_name = "Another" and last_name = "Dude"), "Winner", 79),
	( (select id from tournaments where name = "Completed"), 1, 1, (select id from players where first_name = "Christopher" and last_name = "Wohlwend"), "Winner", 2),
	( (select id from tournaments where name = "Completed"), 1, 1, (select id from players where first_name = "Brian" and last_name = "Kibbler"), "Loser", 1),
	( (select id from tournaments where name = "Completed"), 1, 1, (select id from players where first_name = "Paulo" and last_name = "Vitor"), "Bye", 2);
