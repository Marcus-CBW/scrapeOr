# Reguläre Ausdrücke (RegEx) in Python ermöglichen die Suche, das Extrahieren und die Manipulation von Zeichenfolgen auf flexible Weise. Python bietet das Modul re für die Arbeit mit regulären Ausdrücken.

# Hier sind die wichtigsten Funktionen des re-Moduls:

#     re.search(): Sucht nach einem Muster in einer Zeichenfolge.
#     re.match(): Prüft, ob ein Muster am Anfang einer Zeichenfolge vorhanden ist.
#     re.findall(): Findet alle Vorkommen eines Musters in einer Zeichenfolge.
#     re.sub(): Ersetzt Muster in einer Zeichenfolge durch einen anderen Text.
#     re.split(): Teilt eine Zeichenfolge anhand eines Musters.

# Beispiel: Grundlagen von RegEx in Python
import re

# 1. re.search(): Sucht nach dem Muster 'abc' in einer Zeichenfolge.
text = "abc123xyz"
result = re.search(r'abc', text)
if result:
    print("Gefunden:", result.group())

# 2. re.match(): Überprüft, ob die Zeichenfolge mit 'abc' beginnt.
result = re.match(r'abc', text)
if result:
    print("Match am Anfang gefunden:", result.group())

# 3. re.findall(): Findet alle Vorkommen von Ziffern in der Zeichenfolge.
result = re.findall(r'\d+', text)  # '\d+' sucht eine oder mehrere Ziffern
print("Alle Ziffernfolgen:", result)

# 4. re.sub(): Ersetzt alle Ziffern durch '#' in der Zeichenfolge.
result = re.sub(r'\d+', '#', text)
print("Nach Ersetzung:", result)

# 5. re.split(): Teilt die Zeichenfolge an den Stellen mit Ziffern.
result = re.split(r'\d+', text)
print("Gesplittete Teile:", result)

# Erklärung:

#     r'abc': Das r vor dem String markiert den String als Raw-String, der Sonderzeichen in RegEx korrekt verarbeitet.
#     \d+: Steht für eine oder mehr Ziffern.
#     group(): Gibt das gefundene Ergebnis zurück.

# Nützliche RegEx-Symbole:

#     .: Beliebiges Zeichen außer einem Zeilenumbruch.
#     ^: Anfang einer Zeichenfolge.
#     $: Ende einer Zeichenfolge.
#     *: Null oder mehr Wiederholungen.
#     +: Eine oder mehr Wiederholungen.
#     []: Zeichenklasse, z.B. [a-z] für Kleinbuchstaben.
#     \d: Beliebige Ziffer (0-9).


# re = r'<span class="visually-hidden">(.*?)\s*(\d{1,5}(?:,\d{3})*(?:\.\d{2})?)'
# r'...'
# Das r vor dem String markiert den Ausdruck als Raw String, was bedeutet, dass Python Escape-Zeichen wie \ direkt übernimmt und
# nicht als Steuerzeichen interpretiert. Dies ist besonders wichtig, um sicherzustellen, dass der Backslash (\) korrekt 
# für den Ausdruck genutzt wird.

# <span class="visually-hidden">
# Dieser Teil des Ausdrucks sucht nach einem exakten HTML-Tag:
# span: Sucht nach einem HTML <span>-Tag.
# class="visually-hidden": Stellt sicher, dass das span-Tag die Klasse visually-hidden besitzt.
# Dieser Teil ist wichtig, um sicherzustellen, dass der Ausdruck nur auf ein sehr spezifisches span-Tag in einem HTML-Dokument zutrifft.

# (.*?)
# () definiert eine Gruppe, die das Ergebnis, das von diesem Teil des Ausdrucks gefunden wird, speichert.
# .*? steht für eine nicht-gierige Suche von beliebigen Zeichen (inkl. Leerzeichen),
# die möglichst wenig Text zwischen dem öffnenden <span>-Tag und den Zahlen umfasst.
# .: Beliebiges Zeichen außer einem Zeilenumbruch.
# *?: Die Kombination *? ist eine nicht-gierige Version des Sternchens (*), d.h., sie sucht so wenig wie möglich Zeichen,
# bis der nächste Ausdruck (hier die Zahl) gefunden wird.
# Insgesamt sucht dieser Teil des Ausdrucks nach beliebigem Text innerhalb des span, solange dieser Text möglichst kurz ist.

# \s*
# \s* sucht nach null oder mehr Leerraumzeichen (wie Leerzeichen, Tabs, Zeilenumbrüche). Dies ist wichtig,
# um mögliche Leerzeichen zwischen dem gefundenen Text und der folgenden Zahl zu berücksichtigen.

# (\d{1,5}(?:,\d{3})*(?:\.\d{2})?)
# Dieser Teil des regulären Ausdrucks sucht nach einer Zahl im üblichen Format mit Kommas für Tausendertrennungen und einem optionalen Dezimalteil.

# \d{1,5}: Sucht nach 1 bis 5 Ziffern. Dies deckt den Teil der Zahl vor dem ersten Tausendertrennzeichen ab (z.B. 123, 12345).
# (?:,\d{3})*: Dies ist eine nicht speichernde Gruppe (?:), die optional wiederholte Kommas mit drei Ziffern danach sucht,
# um Tausendertrennzeichen zu erkennen (z.B. 1,234, 1,234,567).

# (?:\.\d{2})?: Dies ist eine weitere nicht speichernde Gruppe, die nach einem Punkt und zwei Dezimalstellen sucht. Der Dezimalteil ist optional (z.B. .99).
# Gesamtfunktion des regulären Ausdrucks:
# Er sucht ein HTML-span-Tag mit der Klasse visually-hidden.
# Innerhalb dieses Tags sucht er nach beliebigem Text, gefolgt von einer Zahl im Format von 1 bis 5 Ziffern,
# optional mit Tausenderkommas und einem optionalen Dezimalteil.

# https://www.ionos.de/digitalguide/websites/webseiten-erstellen/regulaere-ausdruecke/
# https://regexr.com/
