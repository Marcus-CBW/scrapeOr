
# scrapeOr - Web Scraping Projekt mit Scrapy

## Übersicht

**scrapeOr** ist ein Web Scraping-Projekt, das mit dem Python-Framework **Scrapy** entwickelt wurde. Dieses Projekt ermöglicht das Extrahieren von Daten aus einer oder mehreren Webseiten und deren Speicherung in verschiedenen Formaten wie JSON, CSV oder einer Datenbank. Das Hauptziel dieses Projekts ist es, automatisch strukturierte Daten von Webseiten zu sammeln, zu analysieren und zu speichern.

## Voraussetzungen

Bevor Sie das Projekt starten, stellen Sie sicher, dass folgende Voraussetzungen erfüllt sind:

- Python 3.x installiert
- Virtuelle Umgebung (empfohlen)
- Scrapy (wird über `requirements.txt` installiert)

## Installation

1. **Repository klonen**:


   git clone https://github.com/Marcus-CBW/scrapeOr.git
   cd ScrapeOr


2. **Virtuelle Umgebung erstellen** (optional, aber empfohlen):

 
   python -m venv venv
   source venv/bin/activate  # Für Linux/MacOS
   venv\Scripts\activate      # Für Windows


3. **Abhängigkeiten installieren**:

   Alle notwendigen Pakete befinden sich in der Datei `requirements.txt`. Installieren Sie sie mit:


   pip install -r requirements.txt


## Verwendung

1. **Spider ausführen**:

   Nach der Installation der Abhängigkeiten können Sie den Scrapy-Spider wie folgt starten:


   scrapy crawl spider_name


   Ersetzen Sie `spider_name` durch den Namen des zu verwendenden Spiders, der in der Datei `spiders/` definiert ist.

2. **Daten speichern**:

   Sie können die gesammelten Daten in verschiedenen Formaten speichern. Beispiele:

   - Speichern als JSON:

     scrapy crawl spider_name -o output.json


   - Speichern als CSV:

     scrapy crawl spider_name -o output.csv


## Projektstruktur


scrapeOr/
│
├── .venv-scraping/          # Virtuelle Umgebung (nicht versioniert)
├── .vscode
├── src
├── .env
├── spiders/                 # Enthält alle Scrapy-Spiders
├── README.md                # Diese Dokumentation


## Erweiterung

Um das Projekt zu erweitern und neue Seiten zu scrapen, können Sie einfach einen neuen Spider erstellen. Dies geschieht wie folgt:

## Hilfe und Unterstützung

Weitere Informationen zu Scrapy finden Sie in der offiziellen [Scrapy-Dokumentation](https://docs.scrapy.org/en/latest/).

