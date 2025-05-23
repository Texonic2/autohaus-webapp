from flask import Flask, render_template, g, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Import der Verbindungsinformationen zur Datenbank
from db.db_credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

app = Flask(__name__)
app.secret_key = 'dein_geheimes_schluessel'  # Geheimen Schlüssel für Sessions setzen

@app.before_request
def before_request():
    """ Verbindung zur Datenbank herstellen und Cursor öffnen """
    g.con = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                                    database=DB_DATABASE)
    g.cursor = g.con.cursor(dictionary=True)

@app.teardown_request
def teardown_request(exception):
    """ Cursor und Verbindung zur Datenbank trennen """
    cursor = getattr(g, 'cursor', None)
    if cursor is not None:
        cursor.close()
    con = getattr(g, 'con', None)
    if con is not None:
        con.close()

@app.route('/fahrzeugkatalog')
def fahrzeugkatalog():
    cursor = g.cursor
    cursor.execute("SELECT * FROM auto")
    fahrzeuge = cursor.fetchall()
    app.logger.debug(f"Gefundene Autos: {fahrzeuge!r}")
    return render_template("fahrzeugkatalog.html", fahrzeuge=fahrzeuge)

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
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    cursor = g.cursor

    # Fahrzeugdaten laden (nur für Anzeige)
    cursor.execute("SELECT * FROM auto WHERE autoid = %s", (autoid,))
    fahrzeug = cursor.fetchone()
    if not fahrzeug:
        return "Fahrzeug nicht gefunden", 404

    rate = None
    fahrzeugpreis = None
    anzahlung = None
    laufzeit = None
    schlussrate = None

    if request.method == "POST":
        aktion = request.form.get('aktion')

        if aktion == "berechnen":
            try:
                fahrzeugpreis = float(request.form['fahrzeugpreis'])
                anzahlung = float(request.form['anzahlung'])
                laufzeit = int(request.form['laufzeit'])
                schlussrate_raw = request.form.get('schlussrate', '').strip()
                schlussrate = float(schlussrate_raw) if schlussrate_raw else 0.0

                kreditbetrag = fahrzeugpreis - anzahlung - schlussrate
                zins = 0.02  # 2%
                rate = round((kreditbetrag * (1 + zins)) / laufzeit, 2)

            except Exception:
                rate = None  # Fehler bei Eingabe ignorieren

        elif aktion == "barzahlung":
            # Hier ggf. Logik für Barzahlung
            return redirect(url_for('index'))

        elif aktion == "termin":
            try:
                fahrzeugpreis = float(request.form['fahrzeugpreis'])
                anzahlung = float(request.form['anzahlung'])
                laufzeit = int(request.form['laufzeit'])
                schlussrate_raw = request.form.get('schlussrate', '').strip()
                schlussrate = float(schlussrate_raw) if schlussrate_raw else 0.0

                rate_raw = request.form.get('rate', '0').strip()
                rate = float(rate_raw) if rate_raw else 0.0

                termin_datum = request.form['termin']
                termin_uhrzeit = request.form['uhrzeit']
                terminwunsch = f"{termin_datum} {termin_uhrzeit}"

                nutzer_id = session.get('user_id')
                if not nutzer_id:
                    return redirect(url_for('Login'))

                cursor.execute(
                    """INSERT INTO Finanzierungsanfrage 
                       (Auto_ID, Anzahlung, Monate, Monatliche_Rate, Terminwunsch, Status, Schlussrate, Nutzer_ID) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (autoid, anzahlung, laufzeit, rate, terminwunsch, "angefragt", schlussrate, nutzer_id)
                )
                g.con.commit()

                return redirect(url_for('index'))

            except Exception as e:
                import traceback
                traceback.print_exc()
                return f"Fehler beim Speichern des Termins: {e}", 500

    return render_template(
        "finanzierung.html",
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

    # Kein automatisches Redirect mehr für Admins!
    # Admins und Kunden sehen hier ihre eigene Finanzierungsanfragen.

    user_id = session['user_id']
    cursor = g.cursor

    cursor.execute("""
        SELECT f.*, a.marke, a.modell, a.url, a.autoid AS ID, f.monatliche_rate, f.schlussrate
        FROM Finanzierungsanfrage f
        JOIN auto a ON f.Auto_ID = a.autoid
        WHERE f.Nutzer_ID = %s
        ORDER BY f.erstellt_am DESC
    """, (user_id,))
    anfragen = cursor.fetchall()

    return render_template('account.html', finanzierungsanfragen=anfragen)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        passwort = request.form['passwort']

        cursor = g.cursor
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            error_message = "Diese E-Mail-Adresse ist noch nicht registriert."
        elif not check_password_hash(user['passwort'], passwort):
            error_message = "Das Passwort ist falsch. Bitte versuche es erneut."
        else:
            session['user_id'] = user['User_ID']

            # Rollenlogik: Admin, wenn @novadrive.hn
            if email.endswith('@novadrive.hn'):
                session['user_role'] = 'admin'
            else:
                session['user_role'] = 'customer'

            return redirect(url_for('index'))

    return render_template('Login.html', error_message=error_message)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    error_message = None

    if request.method == 'POST':
        vorname = request.form['firstname']
        nachname = request.form['lastname']
        email = request.form['email']
        passwort = request.form['password']

        cursor = g.cursor

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "E-Mail bereits registriert. Bitte benutze eine andere."
        else:
            rolle = 'admin' if email.endswith('@novadrive.hn') else 'customer'
            hashed_password = generate_password_hash(passwort)

            sql = "INSERT INTO users (vorname, nachname, email, passwort, role) VALUES (%s, %s, %s, %s, %s)"
            val = (vorname, nachname, email, hashed_password, rolle)
            cursor.execute(sql, val)
            g.con.commit()

            return redirect(url_for('Login'))

    return render_template('registration.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    return redirect(url_for('index'))

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

    cursor = g.cursor

    if request.method == "POST":
        aktion = request.form.get("aktion")
        anfrage_id = request.form.get("anfrage_id")

        if aktion == "ablehnen":
            cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'abgelehnt' WHERE ID = %s", (anfrage_id,))
        elif aktion == "annehmen":
            cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'angenommen' WHERE ID = %s", (anfrage_id,))
        elif aktion == "kaufvertrag":
            cursor.execute("INSERT INTO Kaufvertrag (Finanzierungs_ID, Datum_Erstellung, PDF_Pfad) VALUES (%s, NOW(), 'kaufvertrag.pdf')", (anfrage_id,))

        g.con.commit()

    cursor.execute("""
        SELECT f.*, a.marke, a.modell, a.url, u.vorname, u.nachname, u.email
        FROM Finanzierungsanfrage f
        JOIN auto a ON f.Auto_ID = a.autoid
        JOIN users u ON f.Nutzer_ID = u.User_ID
        ORDER BY f.erstellt_am DESC
    """)
    anfragen = cursor.fetchall()

    return render_template("admin.html", anfragen=anfragen)

@app.route('/admin/action', methods=['POST'])
def admin_action():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Keine Berechtigung", 403

    aktion = request.form.get('aktion')
    anfrage_id = request.form.get('anfrage_id')

    cursor = g.cursor

    if not anfrage_id:
        return "Anfrage-ID fehlt", 400

    if aktion == "ablehnen":
        cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'abgelehnt' WHERE ID = %s", (anfrage_id,))
    elif aktion == "annehmen":
        cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'genehmigt' WHERE ID = %s", (anfrage_id,))
    elif aktion == "kaufvertrag":
        # Optional: prüfen, ob Kaufvertrag für die Anfrage schon existiert, um Duplikate zu vermeiden
        cursor.execute("SELECT * FROM Kaufvertrag WHERE Finanzierungs_ID = %s", (anfrage_id,))
        vorhandener_vertrag = cursor.fetchone()
        if not vorhandener_vertrag:
            cursor.execute("INSERT INTO Kaufvertrag (Finanzierungs_ID, Datum_Erstellung, PDF_Pfad) VALUES (%s, NOW(), 'kaufvertrag.pdf')", (anfrage_id,))

    g.con.commit()

    return redirect(url_for('admin'))

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        user_id = session.get('user_id')
        rating = request.form['rating']
        comment = request.form['comment']

        cursor = g.cursor
        cursor.execute("""
            INSERT INTO reviews (user_id, rating, comment) 
            VALUES (%s, %s, %s)
        """, (user_id, rating, comment))
        g.con.commit()

        return redirect(url_for('reviews'))

    cursor = g.cursor
    cursor.execute("SELECT r.*, u.vorname, u.nachname FROM reviews r LEFT JOIN users u ON r.user_id = u.User_ID")
    reviews = cursor.fetchall()

    return render_template('reviews.html', reviews=reviews)

@app.route('/termine')
def termine_anzeigen():
    cursor = g.cursor
    cursor.execute("SELECT fa.*, a.marke, a.modell FROM finanzierungsanfrage fa JOIN auto a ON fa.Auto_ID = a.autoid ORDER BY fa.Terminwunsch DESC")
    termine = cursor.fetchall()
    return render_template('termine.html', termine=termine)


if __name__ == '__main__':
    app.run(debug=True)
