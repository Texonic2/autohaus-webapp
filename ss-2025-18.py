from flask import Flask, render_template, g, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename  #  Neu für Upload
import os  #  Neu für Upload

# Import der Verbindungsinformationen zur Datenbank
from db.db_credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

#  Flask-App erstellen (nur EINMAL!)
app = Flask(__name__)
app.secret_key = 'dein_geheimes_schluessel'  # Geheimen Schlüssel für Sessions setzen

#  Upload-Konfiguration
UPLOAD_FOLDER = os.path.join('static')  # Oder z.B. os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Speichert Upload-Ordner in der Config

#  Hilfsfunktion: Prüft, ob die Datei-Endung erlaubt ist
def allowed_file(filename):
    """
    Prüft, ob Dateiname eine erlaubte Bild-Endung hat.
    Beispiel: 'auto.jpg' ist erlaubt, 'auto.exe' NICHT erlaubt.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    # 1. Session-User-ID holen (None, falls nicht eingeloggt)
    user_id = session.get('user_id')

    # 2. Cursor mit dict-Output
    cursor = g.con.cursor(dictionary=True)

    # 3. Filterwerte aus dem GET-Request
    modell    = request.args.get('modell')
    max_preis = request.args.get('preis',    type=int)
    baujahr   = request.args.get('baujahr',  type=int)
    ps        = request.args.get('ps',       type=int)

    # 4. Dynamische SQL-Query bauen
    sql    = "SELECT * FROM auto WHERE marke = 'Mercedes'"
    params = []
    if modell:
        sql    += " AND modell LIKE %s"
        params.append(f"%{modell}%")
    if max_preis:
        sql    += " AND preis <= %s"
        params.append(max_preis)
    if baujahr:
        sql    += " AND baujahr >= %s"
        params.append(baujahr)
    if ps:
        sql    += " AND leistung >= %s"
        params.append(ps)

    # 5. Fahrzeuge abrufen
    cursor.execute(sql, params)
    fahrzeuge = cursor.fetchall()

    # 6. Favoriten-IDs des Users abrufen
    user_fav_ids = []
    if user_id:
        cursor.execute(
            "SELECT autoid FROM favorites WHERE user_id = %s",
            (user_id,)
        )
        user_fav_ids = [row['autoid'] for row in cursor.fetchall()]

    # 7. Template rendern – mit beiden Listen
    return render_template(
        "fahrzeugkatalog.html",
        fahrzeuge=fahrzeuge,
        user_fav_ids=user_fav_ids
    )

@app.route("/finanzierungbsp", methods=["GET", "POST"])
def finanzierungbsp():
    rate = None  # Ergebnis-Variable für die Monatsrate

    if request.method == "POST":
        try:
            #  Werte aus dem Formular auslesen und in richtige Typen umwandeln
            fahrzeugpreis = float(request.form["fahrzeugpreis"])
            anzahlung = float(request.form["anzahlung"])
            laufzeit = int(request.form["laufzeit"])
            schlussrate = float(request.form["schlussrate"])

            #  Plausibilitätsprüfungen (wie bei deiner Haupt-Route)
            if anzahlung < 0 or schlussrate < 0:
                rate = "Anzahlung oder Schlussrate dürfen nicht negativ sein."

            elif anzahlung > fahrzeugpreis:
                rate = "Anzahlung darf nicht höher sein als der Fahrzeugpreis."

            elif laufzeit <= 0 or laufzeit > 120:
                rate = "Laufzeit muss zwischen 1 und 120 Monaten liegen."

            elif (fahrzeugpreis - anzahlung - schlussrate) < 0:
                rate = "Kombination aus Anzahlung und Schlussrate ist zu hoch."

            else:
                #  ZINS = 0% → einfach Restbetrag durch Laufzeit teilen
                kreditbetrag = fahrzeugpreis - anzahlung - schlussrate
                rate = round(kreditbetrag / laufzeit, 2)

        except (ValueError, ZeroDivisionError):
            #  Fehler beim Umwandeln oder Division durch 0 → klare Meldung
            rate = "Eingabefehler"

    #  HTML-Seite mit Ergebnis anzeigen
    return render_template("finanzierungbsp.html", rate=rate)


@app.route('/finanzierung/<int:autoid>', methods=['GET', 'POST'])
def finanzierung(autoid):
    #  Prüfen, ob User eingeloggt ist
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    cursor = g.cursor

    #  Fahrzeug aus DB laden
    cursor.execute("SELECT * FROM auto WHERE autoid = %s", (autoid,))
    fahrzeug = cursor.fetchone()
    if not fahrzeug:
        return "Fahrzeug nicht gefunden", 404

    #  Variablen initialisieren
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

                #  PRÜFUNGEN
                if anzahlung < 0 or schlussrate < 0:
                    flash("Anzahlung oder Schlussrate dürfen nicht negativ sein.")
                elif anzahlung > fahrzeugpreis:
                    flash("Die Anzahlung darf nicht höher sein als der Fahrzeugpreis.")
                elif laufzeit <= 0 or laufzeit > 120:
                    flash("Die Laufzeit muss zwischen 1 und 120 Monaten liegen (max. 10 Jahre).")
                elif (fahrzeugpreis - anzahlung - schlussrate) < 0:
                    flash("Die Kombination aus Anzahlung und Schlussrate ist zu hoch.")

                else:
                    #  Berechnen nur wenn alles OK
                    kreditbetrag = fahrzeugpreis - anzahlung - schlussrate

                    # KEINE ZINSBERECHNUNG MEHR!
                    rate = round(kreditbetrag / laufzeit, 2)

            except Exception as e:
                print(f"Fehler bei Berechnung: {e}")
                rate = None

        elif aktion == "barzahlung":
            try:
                fahrzeugpreis = float(fahrzeug['preis'])
                anzahlung = 0
                laufzeit = 0
                schlussrate = fahrzeugpreis
                rate = 0  # Bei Barzahlung keine Rate

            except Exception as e:
                import traceback
                traceback.print_exc()
                return f"Fehler beim Barkauf: {e}", 500

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

                #  User-ID sicher aus Session holen & prüfen
                nutzer_id = session.get('user_id')
                if not nutzer_id:
                    return redirect(url_for('Login'))
                nutzer_id = int(nutzer_id)

                #  FK-Prüfung: Nutzer muss existieren
                cursor.execute("SELECT User_ID FROM users WHERE User_ID = %s", (nutzer_id,))
                check_user = cursor.fetchone()
                if not check_user:
                    return "Benutzer existiert nicht mehr — bitte erneut einloggen.", 400

                #  FK-Prüfung: Auto muss existieren
                cursor.execute("SELECT autoid FROM auto WHERE autoid = %s", (autoid,))
                check_auto = cursor.fetchone()
                if not check_auto:
                    return "Auto nicht gefunden.", 400

                info = "Barkauf" if laufzeit == 0 else "Finanzierungsanfrage"

                #  Anfrage speichern
                cursor.execute("""
                    INSERT INTO Finanzierungsanfrage 
                    (Nutzer_ID, Auto_ID, Monate, Anzahlung, Monatliche_Rate, Terminwunsch, Status, schlussrate, info)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nutzer_id, autoid, laufzeit, anzahlung, rate, terminwunsch, "angefragt", schlussrate, info))

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

    user_id = session['user_id']
    cursor = g.cursor

    #  Benutzerinfos laden
    cursor.execute("""
        SELECT vorname, nachname, email, role 
        FROM users 
        WHERE User_ID = %s
    """, (user_id,))
    benutzer = cursor.fetchone()

    #  Kaufverträge inkl. Auto-Details
    cursor.execute("""
        SELECT k.*, a.marke, a.modell, a.url, a.autoid, a.baujahr, a.leistung, a.preis, a.hubraum,
               a.kraftstoffverbrauch, a.getriebeart, a.antriebsart, a.umweltplakette
        FROM Kaufvertrag k
        JOIN auto a ON k.auto_id = a.autoid
        WHERE k.kunde_id = %s
        ORDER BY k.Datum_Erstellung DESC
    """, (user_id,))
    kaufvertraege = cursor.fetchall()

    #  Finanzierungsanfragen
    cursor.execute("""
        SELECT f.*, a.marke, a.modell, a.url 
        FROM Finanzierungsanfrage f
        JOIN auto a ON f.auto_id = a.autoid
        WHERE f.Nutzer_ID = %s
        ORDER BY f.erstellt_am DESC
    """, (user_id,))
    finanzierungsanfragen = cursor.fetchall()

    return render_template(
        'account.html',
        benutzer=benutzer,
        kaufvertraege=kaufvertraege,
        finanzierungsanfragen=finanzierungsanfragen
    )

