# NovaDrive – Autohaus Webanwendung (Flask, SQL, HTML/CSS)

NovaDrive ist eine vollständige Webanwendung zur Verwaltung von Fahrzeugen, Nutzern und Finanzierungsanfragen.  
Das Projekt wurde im Rahmen eines Softwareentwicklungsmoduls an der Hochschule Heilbronn umgesetzt und bildet
einen realistischen End-to-End-Prozess ab — von Nutzerregistrierung über Fahrzeugverwaltung bis hin zu
Finanzierungsanfragen mit Rollen- und Session-Management.

---

##  Hauptfunktionen

- **Nutzerregistrierung & Login** (mit Passwort-Hashing & Session-Management)  
- **Rollenverwaltung** (User / Admin)  
- **Admin-Dashboard** für Nutzer- und Fahrzeugverwaltung  
- **Fahrzeugkatalog** mit Bildern  
- **Bild-Upload inkl. Dateitypprüfung**  
- **Finanzierungsanfragen** mit Validierung  
- **Profilverwaltung & Passwortänderung**  
- **CRUD-Funktionen** (Create, Read, Update, Delete)  
- **Responsive HTML-Templates mit Jinja2**  
- **Sichere Datenbankanbindung (MySQL/MariaDB)**  

---

##  Tech-Stack

**Backend:**  
- Python  
- Flask  
- Werkzeug Security (Hashing, Sessions)  

**Database:**  
- MySQL / MariaDB  
- SQL Schema & Queries  

**Frontend:**  
- HTML  
- CSS  
- Jinja2 Templates  

**Tools & DevOps:**  
- Git  
- PyCharm  
- Virtual Environments  

---

##  Projektstruktur

- `db/` – SQL-Schema & DB-Credentials (lokal)
- `templates/` – Jinja2 HTML-Templates
- `static/` – CSS, Bilder
- `ss-2025-18.py` – Haupt-Flask-App
- `README.md` – Projektdoku


---

##  Meine persönlichen Beiträge (Sipan Dölek)

Folgende Bereiche des Projekts habe ich eigenständig umgesetzt bzw. signifikant mitgestaltet:

### Backend / Flask
- Login- & Registrierungslogik  
- Session-Management  
- Passwort-Hashing  
- Routing & Request Handling  
- Fahrzeug-CRUD Funktionen  
- Profiländerungen (Profil bearbeiten, Passwort ändern)

###  Datenbank
- SQL-Abfragen  
- Tabellenlogik verstehen & integrieren  
- Schnittstelle zwischen Flask und MySQL einrichten  

###  Frontend / Templates
- Gestaltung & Anpassung mehrerer HTML-Templates  
- Responsive Layouts  
- Einbindung von Formularen & Fehler-Feedback (Flash Messages)

###  Allgemein
- Debugging  
- Code-Cleanup  
- Verbesserung der Struktur & Dokumentation  

---

---

##  Installation & Start

Voraussetzungen:  
- Python 3.x  
- MySQL/MariaDB  

### 1. Abhängigkeiten installieren
pip install -r requirements.txt

### 2. Datenbank einrichten
- MySQL/MariaDB starten
- Datei `db/db_schema.sql` in eine neue Datenbank importieren



### 3. Anwendung starten

python ss-2025-18.py


Die Anwendung läuft dann unter:
http://localhost:5000


---

##  Projektstatus
Abgeschlossen (Hochschulprojekt), dient als Demonstration praktischer Webentwicklung mit Flask und SQL.

---

##  Lizenz
GNU GPLv3  


