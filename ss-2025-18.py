"""Webbasierte Systeme - Gruppe 18
"""
from calendar import error

# Import benötigter Flask-Module
from flask import Flask, render_template, g, request, redirect, url_for
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

@app.route('/fahrzeugkatalog')
def fahrzeugkatalog():
    return render_template('fahrzeugkatalog.html')



# Route für die Finanzierungsseite – erlaubt GET (anzeigen) und POST (berechnen)
@app.route('/finanzierung', methods=['GET', 'POST'])
def finanzierung():
    rate = None  # Standard: Noch keine Rate berechnet

    # Wenn das Formular abgeschickt wurde (POST-Methode)
    if request.method == 'POST':
        # Werte aus dem Formular auslesen und konvertieren
        fahrzeugpreis = float(request.form['fahrzeugpreis'])  # z. B. 30.000 €
        anzahlung = float(request.form['anzahlung'])          # z. B. 5.000 €
        laufzeit = int(request.form['laufzeit'])              # z. B. 36 Monate
        schlussrate = float(request.form.get('schlussrate', 0))  # z. B. 3.000 €, optional

        # Finanzierungssumme berechnen
        finanzierungsbetrag = fahrzeugpreis - anzahlung - schlussrate

        # Fester Zinssatz: 2 % auf den Finanzierungsbetrag
        zins = 0.02
        gesamtbetrag = finanzierungsbetrag + (finanzierungsbetrag * zins)

        # Monatliche Rate = Gesamtbetrag / Laufzeit
        rate = round(gesamtbetrag / laufzeit, 2)

    # HTML-Template anzeigen und ggf. berechnete Rate übergeben
    return render_template('finanzierung.html', rate=rate)

# Flask-Anwendung starten, nur wenn direkt ausgeführt
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

# Start der Flask-Anwendung
if __name__ == '__main__':
    app.run(debug=True)