@app.route("/passwort_aendern", methods=["GET", "POST"])
def passwort_aendern():
    # Zugriffsschutz: Nur eingeloggte Benutzer dürfen ihr Passwort ändern
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    cursor = g.cursor  # Cursor für DB-Zugriffe

    error = None
    success = None  # Platzhalter für Rückmeldungen im Template

    if request.method == "POST":
        # Eingaben aus dem Formular abholen
        altes = request.form.get("old_password")
        neues = request.form.get("new_password")
        bestaetigen = request.form.get("confirm_password")

        # Altes Passwort aus der Datenbank holen
        cursor.execute("SELECT passwort FROM users WHERE User_ID = %s", (user_id,))
        user = cursor.fetchone()

        # Prüfen, ob Benutzer gefunden wurde
        if not user:
            error = "Benutzer nicht gefunden."

        # Prüfen, ob das alte Passwort korrekt ist
        elif not check_password_hash(user['passwort'], altes):
            error = "Das alte Passwort ist falsch!"

        # Prüfen, ob die neuen Passwörter übereinstimmen
        elif neues != bestaetigen:
            error = "Die neuen Passwörter stimmen nicht überein."

        # Wenn alles korrekt ist: Passwort in DB aktualisieren
        else:
            neues_gehasht = generate_password_hash(neues)  # Hashing aus Sicherheitsgründen
            cursor.execute("UPDATE users SET passwort = %s WHERE User_ID = %s", (neues_gehasht, user_id))
            g.con.commit()
            success = "Passwort erfolgreich geändert."

    # Seite rendern – mit möglicher Fehlermeldung oder Erfolgsmeldung
    return render_template("passwort_aendern.html", error=error, success=success)

@app.route('/profil_aendern', methods=['GET', 'POST'])
def profil_aendern():
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    cursor = g.cursor

    success = None
    error = None

    if request.method == 'POST':
        vorname = request.form['vorname']
        nachname = request.form['nachname']
        email = request.form['email']

        try:
            cursor.execute("""
                UPDATE users
                SET vorname = %s, nachname = %s, email = %s
                WHERE User_ID = %s
            """, (vorname, nachname, email, user_id))
            g.con.commit()
            success = "Profil erfolgreich aktualisiert."
        except Exception as e:
            error = "Fehler beim Aktualisieren: " + str(e)

    cursor.execute("SELECT vorname, nachname, email FROM users WHERE User_ID = %s", (user_id,))
    user = cursor.fetchone()

    return render_template("profil_aendern.html", user=user, success=success, error=error)


