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



@app.route('/enes')
def enes():
    cursor = g.con.cursor()
    cursor.execute("SELECT ID, Name FROM ebuelkue WHERE Name='Enes'; ")
    data = cursor.fetchall()
    cursor.close()
    return render_template('enes.html', data=data)

@app.route('/sipanweb')
def sipanweb():
    cursor = g.con.cursor()
    cursor.execute("SELECT ID, Name FROM sdoelek WHERE Name='Sipan'; ")
    data = cursor.fetchall()
    cursor.close()
    return render_template('sipanweb.html', data=data)

@app.route('/aliweb')
def aliweb():
    cursor = g.con.cursor()
    cursor.execute("SELECT ID, Name FROM ayenil WHERE Name='Ali'; ")
    data = cursor.fetchall()
    cursor.close()
    return render_template('aliweb.html', data=data)

@app.route('/benniweb')
def benniweb():
    cursor = g.con.cursor()
    cursor.execute("SELECT ID, Name FROM sdoelek WHERE Name='benni'; ")
    data = cursor.fetchall()
    cursor.close()
    return render_template('benniweb.html', data=data)



@app.route('/neu')
def neu():
    return render_template('neu.html')

@app.route('/fahrzeugkatalog')
def fahrzeugkatalog():
    return render_template('fahrzeugkatalog.html')

@app.route('/finanzierung')
def finanzierung():
    return render_template('finanzierung.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/')
def index():
    return render_template('index.html')


# Start der Flask-Anwendung
if __name__ == '__main__':
    app.run(debug=True)

