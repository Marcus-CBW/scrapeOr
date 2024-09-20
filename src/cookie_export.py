import sqlite3
import os
from secret import firefox_profile_path

cookies_db = os.path.join(firefox_profile_path, "cookies.sqlite")

# Verbindung zur SQLite-Datenbank herstellen
connection = sqlite3.connect(cookies_db)
cursor = connection.cursor()

# Alle Cookies abfragen, die "indeed" im Hostnamen enthalten
cursor.execute("SELECT host, name, value FROM moz_cookies WHERE host LIKE '%indeed%'")

# Ergebnisse in einer Variablen speichern
cookies = cursor.fetchall()

# Ergebnisse in eine Textdatei speichern
with open("cookies_output.txt", "w+", encoding="utf-8") as file:
    for host, name, value in cookies:
        file.write(f"Host: {host}, Cookie-Name: {name}, Cookie-Wert: {value}\n")

# # Ergebnisse in der Konsole ausgeben
# for host, name, value in cookies:
#     print(f"Host: {host}, Cookie-Name: {name}, Cookie-Wert: {value}")

# # Verbindung schließen
# connection.close()

print("Datei 'cookies_output.txt' wurde erfolgreich erstellt.")