@app.route('/')
def index():
    # Startseite der Website anzeigen
    # Rendert die HTML-Datei 'index.html' als Antwort auf einen GET-Request auf die Root-URL
    return render_template('index.html')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    error_message = None        # Variable zum Speichern von Fehlermeldungen

    if request.method == 'POST':
        # Benutzereingaben aus dem Login-Formular auslesen
        email = request.form['email']
        passwort = request.form['passwort']

        cursor = g.cursor
        # Benutzer mit der angegebenen E-Mail aus der Datenbank abrufen
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        # Überprüfen, ob Benutzer existiert
        if user is None:
            error_message = "Diese E-Mail-Adresse ist noch nicht registriert."
        # Passwort überprüfen (gehasht in DB)
        elif not check_password_hash(user['passwort'], passwort):
            error_message = "Das Passwort ist falsch. Bitte versuche es erneut."
        else:
            # Login erfolgreich, Benutzerdaten in der Session speichern
            session['user_id'] = user['User_ID']
            session['user_role'] = user['role']
            # Weiterleitung zur Startseite nach erfolgreichem Login
            return redirect(url_for('index'))
    # Rendern der Login-Seite mit evtl. Fehlermeldung
    return render_template('Login.html', error_message=error_message)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    error_message = None      # Variable für mögliche Fehlermeldungen

    if request.method == 'POST':
        # Benutzereingaben aus dem Registrierungsformular auslesen
        vorname = request.form['firstname']
        nachname = request.form['lastname']
        email = request.form['email']
        passwort = request.form['password']

        cursor = g.cursor
        # Prüfen, ob die E-Mail bereits registriert ist
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Fehlermeldung bei bereits registrierter E-Mail
            error_message = "E-Mail bereits registriert. Bitte benutze eine andere."
        else:
            # Standardrolle für neue Benutzer setzen
            rolle = 'customer'
            # Passwort sicher hashen
            hashed_password = generate_password_hash(passwort)

            # Neuen Benutzer in die Datenbank einfügen
            sql = "INSERT INTO users (vorname, nachname, email, passwort, role) VALUES (%s, %s, %s, %s, %s)"
            val = (vorname, nachname, email, hashed_password, rolle)
            cursor.execute(sql, val)
            g.con.commit()

            # Nach erfolgreicher Registrierung Weiterleitung zur Login-Seite
            return redirect(url_for('Login'))
        # Rendern der Registrierungsseite, ggf. mit Fehlermeldung
    return render_template('registration.html', error_message=error_message)

@app.route('/logout')
def logout():
    # Entfernt die Benutzer-ID aus der Session, um den Benutzer auszuloggen
    session.pop('user_id', None)
    # Entfernt die Benutzerrolle aus der Session
    session.pop('user_role', None)
    # Leitet den Benutzer zurück zur Startseite weiter
    return redirect(url_for('index'))

# Route für die Impressum-Seite
# Wenn der Benutzer die URL /impressum aufruft, wird die impressum.html-Seite angezeigt.
@app.route('/impressum')
def impressum():
    return render_template('impressum.html')


