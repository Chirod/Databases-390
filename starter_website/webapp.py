from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
import sys
#create the web application
webapp = Flask(__name__)

@webapp.route('/')
def index():
	return render_template("index.html")

@webapp.route('/browse_players')
def browse_players():
	print("Fetching and rendering players web page")
	db_connection = connect_to_database()
	query = "SELECT id, first_name, last_name from players;"
	result = execute_query(db_connection, query).fetchall();
	print(result)
	return render_template('browse_players.html', rows=result)

@webapp.route("/add_player_to_db", methods=["GET", "POST"])
def addPlayer():
	if request.method == "POST":
		print("add new player!")
		db_connection = connect_to_database()
		query = "insert into players (first_name,last_name) values (%s,%s);"
		fname = request.form['fname']
		lname = request.form['lname']
		data = (fname, lname)
		execute_query(db_connection, query, data)
		return redirect('/browse_players')
	else:
		return render_template("add_player_to_db.html")

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
        print("Update Player!");
        id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']

        print(request.form);

        query = "UPDATE players SET first_name = %s, last_name = %s WHERE id = %s"
        data = (fname, lname, id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated");

        return redirect('/browse_players')

@webapp.route('/delete_player/<int:id>')
def delete_player(id):
	'''deletes the player with the given id'''
	db_connection = connect_to_database()
	query = "DELETE FROM players WHERE id = %s"
	data = (id,)

	result = execute_query(db_connection, query, data)
	print(str(result.rowcount) + " row deleted");
	return redirect('/browse_players')

@webapp.route("/add_player_to_tournament.html", methods=["GET", "POST"])
def addPlayerToTournament():
	db_connection = connect_to_database()
	query = "select first_name, last_name, id from players;"
	players = execute_query(db_connection, query)
	query = "select name, id from tournaments;"
	tournaments = execute_query(db_connection, query)
	if request.method == "POST":
		print(request.form)
		player = int(request.form["player"])
		tournament = int(request.form["tournament"])
		query = "insert into tournament_player (tid, pid) values (%s, %s)"
		data = (tournament, player)
		execute_query(db_connection, query, data)
	return render_template("add_player_to_tournament.html", players=players, tournaments=tournaments)

@webapp.route("/add_result_to_tournament.html", methods=["GET","POST"])
def addesult():
	db_connection = connect_to_database()
	query = "select first_name, last_name, id from players;"
	players = execute_query(db_connection, query)
	query = "select name, id from tournaments;"
	tournaments = execute_query(db_connection, query)
	if request.method == "POST":
		print(request.form)
		player = int(request.form["player"])
		tournament = int(request.form["tournament"])
		roundid = int(request.form["round"])
		is_win = request.form["win"]
		score = int(request.form["score"])
		query = "insert into results (tournament_id, round_id, player_id, outcome, score) values (%s, %s, %s, %s, %s);"
		data = (tournament, roundid, player, is_win, score)
		print(data)
		execute_query(db_connection, query, data)
	return render_template("add_result_to_tournament.html", players=players, tournaments=tournaments)

@webapp.route("/add_tournament.html", methods=["GET", "POST"])
def addTournament():
	db_connection = connect_to_database()
	query = "select first_name, last_name, id from officials;"
	officials = execute_query(db_connection, query)
	if request.method == "POST":
		query = "insert into tournaments (name, format, start_date, official_id) values (%s, %s, %s, %s);"
		print(request.form)
		name = request.form["name"]
		t_format = request.form["format"]
		start_date = request.form["sd"]
		official_id = request.form["Official"]
		data = (name, t_format, start_date, official_id)
		print(data)
		execute_query(db_connection, query, data)
	return render_template("add_tournament.html", officials = officials)

@webapp.route("/end_tournament.html", methods=["GET", "POST"])
def endTournament():
	db_connection = connect_to_database()
	query = "select name from tournaments;"
	tournaments = execute_query(db_connection, query)
	if request.method == "POST":
		query = " update tournaments set end_date = %s where name = %s;"
		print(request.form)
		name = request.form["Tournament"]
		date = request.form["sd"]
		data = (date, name)
		print(data)
		execute_query(db_connection, query, data)
	return render_template("end_tournament.html", tournaments = tournaments)

@webapp.route("/player_results.html", methods=["GET","POST"])
def playerResults():
	db_connection = connect_to_database()
	query = "select first_name, last_name, id from players;"
	players = execute_query(db_connection, query)
	if request.method == "POST":
		pname = int(request.form['player'])
		query =	'select outcome, score from results where player_id = %s;'
		data = (pname,)
		result = execute_query(db_connection, query, data)
		return render_template("player_results.html", results=result, players=players)
	return render_template("player_results.html", players=players)

@webapp.route("/players_for_tournament.html", methods=["GET", "POST"])
def playersFortournament():
	db_connection = connect_to_database()
	query = "select name from tournaments"
	tourns = execute_query(db_connection, query)
	print(request)
	if request.method == "POST":
		tname = request.form['tournament']
		print(tname, "tname")
		query =	'select P.first_name, P.last_name from players P inner join tournament_player TP on P.id = TP.pid inner join tournaments T on TP.tid = T.id where T.name = %s;'
		data = (tname,)
		result = execute_query(db_connection, query, data)
		return render_template("players_for_tournament.html", rows=result, tournaments=tourns)
	elif request.method == "GET":
		return render_template("players_for_tournament.html", tournaments=tourns)


@webapp.route("/tournament_results.html")
def tournamentResults():
	return render_template("tournament_results.html")

@webapp.route("/tournament_for_player.html")
def tournamentForPlayer():
	return render_template("tournament_for_player.html")

@webapp.route('/browse_officials')
def browse_officials():
	print("Fetching and rendering officals web page")
	db_connection = connect_to_database()
	query = "SELECT id, first_name, last_name from officials;"
	result = execute_query(db_connection, query).fetchall();
	print(result)
	return render_template('browse_officials.html', rows=result)

@webapp.route("/add_official", methods=["GET", "POST"])
def addOfficial():
	if request.method == "POST":
		db_connection = connect_to_database()
		query = "insert into officials (first_name,last_name) values (%s,%s);"
		fname = request.form['fname']
		lname = request.form['lname']
		data = (fname, lname)
		execute_query(db_connection, query, data)
		return redirect('/browse_officials')
	else:
		return render_template("add_official.html")

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
        print("Update Official!");
        id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']

        print(request.form);

        query = "UPDATE officials SET first_name = %s, last_name = %s WHERE id = %s"
        data = (fname, lname, id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated");

        return redirect('/browse_officials')

@webapp.route('/delete_official/<int:id>')
def delete_official(id):
	'''deletes the official with the given id'''
	db_connection = connect_to_database()
	query = "DELETE FROM officials WHERE id = %s"
	data = (id,)

	result = execute_query(db_connection, query, data)
	print(str(result.rowcount) + " row deleted");
	return redirect('/browse_officials')
