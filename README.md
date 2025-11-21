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
## Screenshots (Auszug)
1. Admin-Dashboard – Finanzierungsanfragen <img width="1848" height="997" alt="Screenshot (49)" src="https://github.com/user-attachments/assets/0aa10c39-ae96-42f1-bf3c-00d16ec61ae7" />


Zeigt die komplette Backend-Logik mit Nutzerverwaltung, Fahrzeugdaten, Finanzierungsstatus, Workflow-Buttons (Annehmen / Ablehnen / Kaufvertrag).

2. Startseite / Landing Page <img width="1882" height="1002" alt="Screenshot 2025-11-21 150736" src="https://github.com/user-attachments/assets/645e680d-f9de-48af-97d1-59c58e2f9971" />


Modernes responsives UI, Navigationsleiste, Hero-Image – zeigt deine Frontend-Fähigkeiten.

3. Login-Seite <img width="1185" height="925" alt="Screenshot 2025-11-21 150749" src="https://github.com/user-attachments/assets/ca3421eb-911d-4680-b8dd-4cd6dd422fe0" />


Implementierte Authentifizierung mit Passwort-Hashing, Session-Management und Validierung.

4. Kennzahlen-Dashboard (KPIs) <img width="1890" height="1001" alt="Screenshot 2025-11-21 151000" src="https://github.com/user-attachments/assets/d0fd2806-da52-46b2-abe0-d48822a83374" />


Berechnung und Visualisierung interner KPIs: Kaufverträge, Anfragen, Barkauf-Quote, Finanzierungs-Quote.

5. Code-Ausschnitt (Flask Backend) <img width="1858" height="1074" alt="Screenshot 2025-11-21 151655" src="https://github.com/user-attachments/assets/d1ab38cb-a82c-4c40-b150-3c15cfd22b29" />


Zeigt die Passwort-Änderungslogik, SQL-Queries, Session-Handling und Sicherheitskonzepte.

6. Datenbank-Modell (ERD) <img width="1831" height="992" alt="Screenshot 2025-11-21 151957" src="https://github.com/user-attachments/assets/a4c8a32c-80ee-4b55-bdba-1163fd2edd6f" />


Relationale Modellierung mit Verknüpfungen zwischen Users, Autos, Anfragen, Kaufverträgen, Favorites und Reviews.
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


