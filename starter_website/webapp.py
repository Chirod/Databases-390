from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
import sys
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
	return "Hello World!";

@webapp.route('/browse_bsg_people')
#the name of this function is just a cosmetic thing
def browse_people():
	print("Fetching and rendering people web page")
	db_connection = connect_to_database()
	query = "SELECT fname, lname, homeworld, age, character_id from bsg_people;"
	result = execute_query(db_connection, query).fetchall();
	print(result)
	return render_template('people_browse.html', rows=result)

@webapp.route('/add_new_people', methods=['POST','GET'])
def add_new_people():
	db_connection = connect_to_database()
	if request.method == 'GET':
		query = 'SELECT planet_id, name from bsg_planets'
		result = execute_query(db_connection, query).fetchall();
		print(result)
		return render_template('people_add_new.html', planets = result)
	elif request.method == 'POST':
		print("Add new people!");
		fname = request.form['fname']
		lname = request.form['lname']
		age = request.form['age']
		homeworld = request.form['homeworld']
		query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
		data = (fname, lname, age, homeworld)
		execute_query(db_connection, query, data)
		return ('Person added!');

@webapp.route('/')
def index():
	return render_template("index.html")

@webapp.route("/add_player_to_db.html")
def addPlayer():
	return render_template("add_player_to_db.html")

@webapp.route("/add_official.html")
def addOfficial():
	return render_template("add_official.html")

@webapp.route("/add_player_to_tournament.html")
def addPlayerToTournament():
	return render_template("add_player_to_tournament.html")

@webapp.route("/add_result_to_tournament.html")
def addesult():
	return render_template("add_result_to_tournament.html")

@webapp.route("/add_tournament.html")
def addTournament():
	return render_template("add_tournament.html")

@webapp.route("/end_tournament.html")
def endTournament():
	return render_template("end_tournament.html")

@webapp.route("/player_results.html")
def playerResults():
	return render_template("player_results.html")

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

@webapp.route('/db-test')
def test_database_connection():
	print("Executing a sample query on the database using the credentials from db_credentials.py")
	db_connection = connect_to_database()
	query = "SELECT * from bsg_people;"
	result = execute_query(db_connection, query);
	return render_template('db_test.html', rows=result)

#display update form and process any updates, using the same function
@webapp.route('/update_people/<int:id>', methods=['POST','GET'])
def update_people(id):
	db_connection = connect_to_database()
	#display existing data
	if request.method == 'GET':
		people_query = 'SELECT character_id, fname, lname, homeworld, age from bsg_people WHERE character_id = %s' % (id)
		people_result = execute_query(db_connection, people_query).fetchone()

		if people_result == None:
			return "No such person found!"

		planets_query = 'SELECT planet_id, name from bsg_planets'
		planets_results = execute_query(db_connection, planets_query).fetchall();

		return render_template('people_update.html', planets = planets_results, person = people_result)
	elif request.method == 'POST':
		print("Update people!");
		character_id = request.form['character_id']
		fname = request.form['fname']
		lname = request.form['lname']
		age = request.form['age']
		homeworld = request.form['homeworld']

		print(request.form);

		query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
		data = (fname, lname, age, homeworld, character_id)
		result = execute_query(db_connection, query, data)
		print(str(result.rowcount) + " row(s) updated");

		return redirect('/browse_bsg_people')

@webapp.route('/delete_people/<int:id>')
def delete_people(id):
	'''deletes a person with the given id'''
	db_connection = connect_to_database()
	query = "DELETE FROM bsg_people WHERE character_id = %s"
	data = (id,)

	result = execute_query(db_connection, query, data)
	return (str(result.rowcount) + "row deleted")
