from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
import sys
#create the web application
webapp = Flask(__name__)

@webapp.route('/')
def index():
	return redirect("/browse_players")

''' Begin Players endpoints ---------------------------------------------------------------------'''
@webapp.route('/browse_players')
def browse_players():
	db_connection = connect_to_database()
	query = "SELECT id, first_name, last_name from players;"
	result = execute_query(db_connection, query).fetchall();
	return render_template('browse_players.html', rows=result)

@webapp.route("/new_player", methods=["GET", "POST"])
def newPlayer():
	if request.method == "POST":
		db_connection = connect_to_database()
		query = "insert into players (first_name,last_name) values (%s,%s);"
		fname = request.form['fname']
		lname = request.form['lname']
		data = (fname, lname)
		execute_query(db_connection, query, data)
		return redirect('/browse_players')
	else:
		return render_template("new_player.html")

@webapp.route('/update_player/<int:id>', methods=['POST','GET'])
def update_player(id):
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        player_query = 'SELECT id, first_name, last_name from players WHERE id = %s' % (id)
        player_result = execute_query(db_connection, player_query).fetchone()
        if player_result == None:
            return "No such player found!"
        return render_template('update_player.html', player = player_result)
    elif request.method == 'POST':
        id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        query = "UPDATE players SET first_name = %s, last_name = %s WHERE id = %s"
        data = (fname, lname, id)
        result = execute_query(db_connection, query, data)
        return redirect('/browse_players')

@webapp.route('/delete_player/<int:id>')
def delete_player(id):
	'''deletes the player with the given id'''
	db_connection = connect_to_database()
	querys = []
	querys.append("delete from results where player_id = %s")
	querys.append("delete from tournament_player where pid = %s")
	querys.append("DELETE FROM players WHERE id = %s")
	data = (id,)
	for query in querys:
		result = execute_query(db_connection, query, data)
	return redirect('/browse_players')

@webapp.route("/player_tournaments/<int:pid>")
def playerTournaments(pid):
	db_connection = connect_to_database()
	data = (pid,)
	player_query = "SELECT id, first_name, last_name FROM players WHERE id = %s;"
	player_result = execute_query(db_connection, player_query, data).fetchone();
	tournament_query = "SELECT t.id, t.name, t.format, t.start_date, t.end_date, (SELECT o.first_name FROM officials o where o.id = t.official_id), (SELECT o.last_name FROM officials o where o.id = t.official_id) FROM tournaments t INNER JOIN tournament_player tp ON tp.tid = t.id WHERE tp.pid = %s;"
	tournament_result = execute_query(db_connection, tournament_query, data).fetchall();
	return render_template("player_tournaments.html", rows=tournament_result, player=player_result)

@webapp.route("/add_player_tournament/<int:pid>", methods=["GET", "POST"])
def addPlayerTournament(pid):
	db_connection = connect_to_database()
	if request.method == "GET":
		tournaments_query = "SELECT id, name FROM tournaments;"
		tournaments = execute_query(db_connection, tournaments_query)
		player_query = "SELECT id, first_name, last_name FROM players WHERE id = %s;"
		data = (pid,)
		player = execute_query(db_connection, player_query, data).fetchone();
		return render_template("add_player_tournament.html", player=player, tournaments=tournaments)
	else:
		tid = int(request.form["tournament"])
		query = "INSERT INTO tournament_player (tid, pid) VALUES (%s, %s)"
		data = (tid, pid)
		execute_query(db_connection, query, data)
		return redirect('/player_tournaments/' + str(pid))

@webapp.route("/dropout/<int:pid>/<int:tid>")
def dropout(pid,tid):
	db_connection = connect_to_database()
	query = "DELETE FROM tournament_player WHERE pid = %s AND tid = %s"
	data = (pid,tid)
	result = execute_query(db_connection, query, data)
	return redirect('/player_tournaments/' + str(pid))

@webapp.route("/player_results/<int:pid>")
def playerResults(pid):
	db_connection = connect_to_database()
	player_query = "SELECT id, first_name, last_name FROM players WHERE id = %s;"
	data = (pid,)
	player_result = execute_query(db_connection, player_query, data).fetchone();
	query =	'SELECT r.id, t.name, r.round_id, r.match_id, r.outcome, r.score, (SELECT o.first_name FROM officials o where o.id = t.official_id), (SELECT o.last_name FROM officials o where o.id = t.official_id) FROM results r INNER JOIN  tournaments t ON r.tournament_id = t.id WHERE r.player_id = %s;'
	results = execute_query(db_connection, query, data)
	return render_template("player_results.html", rows=results, player=player_result)

