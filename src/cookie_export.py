import sqlite3
import os
from secret import firefox_profile_path

cookies_db = os.path.join(firefox_profile_path, "cookies.sqlite")


try:
    # Verbindung zur SQLite-Datenbank herstellen
    verbindung = sqlite3.connect(cookies_db)
    cursor = verbindung.cursor()

    # Alle Cookies abfragen, die "indeed" im Hostnamen enthalten
    cursor.execute("SELECT host, name, value FROM moz_cookies WHERE host LIKE '%indeed%'")

    # Ergebnisse in einer Variablen speichern
    cookies = cursor.fetchall()

    # Ergebnisse in eine Textdatei speichern
    datei = open("cookies_secret.py", "w+", encoding="utf-8")

    datei.write("'''\n") 
    for host, name, value in cookies:
        #print(f"Host: {host}, Cookie-Name: {name}, Cookie-Wert: {value}")
        datei.write(f"Host: {host}, Cookie-Name: {name}, Cookie-Wert: {value}\n")
    datei.write("'''") 

except sqlite3.DatabaseError as e:
    print(f"Datenbankfehler: {e}")

except OSError as e:
    print(f"Dateifehler: {e}")

except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")

else:
    print("Vorgang war erfolgreich.")

finally:
    # Sicherstellen, dass die Verbindung geschlossen wird, falls sie geöffnet wurde
    #print(dir())
    if 'verbindung' in locals():
        verbindung.close()
    if 'datei' in locals():
        datei.close()
