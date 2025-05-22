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
        return redirect(url_for('Login'))

    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboar'))

    # Falls kein Admin → reguläre Konto-Seite laden
    user_id = session['user_id']
    cursor = g.con.cursor(dictionary=True)

    cursor.execute("""
        SELECT f.*, a.marke, a.modell, a.url
        FROM Finanzierungsanfrage f
        JOIN auto a ON f.Auto_ID = a.autoid
        WHERE f.Nutzer_ID = %s
        ORDER BY f.erstellt_am DESC
    """, (user_id,))
    anfragen = cursor.fetchall()

    return render_template('account.html', anfragen=anfragen)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        passwort = request.form['passwort']

        cursor = g.con.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            error_message = "Diese E-Mail-Adresse ist noch nicht registriert."
        elif not check_password_hash(user[4], passwort):  # user[4] = passwort
            error_message = "Das Passwort ist falsch. Bitte versuche es erneut."
        else:
            session['user_id'] = user[0]

            # Rollenlogik: Admin, wenn @novadrive.hn
            if email.endswith('@novadrive.hn'):
                session['user_role'] = 'admin'
            else:
                session['user_role'] = 'customer'

            return redirect(url_for('index'))

    return render_template('Login.html', error_message=error_message)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    error_message = None  # Für Fehlermeldungen

    if request.method == 'POST':
        # Formulardaten holen
        vorname = request.form['firstname']
        nachname = request.form['lastname']
        email = request.form['email']
        passwort = request.form['password']

        cursor = g.con.cursor()

        # Prüfen, ob E-Mail bereits registriert ist
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "E-Mail bereits registriert. Bitte benutze eine andere."
        else:
            # Automatisch Rolle zuweisen: admin, wenn @novadrive.hn
            rolle = 'admin' if email.endswith('@novadrive.hn') else 'customer'

            # Passwort hashen
            hashed_password = generate_password_hash(passwort)

            # Nutzer in Datenbank einfügen
            sql = "INSERT INTO users (vorname, nachname, email, passwort, role) VALUES (%s, %s, %s, %s, %s)"
            val = (vorname, nachname, email, hashed_password, rolle)
            cursor.execute(sql, val)
            g.con.commit()

            return redirect(url_for('Login'))  # Weiterleitung nach erfolgreicher Registrierung

    # Seite rendern (inkl. evtl. Fehlermeldung)
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

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403

    cursor = g.con.cursor(dictionary=True)

    if request.method == "POST":
        aktion = request.form.get("aktion")
        anfrage_id = request.form.get("anfrage_id")

        if aktion == "ablehnen":
            cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'abgelehnt' WHERE ID = %s", (anfrage_id,))
        elif aktion == "annehmen":
            cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'angenommen' WHERE ID = %s", (anfrage_id,))
        elif aktion == "kaufvertrag":
            # Beispielhafte Einfügung, kann erweitert werden
            cursor.execute("INSERT INTO Kaufvertrag (Finanzierungs_ID, Datum_Erstellung, PDF_Pfad) VALUES (%s, NOW(), 'kaufvertrag.pdf')", (anfrage_id,))

        g.con.commit()

    # Admin soll ALLE Anfragen sehen
    cursor.execute("""
        SELECT f.*, a.marke, a.modell, a.url
        FROM Finanzierungsanfrage f
        JOIN auto a ON f.Auto_ID = a.autoid
        ORDER BY f.ID DESC
    """)
    anfragen = cursor.fetchall()

    return render_template("admin.html", anfragen=anfragen)

@app.route('/admin/action', methods=['POST'])
def admin_action():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Keine Berechtigung", 403

    aktion = request.form.get('aktion')
    if aktion == "ablehnen":
        # Logik zum Ablehnen
        pass
    elif aktion == "annehmen":
        # Logik zum Annehmen
        pass
    elif aktion == "kaufvertrag":
        # Logik zum Kaufvertrag erstellen
        pass

    return redirect(url_for('admin'))  # z.B. zurück zum Adminbereich

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        # Rezension speichern
        user_id = session.get('user_id')  # Falls User-Login vorhanden
        rating = request.form['rating']
        comment = request.form['comment']

        cursor = g.con.cursor()
        cursor.execute("""
            INSERT INTO reviews (user_id, rating, comment) 
            VALUES (%s, %s, %s)
        """, (user_id, rating, comment))
        g.con.commit()

        return redirect(url_for('reviews'))

    # Alle Rezensionen abrufen
    cursor = g.con.cursor(dictionary=True)
    cursor.execute("SELECT r.*, u.vorname, u.nachname FROM reviews r LEFT JOIN users u ON r.user_id = u.User_ID")
    reviews = cursor.fetchall()

    return render_template('reviews.html', reviews=reviews)


# Start der Flask-Anwendung
if __name__ == '__main__':
    app.run(debug=True)