@webapp.route("/add_player_result/<int:pid>", methods=["GET","POST"])
def addPlayerResult(pid):
	db_connection = connect_to_database()
	if request.method =="GET":
		tournament_query = "SELECT id, name FROM tournaments t INNER JOIN tournament_player tp ON t.id = tp.tid WHERE tp.pid = %s;"
		data = (pid,)
		tournament_result = execute_query(db_connection, tournament_query, data).fetchall();
		player_query = "SELECT id, first_name, last_name FROM players WHERE id = %s;"
		player_result = execute_query(db_connection, player_query, data).fetchone();
		return render_template("add_player_result.html", player=player_result, tournaments=tournament_result)
	else:
		tid = int(request.form["tournament"])
		roundid = int(request.form["round"])
		matchid = int(request.form["match"])
		result = request.form["result"]
		score = int(request.form["score"])
		query = "INSERT INTO results (tournament_id, player_id, round_id, match_id, outcome, score) values (%s, %s, %s, %s, %s, %s);"
		data = ( tid, pid, roundid, matchid, result, score)
		execute_query(db_connection, query, data)
		return redirect('/player_results/' + str(pid))

@webapp.route("/delete_player_result/<int:pid>/<int:rid>")
def deletePlayerResult(pid,rid):
	db_connection = connect_to_database()
	query = "DELETE FROM results WHERE id = %s;"
	data = (rid,)
	results = execute_query(db_connection, query, data)
	return redirect('/player_results/' + str(pid))

''' Begin Official endpoints ---------------------------------------------------------------------'''
@webapp.route('/browse_officials')
def browse_officials():
	db_connection = connect_to_database()
	query = "SELECT id, first_name, last_name from officials;"
	result = execute_query(db_connection, query).fetchall();
	return render_template('browse_officials.html', rows=result)

@webapp.route("/new_official", methods=["GET", "POST"])
def newOfficial():
	if request.method == "POST":
		db_connection = connect_to_database()
		query = "insert into officials (first_name,last_name) values (%s,%s);"
		fname = request.form['fname']
		lname = request.form['lname']
		data = (fname, lname)
		execute_query(db_connection, query, data)
		return redirect('/browse_officials')
	else:
		return render_template("new_official.html")

#display update form and process any updates, using the same function
@webapp.route('/update_official/<int:id>', methods=['POST','GET'])
def update_official(id):
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        official_query = 'SELECT id, first_name, last_name from officials WHERE id = %s' % (id)
        official_result = execute_query(db_connection, official_query).fetchone()
        if official_result == None:
            return "No such official found!"
        return render_template('update_official.html', official = official_result)
    elif request.method == 'POST':
        id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        query = "UPDATE officials SET first_name = %s, last_name = %s WHERE id = %s"
        data = (fname, lname, id)
        result = execute_query(db_connection, query, data)
        return redirect('/browse_officials')

@webapp.route('/delete_official/<int:oid>')
def delete_official(oid):
	'''deletes the official with the given id'''
	db_connection = connect_to_database()
	query = "UPDATE tournaments SET official_id = NULL WHERE official_id = %s"
	data = (oid,)
	result = execute_query(db_connection, query, data)
	query = "DELETE FROM officials WHERE id = %s"
	result = execute_query(db_connection, query, data)
	return redirect('/browse_officials')

@webapp.route("/official_results/<int:oid>")
def officialResults(oid):
	db_connection = connect_to_database()
	official_query = "SELECT id, first_name, last_name FROM officials WHERE id = %s;"
	data = (oid,)
	official_result = execute_query(db_connection, official_query, data).fetchone();
	query =	'SELECT r.id, t.name, p.first_name, p.last_name, r.round_id, r.match_id, r.outcome, r.score FROM results r INNER JOIN  tournaments t ON r.tournament_id = t.id INNER JOIN players p ON p.id = r.player_id WHERE t.official_id = %s;'
	results = execute_query(db_connection, query, data)
	return render_template("official_results.html", rows=results, official=official_result)

@webapp.route("/delete_official_result/<int:oid>/<int:rid>")
def deleteOfficialResult(oid,rid):
	db_connection = connect_to_database()
	query = "DELETE FROM results WHERE id = %s;"
	data = (rid,)
	results = execute_query(db_connection, query, data)
	return redirect('/official_results/' + str(oid))

