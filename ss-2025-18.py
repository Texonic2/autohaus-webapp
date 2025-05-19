from flask import Flask, render_template, g, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Import der Verbindungsinformationen zur Datenbank
from db.db_credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

app = Flask(__name__)
app.secret_key = 'dein_geheimes_schluessel'  # Geheimen Schlüssel für Sessions setzen

from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Zugriff nur für Administratoren.")
            return redirect(url_for("Login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin") #Admin Dashboard
@admin_required
def admin_dashboard():
    return render_template("admin/dashboard.html")

@app.route("/admin/users") #Benutzerliste
@admin_required
def user_list():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()
    cursor.execute("SELECT User_ID, vorname, nachname, email, role FROM users")
    users = cursor.fetchall()
    db.close()
    return render_template("admin/user_list.html", users=users)

@app.route("/admin/users/delete/<int:user_id>") #Benutzer löschen
@admin_required
def delete_user(user_id):
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE User_ID = %s", (user_id,))
    db.commit()
    db.close()
    return redirect(url_for("user_list"))

@app.route("/admin/autos")
@admin_required
def auto_list():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM auto")
    autos = cursor.fetchall()
    db.close()
    return render_template("admin/auto_list.html", autos=autos)

@app.route("/admin/autos/delete/<int:autoid>")
@admin_required
def delete_auto(autoid):
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()
    cursor.execute("DELETE FROM auto WHERE autoid = %s", (autoid,))
    db.commit()
    db.close()
    return redirect(url_for("auto_list"))

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
    cursor = g.con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM auto")
    fahrzeuge = cursor.fetchall()
    return render_template('fahrzeugkatalog.html', fahrzeuge=fahrzeuge)



@app.route("/finanzierungbsp", methods=["GET", "POST"])
def finanzierungbsp():
    rate = None

    if request.method == "POST":
        try:
            fahrzeugpreis = float(request.form["fahrzeugpreis"])
            anzahlung = float(request.form["anzahlung"])
            laufzeit = int(request.form["laufzeit"])
            schlussrate = float(request.form["schlussrate"])

            # Effektivzins: 2 % jährlich → monatlich:
            zinssatz = 0.02 / 12
            kreditbetrag = fahrzeugpreis - anzahlung - schlussrate

            if laufzeit > 0 and kreditbetrag > 0:
                rate = kreditbetrag * zinssatz / (1 - (1 + zinssatz) ** -laufzeit)
                rate = round(rate, 2)
            else:
                rate = "Ungültige Eingaben"

        except (ValueError, ZeroDivisionError):
            rate = "Eingabefehler"

    return render_template("finanzierungbsp.html", rate=rate)

@app.route('/finanzierung/<int:autoid>', methods=['GET', 'POST'])
def finanzierung(autoid):
    cursor = g.con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM auto WHERE autoid = %s", (autoid,))
    fahrzeug = cursor.fetchone()
    aktion = request.form.get("aktion")

    if not fahrzeug:
        return "Fahrzeug nicht gefunden", 404

    # Standardwerte
    rate = None
    fahrzeugpreis = None
    anzahlung = None
    laufzeit = None
    schlussrate = None

    if aktion == "berechnen":
        fahrzeugpreis = float(request.form['fahrzeugpreis'])
        anzahlung = float(request.form['anzahlung'])
        laufzeit = int(request.form['laufzeit'])
        schlussrate = float(request.form.get('schlussrate', 0))

        finanzierungsbetrag = fahrzeugpreis - anzahlung - schlussrate
        zins = 0.02
        gesamtbetrag = finanzierungsbetrag + (finanzierungsbetrag * zins)
        rate = round(gesamtbetrag / laufzeit, 2)

        # Speichern in der Session
        session['finanzierung'] = {
            'autoid': autoid,
            'fahrzeugpreis': fahrzeugpreis,
            'anzahlung': anzahlung,
            'laufzeit': laufzeit,
            'schlussrate': schlussrate,
            'rate': rate
        }
    elif aktion == "barzahlung":
        fahrzeugpreis = float(request.form['fahrzeugpreis'])
        anzahlung = 0
        laufzeit = 0
        schlussrate = 0
        rate= fahrzeugpreis


    elif aktion == "termin":
        fahrzeugpreis = float(request.form['fahrzeugpreis'])
        anzahlung = float(request.form['anzahlung'])
        laufzeit = int(request.form['laufzeit'])
        schlussrate = float(request.form.get('schlussrate', 0))
        rate = float(request.form['rate'])
        terminwunsch = f"{request.form['termin']} {request.form['uhrzeit']}"

        cursor.execute(
            "INSERT INTO finanzierungsanfrage (Auto_ID, Anzahlung, Monate, Monatliche_Rate, Terminwunsch, Status) VALUES (%s, %s, %s, %s, %s, %s)",
            (autoid, anzahlung, laufzeit, rate, terminwunsch, "offen")
        )
        g.con.commit()
        return redirect(url_for('danke'))

    return render_template(
        'finanzierung.html',
        fahrzeug=fahrzeug,
        rate=rate,

        fahrzeugpreis=fahrzeugpreis,
        anzahlung=anzahlung,
        laufzeit=laufzeit,
        schlussrate=schlussrate
    )

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
    error_message = None  # Hier wird die Fehlermeldung gesetzt, falls eine auftaucht.

    if request.method == 'POST':
        email = request.form['email']  # E-Mail aus dem Formular
        passwort = request.form['passwort']  # Passwort aus dem Formular

        cursor = g.con.cursor()

        # SQL-Abfrage, um nach einem Benutzer mit der angegebenen E-Mail zu suchen
        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        cursor.execute(sql, val)
        user = cursor.fetchone()

        if user is None:
            error_message = "Diese E-Mail-Adresse ist noch nicht registriert."  # Fehler bei nicht existierender E-Mail
        elif not check_password_hash(user[4], passwort):  # assuming password is at index 4
            error_message = "Das Passwort ist falsch. Bitte versuche es erneut."  # Fehler bei falschem Passwort
        else:
            session['user_id'] = user[0]  # user[0] ist die ID des Benutzers
            if user[5] == "admin":  # user[5] ist die Spalte "role"
                session['role'] = "admin"
                return redirect(url_for('admin_dashboard'))
            else:
                session['role'] = "customer"
                return redirect(url_for('index'))

    return render_template('Login.html', error_message=error_message)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    error_message = None  # Variable für die Fehlermeldung

    if request.method == 'POST':
        # Formulardaten
        vorname = request.form['firstname']
        nachname = request.form['lastname']
        email = request.form['email']
        passwort = request.form['password']

        cursor = g.con.cursor()

        # Überprüfen, ob die E-Mail bereits in der Datenbank existiert
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Falls die E-Mail schon existiert, Fehlermeldung setzen
            error_message = "E-Mail bereits registriert. Bitte benutze eine andere E-Mail."
        else:
            # Falls die E-Mail nicht existiert, Benutzer registrieren
            hashed_password = generate_password_hash(passwort)
            sql = "INSERT INTO users (vorname, nachname, email, passwort) VALUES (%s, %s, %s, %s)"
            val = (vorname, nachname, email, hashed_password)
            cursor.execute(sql, val)
            g.con.commit()
            return redirect(url_for('Login'))  # Weiterleitung nach erfolgreicher Registrierung

    # Die Fehlermeldung an das Template übergeben, wenn die E-Mail bereits existiert
    return render_template('registration.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Entfernt die ID aus der Session, sodass der Benutzer ausgeloggt wird
    return redirect(url_for('index'))  # Weiterleitung zur Homepage



@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/Datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

# Start der Flask-Anwendung
if __name__ == '__main__':
    app.run(debug=True)