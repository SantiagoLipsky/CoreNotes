import ollama

def summarize_text(input_text, max_length=2000):
    # System-Prompt für präzise Zusammenfassungen
    system_prompt = """Du bist ein Experte für Textzusammenfassungen. Fasse den folgenden Text präzise zusammen, behalte die Kernaussagen bei und liefere eine kurze Erklärung der Hauptkonzepte. Gib ein Beispiel, um die Inhalte zu verdeutlichen. Antworte auf Deutsch."""
    
    # Eingabe formatieren
    prompt = f"{system_prompt}\n\nFasse diesen Text zusammen: {input_text}"
    
    # Ollama API aufrufen
    response = ollama.generate(
        model="llama3.1:8b",
        prompt=prompt,
        options={
            "num_predict": max_length,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    
    # Antwort zurückgeben
    return response['response'].strip()

# Beispieltext (kann durch Nutzerinput ersetzt werden)
example_text = """
Ping (Datenübertragung)

47 Sprachen
Artikel
Diskussion
Lesen
Bearbeiten
Quelltext bearbeiten
Versionsgeschichte

Werkzeuge
Erscheinungsbild Verbergen
Text

Klein

Standard

Groß
Breite

Standard

Breit
Farbe (Beta)

Automatisch

Hell

Dunkel
Ping ist ein Diagnose-Werkzeug, mit dem überprüft werden kann, ob ein bestimmter Host in einem IP-Netzwerk erreichbar ist. Daneben geben die meisten heutigen Implementierungen dieses Werkzeuges auch die Zeitspanne zwischen dem Aussenden eines Paketes zu diesem Host und dem Empfangen eines daraufhin unmittelbar zurückgeschickten Antwortpaketes an (= Paketumlaufzeit, meist round trip time oder RTT genannt). Das Programm wird üblicherweise als Konsolenbefehl ausgeführt. Entwickelt wurde Ping ursprünglich Ende 1983 von Mike Muuss und erschien zum ersten Mal in BSD 4.3.

Funktionsweise
Ping sendet ein ICMP- oder ICMPv6-Paket des Typs „Echo Request“ an die angegebene Zieladresse. Der Empfänger antwortet darauf mit einem ICMP- oder ICMPv6-Paket vom Typ „Echo Reply“. Ist der Zielrechner nicht erreichbar, antwortet der zuständige Router mit einem ICMP- oder ICMPv6-Paket: „Network unreachable“ (Netzwerk nicht erreichbar) oder „Host unreachable“ (Gegenstelle nicht erreichbar).

Aus einer fehlenden Antwort kann nicht zweifelsfrei geschlossen werden, dass die Gegenstelle nicht erreichbar wäre, da manche Hosts oder Netze so konfiguriert sind, dass sie Ping-Anfragen ignorieren und verwerfen.

Wird dem Ping-Kommando ein Hostname anstatt einer IP-Adresse übergeben, lässt das Programm diesen durch das Betriebssystem auflösen. Bei einer fehlerhaft konfigurierten Namensauflösung schlägt diese nach Ablauf einer Wartezeit (Timeout) fehl und resultiert in einer Fehlermeldung. Falls eine IP-Adresse angegeben wurde, kann bei der Rückwärtsauflösung von IP-Adresse zu Name ebenfalls ein Timeout auftreten. Je nach Implementation von Ping ist die Rückwärtsauflösung jedoch standardmäßig deaktiviert oder lässt sich per Option abschalten.

Beispiel

Ping auf der Kommandozeile in Windows
Es werden Datenpakete an den Zielhost www.google.de gesandt. Vom Programm wird die Zeit gemessen, bis die Antwort des Hosts eintrifft. Die Zeitangabe sagt aus, wie lange ein Datenpaket zum Host und wieder zurück benötigt („response time average“). Man kann daran grob erkennen, ob das Routing zur Gegenstelle funktioniert, deren TCP/IP-Stack funktionsfähig ist und mit welcher Verzögerung bei einer Verbindung zu rechnen ist.

Die Angabe TTL kann dazu genutzt werden, um grob abzuschätzen, über wie viele Router die ICMP-Antworten zurückgelaufen sind (jeder Router dekrementiert den Wert mindestens um 1, wobei der Initialwert je nach Implementierung 64, 128 etc. sein kann). Der Hinweg der Datenpakete muss nicht dem Rückweg entsprechen, daher ist die TTL nur ein Maß für die Anzahl der Router auf dem Rückweg. Bei Verwendung von dynamischen Routingmechanismem kann die TTL daher auch bei jeder Antwort anders aussehen
"""
# Zusammenfassung aufrufen
if __name__ == "__main__":
    result = summarize_text(example_text)
    print("Zusammenfassung:\n", result)