@webapp.route("/official_tournaments/<int:oid>")
def officialTournaments(oid):
	db_connection = connect_to_database()
	data = (oid,)
	official_query = "SELECT id, first_name, last_name FROM officials WHERE id = %s;"
	official_result = execute_query(db_connection, official_query, data).fetchone();
	tournament_query = "SELECT t.id, t.name, t.format, t.start_date, t.end_date FROM tournaments t INNER JOIN officials o ON t.official_id = o.id WHERE t.official_id = %s;"
	tournament_result = execute_query(db_connection, tournament_query, data).fetchall();
	return render_template("official_tournaments.html", rows=tournament_result, official=official_result)

@webapp.route('/add_official_tournament/<int:oid>', methods=["GET", "POST"])
def addOfficialTournament(oid):
	db_connection = connect_to_database()
	query = "SELECT id, first_name, last_name FROM officials WHERE id = %s;"
	data = (oid,)
	official = execute_query(db_connection, query, data).fetchone();
	if request.method == "POST":
		name = request.form["name"]
		t_format = request.form["format"]
		start_date = request.form["sd"]
		query = "INSERT INTO tournaments (name, format, start_date, official_id) VALUES (%s, %s, %s, %s);"
		data = (name, t_format, start_date, oid)
		execute_query(db_connection, query, data)
		return redirect('/official_tournaments/' + str(oid))
	return render_template("add_official_tournament.html", official = official)

''' Begin Tournament endpoints ---------------------------------------------------------------------'''
@webapp.route('/browse_tournaments')
def browse_tournaments():
	db_connection = connect_to_database()
	query = "SELECT t.id, t.name, t.format, t.start_date, t.end_date, o.first_name, o.last_name FROM tournaments t, officials o WHERE t.official_id = o.id UNION SELECT t.id, t.name, t.format, t.start_date, t.end_date, NULL, NULL FROM tournaments t WHERE t.official_id is NULL;"
	result = execute_query(db_connection, query).fetchall();
	return render_template('browse_tournaments.html', rows=result)

@webapp.route("/new_tournament", methods=["GET", "POST"])
def newTournament():
	db_connection = connect_to_database()
	query = "select first_name, last_name, id from officials;"
	officials = execute_query(db_connection, query)
	if request.method == "POST":
		query = "insert into tournaments (name, format, start_date, official_id) values (%s, %s, %s, %s);"
		name = request.form["name"]
		t_format = request.form["format"]
		start_date = request.form["sd"]
		official_id = request.form["Official"]
		data = (name, t_format, start_date, official_id)
		execute_query(db_connection, query, data)
		return redirect('/browse_tournaments')
	return render_template("new_tournament.html", officials = officials)

@webapp.route('/update_tournament/<int:tid>', methods=['POST','GET'])
def update_tournament(tid):
	db_connection = connect_to_database()
	#display existing data
	if request.method == 'GET':
		officials_query = "select first_name, last_name, id from officials;"
		officials_result = execute_query(db_connection, officials_query)
		tournament_query = 'SELECT id, name, official_id, format, start_date, end_date from tournaments WHERE id = %s'
		data = (tid,)
		tournament_result = execute_query(db_connection, tournament_query, data).fetchone()
		if tournament_result == None:
			return "No such tournament found!"
		return render_template('update_tournament.html', officials = officials_result, tourny = tournament_result)
	elif request.method == 'POST':
		id = request.form['id']
		name = request.form['name']
		official = request.form['official']
		format = request.form['format']
		start_date = request.form['sd']
		end_date = request.form['ed']
		query = "UPDATE tournaments SET name = %s, format = %s, official_id = %s, start_date = %s, end_date = %s WHERE id = %s"
		data = (name, format, official, start_date, end_date, id)
		result = execute_query(db_connection, query, data)
		return redirect('/browse_tournaments')

@webapp.route('/delete_tournament/<int:id>')
def delete_tournament(id):
	'''deletes the tournament with the given id'''
	db_connection = connect_to_database()
	querys = []
	querys.append("delete from results where tournament_id = %s")
	querys.append("delete from tournament_player where tid = %s")
	querys.append("DELETE FROM tournaments WHERE id = %s")
	data = (id,)
	for query in querys:
		result = execute_query(db_connection, query, data)
	return redirect('/browse_tournaments')

@webapp.route("/tournament_players/<int:tid>")
def tournamentPlayers(tid):
	db_connection = connect_to_database()
	tournament_query = "SELECT id, name FROM tournaments WHERE id = %s"
	data = (tid,)
	tournament_result = execute_query(db_connection, tournament_query, data).fetchone();
	query =	'SELECT p.id, p.first_name, p.last_name from players p INNER JOIN tournament_player tp on p.id = tp.pid INNER JOIN tournaments t on tp.tid = t.id where t.id = %s;'
	result = execute_query(db_connection, query, data)
	return render_template("tournament_players.html", rows=result, tournament=tournament_result)

