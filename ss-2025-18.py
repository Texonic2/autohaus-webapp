from flask import Flask, render_template, g, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Import der Verbindungsinformationen zur Datenbank
from db.db_credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

app = Flask(__name__)
app.secret_key = 'dein_geheimes_schluessel'  # Geheimen Schlüssel für Sessions setzen

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

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('Login'))  # Wenn der Benutzer nicht eingeloggt ist, zum Login weiterleiten
    return render_template('account.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']   # E-Mail aus dem Formular
        passwort = request.form['passwort']  # Passwort aus dem Formular

        cursor = g.con.cursor()

        # SQL-Abfrage, um nach einem Benutzer mit der angegebenen E-Mail zu suchen
        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        cursor.execute(sql, val)
        user = cursor.fetchone()

        # Überprüfen, ob der Benutzer existiert und das Passwort korrekt ist
        if user and check_password_hash(user[4], passwort):  # assuming password is at index 4
            session['user_id'] = user[0]  # user[0] ist die ID des Benutzers
            return redirect(url_for('index'))  # Nach dem Login zur Homepage weiterleiten
        else:
            return "Benutzername oder Passwort falsch. Bitte versuche es erneut."

    return render_template('Login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Daten aus dem Formular
        vorname = request.form['firstname']
        nachname = request.form['lastname']
        email = request.form['email']
        passwort = request.form['password']

        cursor = g.con.cursor()

        # SQL-Abfrage zur Überprüfung, ob die E-Mail schon existiert
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "E-Mail bereits registriert. Bitte benutze eine andere E-Mail."

        # Passwort vor dem Speichern in der DB hashen
        hashed_password = generate_password_hash(passwort)

        # SQL-Abfrage zum Einfügen eines neuen Benutzers
        sql = "INSERT INTO users (vorname, nachname, email, passwort) VALUES (%s, %s, %s, %s)"
        val = (vorname, nachname, email, hashed_password)  # Gehashtes Passwort hier einfügen
        cursor.execute(sql, val)
        g.con.commit()

        return redirect(url_for('Login'))  # Nach der Registrierung zum Login weiterleiten

    return render_template('registration.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Entfernt die ID aus der Session, sodass der Benutzer ausgeloggt wird
    return redirect(url_for('index'))  # Weiterleitung zur Homepage

# Start der Flask-Anwendung
if __name__ == '__main__':
    app.run(debug=True)
