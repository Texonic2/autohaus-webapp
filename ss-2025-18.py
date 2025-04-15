"""Webbasierte Systeme - Gruppe 18
"""
# Import benötigter Flask-Module
from flask import Flask, render_template, g, request
# Import MySQL-Connector
import mysql.connector

# Import der Verbindungsinformationen zur Datenbank:
# Variable DB_HOST: Servername des MySQL-Servers
# Variable DB_USER: Nutzername
# Variable DB_PASSWORD: Passwort
# Variable DB_DATABASE: Datenbankname
from db.db_credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

app = Flask(__name__)


@app.route


@app.before_request
def before_request():
    """ Verbindung zur Datenbank herstellen """
    g.con = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                                    database=DB_DATABASE)


@app.teardown_request
def teardown_request(exception):
    """ Verbindung zur Datenbank trennen """
    con = getattr(g, 'con', None)
    if con is not None:
        con.close()


@app.route('/')
def index():
    """Startseite"""
    return render_template('index.html')

@app.route('/enes')
def enes():
    return render_template('enes.html')

@app.route('/sipanweb')
def sipanweb():
    return render_template('sipanweb.html')

@app.route('/aliweb')
def aliweb():
    return render_template('aliweb.html')

@app.route('/benniweb')
def benniweb():
    return render_template('benniweb.html')


@app.route('/eingabeformular', methods=['GET', 'POST'])
def eingabeformular():
    if request.method == 'GET':
        return render_template('formular.html')
    elif request.method == 'POST':
        name = request.form['eingabe']
        passwort = request.form['passwort']
        return render_template('formular.html', name=name, password=passwort)

@app.route("/benniweb")
def benniweb():
    cursor = g.con.cursor()
    cursor.execute("SELECT id,name FROM bdavid")
    data= cursor.fetchall()
    cursor.close()
    return render_template("benniweb.html", data=data)


# Start der Flask-Anwendung
if __name__ == '__main__':
    app.run(debug=True)