@webapp.route("/add_tournament_player/<int:tid>", methods=["GET", "POST"])
def addTournamnetPlayer(tid):
	db_connection = connect_to_database()
	if request.method == "GET":
		players_query = "SELECT id, first_name, last_name FROM players;"
		players = execute_query(db_connection, players_query)
		tournament_query = "SELECT id, name FROM tournaments WHERE id = %s;"
		data = (tid,)
		tournament = execute_query(db_connection, tournament_query, data).fetchone();
		return render_template("add_tournament_player.html", players=players, tournament=tournament)
	else:
		pid = int(request.form["player"])
		query = "INSERT INTO tournament_player (tid, pid) VALUES (%s, %s)"
		data = (tid, pid)
		execute_query(db_connection, query, data)
		return redirect('/tournament_players/' + str(tid))

@webapp.route("/remove/<int:tid>/<int:pid>")
def remove_player_from_tournament(tid,pid):
		'''deletes connection of player to tournament by given ids'''
		db_connection = connect_to_database()
		query = "DELETE FROM tournament_player WHERE tid = %s AND pid = %s"
		data = (tid,pid)
		result = execute_query(db_connection, query, data)
		return redirect('/tournament_players/' + str(tid))

@webapp.route("/tournament_results/<int:tid>")
def tournamentResults(tid):
	db_connection = connect_to_database()
	tournament_query = "SELECT id, name FROM tournaments WHERE id = %s;"
	data = (tid,)
	tournament_result = execute_query(db_connection, tournament_query, data).fetchone();
	query =	'SELECT r.id, p.first_name, p.last_name, r.round_id, r.match_id, r.outcome, r.score, (SELECT o.first_name FROM officials o WHERE o.id = t.official_id), (SELECT o.last_name FROM officials o WHERE o.id = t.official_id) FROM results r INNER JOIN  tournaments t ON r.tournament_id = t.id INNER JOIN players p ON p.id = r.player_id WHERE r.tournament_id = %s;'
	results = execute_query(db_connection, query, data).fetchall();
	return render_template("tournament_results.html", rows=results, tournament=tournament_result)

@webapp.route("/delete_tournament_result/<int:tid>/<int:rid>")
def deleteTournamentResult(tid,rid):
	db_connection = connect_to_database()
	query = "DELETE FROM results WHERE id = %s;"
	data = (rid,)
	results = execute_query(db_connection, query, data)
	return redirect('/tournament_results/' + str(tid))

@webapp.route("/add_tournament_result/<int:tid>", methods=["GET","POST"])
def addTournamentResult(tid):
	db_connection = connect_to_database()
	if request.method =="GET":
		query = "SELECT id, first_name, last_name FROM players p INNER JOIN tournament_player tp ON p.id = tp.pid WHERE tp.tid = %s;"
		data = (tid,)
		players_result = execute_query(db_connection, query, data).fetchall();
		tournament_query = "SELECT id, name FROM tournaments WHERE id = %s;"
		tournament_result = execute_query(db_connection, tournament_query, data).fetchone();
		return render_template("add_tournament_result.html", players=players_result, tournament=tournament_result)
	else:
		pid = int(request.form["player"])
		roundid = int(request.form["round"])
		matchid = int(request.form["match"])
		result = request.form["result"]
		score = int(request.form["score"])
		query = "INSERT INTO results (tournament_id, player_id, round_id, match_id, outcome, score) values (%s, %s, %s, %s, %s, %s);"
		data = ( tid, pid, roundid, matchid, result, score)
		execute_query(db_connection, query, data)
		return redirect('/tournament_results/' + str(tid))

@webapp.route("/end_tournament/<int:tid>", methods=["GET", "POST"])
def endTournament(tid):
	db_connection = connect_to_database()
	if request.method == "GET":
		query = "SELECT id, name FROM tournaments WHERE id = %s AND end_date is null;"
		data = (tid,)
		tournament = execute_query(db_connection, query, data).fetchone();
		if tournament == None:
			return redirect('/browse_tournaments')
		return render_template("end_tournament.html", tournament = tournament)
	else:
		endDate = request.form["endDate"]
		query = "UPDATE tournaments SET end_date = %s WHERE id = %s;"
		data = (endDate, tid)
		execute_query(db_connection, query, data)
		return redirect('/browse_tournaments')