# Route für die Datenschutz-Seite
# Wenn der Benutzer die URL /Datenschutz aufruft, wird die datenschutz.html-Seite angezeigt.
@app.route('/Datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Liest den Query-Parameter "geloescht" aus, z.B. um Löschbestätigungen anzuzeigen
    geloescht = request.args.get("geloescht")
    # Überprüft, ob der Benutzer eingeloggt ist und die Rolle "admin" besitzt
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403   # Zugriff verweigert, wenn keine Admin-Rechte vorhanden

    cursor = g.cursor

    if request.method == "POST":
        # Liest die Aktion und die ID der Finanzierungsanfrage aus dem Formular aus
        aktion = request.form.get("aktion")
        anfrage_id = request.form.get("anfrage_id")

        # Führt die entsprechende Datenbankaktion je nach Aktionstyp aus
        if aktion == "ablehnen":
            cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'abgelehnt' WHERE ID = %s", (anfrage_id,))
        elif aktion == "annehmen":
            cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'angenommen' WHERE ID = %s", (anfrage_id,))
        elif aktion == "kaufvertrag":
            # Fügt einen Kaufvertrag für die Finanzierungsanfrage hinzu
            cursor.execute("INSERT INTO Kaufvertrag (Finanzierungs_ID, Datum_Erstellung, PDF_Pfad) VALUES (%s, NOW(), 'kaufvertrag.pdf')", (anfrage_id,))

        # Speichert die Änderungen in der Datenbank
        g.con.commit()

    # Holt alle Finanzierungsanfragen mit zugehörigen Auto- und Benutzerinformationen, sortiert nach Erstellungsdatum absteigend
    cursor.execute("""
        SELECT f.*, a.marke, a.modell, a.url, f.info, u.vorname, u.nachname, u.email
        FROM Finanzierungsanfrage f
        JOIN auto a ON f.Auto_ID = a.autoid
        JOIN users u ON f.Nutzer_ID = u.User_ID
        ORDER BY f.erstellt_am DESC
    """)
    anfragen = cursor.fetchall()

    # Rendert die Admin-Seite und übergibt die Anfragen und den optionalen Lösch-Parameter an das Template
    return render_template("admin.html", anfragen=anfragen, geloescht=geloescht)


# Route für Admin-Aktionen (z.B. Anfragen annehmen, ablehnen, Kaufvertrag erstellen)
# Diese Route akzeptiert nur POST-Anfragen
@app.route('/admin/action', methods=['POST']) # Enes Bülkü und Benjamin David
def admin_action():
    # Überprüfen, ob der Benutzer eingeloggt ist und die Rolle 'admin' hat
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Keine Berechtigung", 403  # Zugriff verweigert, wenn keine Adminrechte

    # Abfrage der übermittelten Formulardaten
    aktion = request.form.get('aktion')           # Welche Aktion soll ausgeführt werden?
    anfrage_id = request.form.get('anfrage_id')   # Auf welche Finanzierungsanfrage bezieht sich die Aktion?

    cursor = g.cursor  # Zugriff auf die Datenbank über das globale Cursor-Objekt

    # Überprüfung, ob eine Anfrage-ID übermittelt wurde
    if not anfrage_id:
        return "Anfrage-ID fehlt", 400  # Bad Request, wenn keine ID angegeben wurde

    # Verschiedene mögliche Aktionen je nach übermitteltem Formularwert
    if aktion == "ablehnen":
        # Setzt den Status der Anfrage auf 'abgelehnt'
        cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'abgelehnt' WHERE ID = %s", (anfrage_id,))
    elif aktion == "annehmen":
        # Setzt den Status der Anfrage auf 'genehmigt'
        cursor.execute("UPDATE Finanzierungsanfrage SET Status = 'genehmigt' WHERE ID = %s", (anfrage_id,))
    elif aktion == "kaufvertrag":
        # Prüfen, ob bereits ein Kaufvertrag für diese Anfrage existiert
        cursor.execute("SELECT * FROM Kaufvertrag WHERE Finanzierungs_ID = %s", (anfrage_id,))
        vorhandener_vertrag = cursor.fetchone()
        if not vorhandener_vertrag:
            # Wenn kein Vertrag vorhanden ist, wird ein neuer erstellt
            cursor.execute(
                "INSERT INTO Kaufvertrag (Finanzierungs_ID, Datum_Erstellung, PDF_Pfad) VALUES (%s, NOW(), 'kaufvertrag.pdf')",
                (anfrage_id,)
            )

    # Änderungen an der Datenbank dauerhaft speichern
    g.con.commit()

    # Zurückleitung zur Admin-Seite nach Ausführung der Aktion
    return redirect(url_for('admin'))


# Route für die Bewertungsseite (Reviews)
# Unterstützt sowohl GET- als auch POST-Anfragen
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    # Wenn ein Formular abgeschickt wurde (POST-Methode)
    if request.method == 'POST':
        user_id = session.get('user_id')      # ID des eingeloggten Nutzers aus der Session
        rating = request.form['rating']       # Bewertung (z.B. Sterne) aus dem Formular
        comment = request.form['comment']     # Kommentartext aus dem Formular

        cursor = g.cursor  # Zugriff auf den Datenbank-Cursor

        # Einfügen einer neuen Bewertung in die Datenbank
        cursor.execute("""
            INSERT INTO reviews (user_id, rating, comment) 
            VALUES (%s, %s, %s)
        """, (user_id, rating, comment))

        # Änderungen speichern
        g.con.commit()

        # Nach erfolgreichem Einfügen zur Bewertungsseite weiterleiten (um erneute POST-Anfragen bei Refresh zu vermeiden)
        return redirect(url_for('reviews'))

    # Wenn die Seite normal aufgerufen wird (GET-Methode)
    cursor = g.cursor

    # Alle Bewertungen aus der Datenbank abrufen, inkl. Vor- und Nachnamen des Nutzers
    cursor.execute("""
        SELECT r.*, u.vorname, u.nachname 
        FROM reviews r 
        LEFT JOIN users u ON r.user_id = u.User_ID
    """)

    reviews = cursor.fetchall()  # Alle Bewertungen als Liste von Einträgen holen

    # Die Bewertungen an das HTML-Template übergeben und anzeigen
    return render_template('reviews.html', reviews=reviews)


@app.route("/benutzer_verwalten", methods=["GET", "POST"])
def benutzer_verwalten():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403

    cursor = g.cursor

    if request.method == "POST":
        user_id = request.form.get("user_id")
        action = request.form.get("aktion")

        if action == "loeschen":
            cursor.execute("DELETE FROM Finanzierungsanfrage WHERE Nutzer_ID = %s", (user_id,))
            cursor.execute("DELETE FROM Kaufvertrag WHERE kunde_id = %s", (user_id,))
            cursor.execute("DELETE FROM favorites WHERE User_ID = %s", (user_id,))
            cursor.execute("DELETE FROM reviews WHERE user_id = %s", (user_id,))  #  korrekt!
            cursor.execute("DELETE FROM users WHERE User_ID = %s", (user_id,))
            g.con.commit()

        elif action == "daten_aendern":
            vorname = request.form.get("vorname")
            nachname = request.form.get("nachname")
            neue_rolle = request.form.get("rolle")

            cursor.execute("""
                UPDATE users
                SET vorname = %s, nachname = %s, role = %s
                WHERE User_ID = %s
            """, (vorname, nachname, neue_rolle, user_id))
            g.con.commit()

        return redirect(url_for('benutzer_verwalten'))

    # Benutzerliste anzeigen
    cursor.execute("SELECT * FROM users ORDER BY User_ID ASC")
    benutzerliste = cursor.fetchall()

    return render_template("admin/benutzer.html", benutzerliste=benutzerliste)


@app.route("/benutzer_anlegen", methods=["GET", "POST"])

def benutzer_anlegen():
    # Nur Admins dürfen Benutzer anlegen
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403

    if request.method == "POST":
        # Formulardaten auslesen
        vorname = request.form.get("vorname")
        nachname = request.form.get("nachname")
        email = request.form.get("email")
        passwort = request.form.get("passwort")
        rolle = request.form.get("rolle")

        # Passwort hashen für sichere Speicherung
        hashed_pw = generate_password_hash(passwort)

        cursor = g.cursor
        # Neuen Benutzer in Datenbank einfügen
        cursor.execute("INSERT INTO users (vorname, nachname, email, passwort, role) VALUES (%s, %s, %s, %s, %s)",
                       (vorname, nachname, email, hashed_pw, rolle))
        g.con.commit()

        # Nach dem Anlegen zurück zur Benutzerverwaltung
        return redirect(url_for('benutzer_verwalten'))

    # GET-Request: Formular zum Benutzer anlegen anzeigen
    return render_template("benutzer_anlegen.html")

@app.route('/anfrage_loeschen/<int:anfrage_id>', methods=['POST'])
def anfrage_loeschen(anfrage_id):
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    cursor = g.cursor

    # Nur löschen, wenn die Anfrage auch dem eingeloggten Nutzer gehört
    cursor.execute("DELETE FROM Finanzierungsanfrage WHERE ID = %s AND Nutzer_ID = %s", (anfrage_id, user_id))
    g.con.commit()

    return redirect(url_for('account'))

@app.route('/admin/anfrage_loeschen/<int:anfrage_id>', methods=['POST'])
def anfrage_loeschen_admin(anfrage_id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403

    cursor = g.cursor



    # 2. Finanzierungsanfrage löschen
    cursor.execute("DELETE FROM Finanzierungsanfrage WHERE ID = %s", (anfrage_id,))
    g.con.commit()

    return redirect(url_for('admin'))

@app.route('/admin/loesche_abgelehnte', methods=['POST'])
def loesche_abgelehnte_anfragen():
    cursor = g.cursor

    # Alle abgelehnten Anfragen direkt löschen
    cursor.execute("DELETE FROM Finanzierungsanfrage WHERE LOWER(Status) = 'abgelehnt'")
    anzahl = cursor.rowcount  # gibt Anzahl der gelöschten Zeilen zurück

    g.con.commit()
    return redirect(url_for('admin', geloescht=anzahl))

@app.route("/auto_verwalten")
def auto_verwalten():
    # Nur Admins dürfen auf diese Seite
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403

    cursor = g.cursor
    cursor.execute("""
        SELECT autoid, marke, modell, baujahr, leistung
        FROM auto
        ORDER BY autoid ASC
    """)
    autos = cursor.fetchall()

    return render_template("auto_verwalten.html", autos=autos)


@app.route('/auto_bearbeiten/<int:autoid>', methods=['GET', 'POST'])
def auto_bearbeiten(autoid):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403

    cursor = g.cursor

    if request.method == 'POST':
        daten = (
            request.form['marke'],
            request.form['modell'],
            request.form['baujahr'],
            request.form['leistung'],
            request.form['preis'],
            request.form['url'],
            request.form['kraftstoffverbrauch'],
            request.form['hubraum'],
            request.form['getriebeart'],
            request.form['antriebsart'],
            request.form['umweltplakette'],
            autoid
        )

        cursor.execute("""
            UPDATE auto SET
              marke = %s,
              modell = %s,
              baujahr = %s,
              leistung = %s,
              preis = %s,
              url = %s,
              kraftstoffverbrauch = %s,
              hubraum = %s,
              getriebeart = %s,
              antriebsart = %s,
              umweltplakette = %s
            WHERE autoid = %s
        """, daten)
        g.con.commit()
        return redirect(url_for('auto_verwalten'))

    # Auto-Daten laden
    cursor.execute("SELECT * FROM auto WHERE autoid = %s", (autoid,))
    auto = cursor.fetchone()

    if not auto:
        return "Fahrzeug nicht gefunden", 404

    return render_template("auto_bearbeiten.html", auto=auto)

@app.route('/auto_hinzufuegen', methods=['GET', 'POST'])
def auto_hinzufuegen():
    # Zugriff prüfen: Nur Admin darf Auto hinzufügen
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Zugriff verweigert", 403

    if request.method == 'POST':
        #  Formulardaten auslesen
        marke = request.form['marke']
        modell = request.form['modell']
        baujahr = request.form['baujahr']
        leistung = request.form['leistung']
        preis = request.form['preis']
        kraftstoffverbrauch = request.form['kraftstoffverbrauch']
        hubraum = request.form['hubraum']
        getriebeart = request.form['getriebeart']
        antriebsart = request.form['antriebsart']
        umweltplakette = request.form['umweltplakette']

        # Bilddatei verarbeiten
        if 'bilddatei' not in request.files:
            flash("Keine Bilddatei gefunden!")
            return redirect(request.url)

        file = request.files['bilddatei']

        if file.filename == '':
            flash("Keine Datei ausgewählt!")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Sicheren Dateinamen erstellen
            filename = secure_filename(file.filename)
            # Datei im static/ Ordner speichern
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash("Ungültiger Dateityp!")
            return redirect(request.url)

        #  ALLE Daten inkl. Bild-Dateiname in die DB eintragen
        daten = (
            marke,
            modell,
            baujahr,
            leistung,
            preis,
            filename,  # <- HIER kommt der Dateiname vom Bild
            kraftstoffverbrauch,
            hubraum,
            getriebeart,
            antriebsart,
            umweltplakette
        )

        cursor = g.cursor
        cursor.execute("""
            INSERT INTO auto 
            (marke, modell, baujahr, leistung, preis, url,
             kraftstoffverbrauch, hubraum, getriebeart, antriebsart, umweltplakette)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, daten)
        g.con.commit()

        flash("Fahrzeug erfolgreich hinzugefügt!")
        return redirect(url_for('auto_verwalten'))

    # GET: Formular anzeigen
    return render_template("auto_hinzufuegen.html")

@app.route('/auto_loeschen/<int:autoid>', methods=['POST'])
def auto_loeschen(autoid):
    try:
        cursor = g.cursor
        cursor.execute("DELETE FROM auto WHERE autoid = %s", (autoid,))
        g.con.commit()
    except Exception as e:
        # Optional: Logging oder Fehlerbehandlung
        pass
    return redirect(url_for('auto_verwalten'))


@app.route('/favorite/toggle/<int:autoid>', methods=['POST'])
def toggle_favorite(autoid):
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    cursor = g.con.cursor()

    #  Korrigierter Spaltenname: User_ID und autoid
    cursor.execute(
        "SELECT id FROM favorites WHERE User_ID = %s AND autoid = %s",
        (user_id, autoid)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "DELETE FROM favorites WHERE id = %s",
            (exists[0],)
        )
    else:
        cursor.execute(
            "INSERT INTO favorites (User_ID, autoid) VALUES (%s, %s)",
            (user_id, autoid)
        )

    g.con.commit()
    return redirect(request.referrer or url_for('fahrzeugkatalog'))


@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('Login'))

    user_id = session['user_id']
    cursor = g.con.cursor(dictionary=True)

    #  Korrekt: User_ID (nicht ID)
    cursor.execute("SELECT * FROM users WHERE User_ID = %s", (user_id,))
    benutzer = cursor.fetchone()

    cursor.execute("""
        SELECT a.*
        FROM favorites f
        JOIN auto a ON f.autoid = a.autoid
        WHERE f.User_ID = %s
        ORDER BY a.autoid DESC
    """, (user_id,))
    fahrzeuge = cursor.fetchall()

    return render_template('favorites.html', fahrzeuge=fahrzeuge, benutzer=benutzer)

@app.route('/admin/kaufvertrag_erstellen/<int:anfrage_id>', methods=['GET', 'POST'])
def kaufvertrag_erstellen(anfrage_id):
    autohaus_daten = {
        "name": "Nova Drive",
        "adresse": "Max-Planck-Straße 39, 74072 Heilbronn",
        "telefon": "07131 123456",
        "email": "NovaDrive@autohaus-heilbronn.de",
        "geschaeftsfuehrer": "LeBron James"
    }

    with g.con.cursor(dictionary=True, buffered=True) as cursor:
        # 1) Hole Anfrage + User + Auto + Finanzierungsdetails + Info
        cursor.execute("""
            SELECT fa.ID, fa.Info, fa.Terminwunsch, fa.Monate, fa.Anzahlung, fa.Monatliche_Rate, fa.schlussrate, fa.Status,
                   fa.Nutzer_ID AS kunde_id, fa.Auto_ID AS auto_id,
                   u.vorname, u.nachname, u.email,
                   a.marke, a.modell, a.url
            FROM Finanzierungsanfrage fa
            JOIN users u ON fa.Nutzer_ID = u.User_ID
            JOIN auto a ON fa.Auto_ID = a.autoid
            WHERE fa.ID = %s
        """, (anfrage_id,))
        daten = cursor.fetchone()

        if not daten:
            return "Anfrage nicht gefunden", 404

        #  Nur genehmigte Anfragen
        if daten['Status'] != 'genehmigt':
            flash("Kaufvertrag kann nur für genehmigte Anfragen erstellt werden.", "error")
            return redirect(url_for('admin'))

        if request.method == "POST":
            # Adresse und Telefon vom Formular holen
            kunde_adresse = request.form.get("adresse")
            kunde_telefon = request.form.get("telefon")

            try:

                cursor.execute("""
                    INSERT INTO Kaufvertrag 
                    (kunde_id, auto_id, Info, Monate, Anzahlung, Schlussrate, Monatliche_Rate, Datum_Erstellung, 
                    vorname, nachname, email, kunde_adresse, kunde_telefon)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s)
                    """, (
                    daten['kunde_id'],
                    daten['auto_id'],
                    daten['Info'],
                    daten['Monate'],
                    daten['Anzahlung'],
                    daten['schlussrate'],
                    daten['Monatliche_Rate'],
                    daten['vorname'],
                    daten['nachname'],
                    daten['email'],
                    kunde_adresse,
                    kunde_telefon,

                ))
                g.con.commit()

                cursor.execute("""
                    DELETE FROM Finanzierungsanfrage WHERE ID = %s
                """, (anfrage_id,))
                g.con.commit()

                flash("Kaufvertrag wurde erfolgreich gespeichert & Anfrage gelöscht!", "success")
                return redirect(url_for('kaufvertrag_erfolgreich', anfrage_id=anfrage_id))

            except Exception as e:
                return f"Fehler beim Speichern des Kaufvertrags: {e}", 500

        # GET → zeigt Vorschau an
        return render_template("kaufvertrag.html", kaufvertrag=daten, autohaus=autohaus_daten)

@app.route('/admin/kaufvertrag_erfolgreich/<int:anfrage_id>')
def kaufvertrag_erfolgreich(anfrage_id):
    # Optional: Admin-Check, wenn benötigt
    # if 'user_role' not in session or session['user_role'] != 'admin':
    #     return redirect(url_for('Login'))

    return render_template("kaufvertrag_erfolgreich.html", anfrage_id=anfrage_id)

@app.route('/kaufvertraege')
def kaufvertraege():
    cursor = g.cursor
    cursor.execute("""
        SELECT 
            k.Kaufvertrag_ID,
            k.Info,
            k.Monate,
            k.Anzahlung,
            k.Schlussrate,
            k.Monatliche_Rate,
            k.Datum_Erstellung,
            u.vorname, u.nachname, u.email,
            a.marke, a.modell, a.preis
        FROM Kaufvertrag k
        JOIN users u ON k.kunde_id = u.User_ID
        JOIN auto a ON k.auto_id = a.autoid
    """)
    vertraege = cursor.fetchall()
    return render_template("kaufvertraege.html", vertraege=vertraege)


# Route zum Löschen einer Bewertung
# Diese Route ist nur per POST-Methode erreichbar
@app.route('/delete_review', methods=['POST'])
def delete_review():
    # Überprüfen, ob der Nutzer eingeloggt ist und die Rolle 'admin' hat
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Keine Berechtigung", 403  # Zugriff verweigert bei fehlender Admin-Berechtigung

    # ID der zu löschenden Bewertung aus dem Formular holen
    review_id = request.form.get('review_id')

    # Sicherstellen, dass eine review_id übermittelt wurde
    if not review_id:
        return "Rezension-ID fehlt", 400  # Bad Request, wenn keine ID vorhanden ist

    cursor = g.cursor  # Datenbank-Cursor holen

    # Bewertung mit der übergebenen ID aus der Datenbank löschen
    cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
    g.con.commit()  # Änderungen speichern

    # Nach dem Löschen zurück zur Bewertungsseite
    return redirect(url_for('reviews'))



# Route zum Beantworten einer Bewertung durch einen Admin
# Diese Route ist nur per POST-Methode erreichbar
@app.route('/reply_to_review', methods=['POST'])
def reply_to_review():
    # Prüfen, ob der Nutzer eingeloggt ist und Adminrechte hat
    if 'user_role' not in session or session['user_role'] != 'admin':
        return "Keine Berechtigung", 403  # Zugriff verweigert, wenn kein Admin

    # Formularwerte abrufen: ID der Bewertung und die Admin-Antwort
    review_id = request.form.get('review_id')
    reply = request.form.get('admin_response')

    # Sicherstellen, dass beide Werte übermittelt wurden
    if not review_id or not reply:
        return "Fehlende Daten", 400  # Bad Request, wenn Daten fehlen

    cursor = g.cursor  # Datenbank-Cursor holen

    # Bewertung in der Datenbank aktualisieren: Antwort des Admins speichern
    cursor.execute("""
        UPDATE reviews 
        SET admin_response = %s 
        WHERE id = %s
    """, (reply, review_id))

    g.con.commit()  # Änderungen speichern

    # Zurückleitung zur Bewertungsseite nach dem Speichern der Antwort
    return redirect(url_for('reviews'))


# Route zum Erstellen einer Finanzierungs- oder Barkaufanfrage
@app.route("/anfrage_erstellen", methods=["GET", "POST"])  # Ali Yenil und Benjamin David
def anfrage_erstellen():
    cursor = g.cursor  # Datenbank-Cursor holen

    # Alle Autos aus der Datenbank abfragen
    cursor.execute("SELECT autoid, marke, modell, preis FROM auto")
    autos = cursor.fetchall()

    # Alle registrierten Benutzer (Kunden) abfragen
    cursor.execute("SELECT User_ID, email, vorname, nachname FROM users")
    kunden = cursor.fetchall()

    # Initialisierung der Variablen, die später im Template verwendet werden
    preis = None
    rate = None
    laufzeit = None
    anzahlung = None
    schlussrate = None
    fehler = None
    auto_id = None
    terminwunsch = None
    kaufart = request.form.get("kaufart")  # Barkauf oder Finanzierung

    # Wenn das Formular abgeschickt wurde
    if request.method == "POST":
        # Abfrage der Auto-ID und Preisermittlung
        auto_id_input = request.form.get("auto_id")
        if auto_id_input and auto_id_input.isdigit():
            auto_id = int(auto_id_input)
            cursor.execute("SELECT preis FROM auto WHERE autoid = %s", (auto_id,))
            result = cursor.fetchone()

            if result:
                preis = float(result['preis'])
            else:
                fehler = "Auto mit dieser ID wurde nicht gefunden."
        else:
            fehler = "Bitte gib eine gültige Auto-ID ein."

        # Weitere Eingabefelder aus dem Formular abrufen
        laufzeit_input = request.form.get("laufzeit")
        anzahlung_input = request.form.get("anzahlung")
        schlussrate_input = request.form.get("schlussrate")
        terminwunsch_input = request.form.get("terminwunsch")

        # Terminwunsch in ein datetime-Format umwandeln
        if terminwunsch_input:
            try:
                terminwunsch = terminwunsch_input.replace("T", " ") + ":00"
            except Exception:
                fehler = " Ungültiges Datumsformat beim Terminwunsch."

        # Berechnung der monatlichen Rate bei Finanzierungsanfrage
        try:
            if kaufart == "Finanzierungsanfrage":
                if preis and laufzeit_input and anzahlung_input and schlussrate_input:
                    laufzeit = int(laufzeit_input)
                    anzahlung = float(anzahlung_input)
                    schlussrate = float(schlussrate_input)

                    if laufzeit > 0:
                        finanzierungsbetrag = preis - anzahlung - schlussrate
                        zinsen = finanzierungsbetrag * 0.02  # 2 % Zinsen
                        rate = round((finanzierungsbetrag + zinsen) / laufzeit, 2)
                    else:
                        fehler = " Laufzeit muss größer als 0 sein."
                else:
                    fehler = " Bitte alle Finanzierungsfelder ausfüllen."
            else:
                # Barkauf – keine Rate nötig
                laufzeit = 0
                anzahlung = 0
                schlussrate = preis
                rate = 0.0
        except ValueError:
            fehler = " Ungültige Zahlen bei Laufzeit, Anzahlung oder Schlussrate."

        # Prüfung ob Kunde existiert, anhand der E-Mail-Adresse
        email = request.form.get("email")
        if not fehler and preis and email and terminwunsch:
            cursor.execute("SELECT User_ID FROM users WHERE email = %s", (email,))
            kunde = cursor.fetchone()

            if not kunde:
                fehler = " Kunde nicht gefunden. Bitte Kundenkonto erstellen."
            else:
                benutzer_id = kunde['User_ID']
                try:
                    # Eintrag der Anfrage in die Datenbank
                    cursor.execute("""
                        INSERT INTO Finanzierungsanfrage 
                        (Nutzer_ID, Auto_ID, Monate, Anzahlung, Schlussrate, Monatliche_Rate, Terminwunsch, Status, erstellt_am, info)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'angefragt', NOW(), %s)
                    """, (
                        benutzer_id,
                        auto_id,
                        laufzeit,
                        anzahlung,
                        schlussrate,
                        rate,
                        terminwunsch,
                        kaufart
                    ))
                    g.con.commit()  # Änderungen speichern
                    return redirect(url_for("admin"))  # Weiterleitung zur Admin-Seite
                except Exception as e:
                    fehler = f" Fehler beim Speichern: {e}"

    # Rendern des Anfrageformulars mit allen benötigten Variablen
    return render_template("anfrage_erstellen.html",
        autos=autos,
        preis=preis,
        rate=rate,
        laufzeit=laufzeit,
        anzahlung=anzahlung,
        schlussrate=schlussrate,
        fehler=fehler,
        auto_id=auto_id,
        kaufart=kaufart,
        kunden=kunden
    )


@app.route('/kaufvertraege')
def kaufvertraege_anzeigen():
    cursor = g.cursor
    cursor.execute("""
        SELECT 
            k.Kaufvertrag_ID,
            k.Finanzierungs_ID,
            k.Datum_Erstellung,
            k.kunde_vorname,
            k.kunde_nachname,
            k.kunde_email,
            k.kunde_adresse,
            k.kunde_telefon
        FROM Kaufvertrag k
        ORDER BY k.Datum_Erstellung DESC
    """)

    kaufvertraege = cursor.fetchall()
    return render_template('kaufvertraege.html', kaufvertraege=kaufvertraege)

@app.route('/kaufvertrag_loeschen/<int:vertrag_id>', methods=['POST'])
def kaufvertrag_loeschen(vertrag_id):
    cursor = g.cursor
    cursor.execute("DELETE FROM Kaufvertrag WHERE Kaufvertrag_ID = %s", (vertrag_id,))
    g.con.commit()
    return redirect(url_for('kaufvertraege_anzeigen'))

@app.route('/unternehmenszahlen')
def unternehmenszahlen():
    cursor = g.cursor

    #  Gesamtanzahl Kaufverträge
    cursor.execute("SELECT COUNT(*) as anzahl FROM Kaufvertrag")
    anzahl_vertraege = cursor.fetchone()['anzahl'] or 0

    # Barkauf-Umsatz basierend auf Kaufverträgen
    cursor.execute("""
        SELECT SUM(a.preis) AS barkauf_umsatz
        FROM Kaufvertrag k
        JOIN auto a ON k.auto_id = a.autoid
        WHERE LOWER(k.Info) = 'barkauf'
    """)
    barkauf_umsatz = cursor.fetchone()['barkauf_umsatz'] or 0

    # Finanzierung-Umsatz basierend auf Kaufverträgen
    cursor.execute("""
        SELECT SUM(a.preis) AS finanzierungs_umsatz
        FROM Kaufvertrag k
        JOIN auto a ON k.auto_id = a.autoid
        WHERE LOWER(k.Info) = 'finanzierungsanfrage'
    """)
    finanzierungs_umsatz = cursor.fetchone()['finanzierungs_umsatz'] or 0

    #  Gesamtumsatz
    gesamtumsatz = barkauf_umsatz + finanzierungs_umsatz

    #  Kreditbetrag nur aus Kaufverträgen (Preis - Anzahlung - Schlussrate)
    cursor.execute("""
        SELECT SUM(a.preis - k.Anzahlung - k.Schlussrate) AS kreditbetrag
        FROM Kaufvertrag k
        JOIN auto a ON k.auto_id = a.autoid
        WHERE LOWER(k.Info) = 'finanzierungsanfrage'
    """)
    kredit_summe = cursor.fetchone()['kreditbetrag'] or 0
    kreditanteil_prozent = round((kredit_summe / gesamtumsatz) * 100, 2) if gesamtumsatz else 0

    #  Durchschnittliche Laufzeit nur aus Kaufverträgen
    cursor.execute("""
        SELECT AVG(k.Monate) AS avg_laufzeit
        FROM Kaufvertrag k
        WHERE LOWER(k.Info) = 'finanzierungsanfrage'
    """)
    durchschnitt_laufzeit = round(cursor.fetchone()['avg_laufzeit'] or 0)

    # Anzahl registrierte Kunden
    cursor.execute("SELECT COUNT(*) AS kunden FROM users WHERE LOWER(role) = 'customer'")
    kundenanzahl = cursor.fetchone()['kunden'] or 0

    #  Barkauf vs. Finanzierung basierend auf Kaufverträgen
    cursor.execute("SELECT COUNT(*) AS barkaeufe FROM Kaufvertrag WHERE LOWER(Info) = 'barkauf'")
    barkaeufe = cursor.fetchone()['barkaeufe'] or 0
    finanzierungen = anzahl_vertraege - barkaeufe
    barkauf_anteil = round((barkaeufe / anzahl_vertraege) * 100, 2) if anzahl_vertraege else 0
    finanzierungs_anteil = 100 - barkauf_anteil

    #  Offene Anfragen (bleibt bei Finanzierungsanfrage)
    cursor.execute("SELECT COUNT(*) AS offen FROM Finanzierungsanfrage WHERE LOWER(Status) = 'angefragt'")
    offene_anfragen = cursor.fetchone()['offen'] or 0

    #  Annahmequote (immer noch bei Finanzierungsanfrage)
    cursor.execute("SELECT COUNT(*) AS angenommen FROM Finanzierungsanfrage WHERE LOWER(Status) = 'angenommen'")
    angenommen = cursor.fetchone()['angenommen'] or 0
    # Gesamt Anfragen immer aus Anfragen-Tabelle

    cursor.execute("SELECT COUNT(*) AS gesamt FROM Finanzierungsanfrage")
    gesamt_anfragen = cursor.fetchone()['gesamt'] or 1
    annahmequote = round((angenommen / gesamt_anfragen) * 100, 2)

    return render_template(
        "unternehmenszahlen.html",
        gesamtumsatz=gesamtumsatz,
        barkauf_umsatz=barkauf_umsatz,
        finanzierungs_umsatz=finanzierungs_umsatz,
        kreditanteil_prozent=kreditanteil_prozent,
        durchschnitt_laufzeit=durchschnitt_laufzeit,
        anzahl_vertraege=anzahl_vertraege,
        kundenanzahl=kundenanzahl,
        offene_anfragen=offene_anfragen,
        annahmequote=annahmequote,
        barkauf_anteil=barkauf_anteil,
        finanzierungs_anteil=finanzierungs_anteil,
        gesamt_anfragen=gesamt_anfragen
    )




if __name__ == '__main__':
    app.run(debug=True)