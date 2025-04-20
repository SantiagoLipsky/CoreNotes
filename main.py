import ollama

def summarize_text(input_text, language="de", max_length=2000):
    # System-Prompt basierend auf der Sprache
    if language.lower() == "en":
        system_prompt = """You are an expert in text summarization. Summarize the following text concisely, translate to englisch if nessasary, retaining the core messages and providing a brief explanation of the main concepts. Include an example to illustrate the content. Respond in English: """
    else:  # Standardmäßig Deutsch
        system_prompt = """Du bist ein Experte für Textzusammenfassungen. Fasse den folgenden Text präzise zusammen, übersetzte auf Deutsch wenn nötig, behalte die Kernaussagen bei und liefere eine kurze Erklärung der Hauptkonzepte. Gib ein Beispiel, um die Inhalte zu verdeutlichen. Antworte auf Deutsch"""
    
    # Eingabe formatieren
    prompt = f"{system_prompt} {input_text}"
    
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
example_text = """ Blockchain-Technologie

Die Blockchain-Technologie ist eine dezentrale Datenbankstruktur, die Transaktionen in einer Kette von Blöcken speichert. Jeder Block enthält eine Liste von Transaktionen, einen Zeitstempel und einen kryptografischen Hash des vorherigen Blocks, wodurch eine unveränderliche und transparente Aufzeichnung entsteht. Die Technologie wurde erstmals 2008 von einer Person oder Gruppe unter dem Pseudonym Satoshi Nakamoto für die Kryptowährung Bitcoin eingeführt.

Funktionsweise
Eine Blockchain funktioniert durch ein Netzwerk von Computern (Nodes), die eine Kopie der gesamten Blockchain-Datenbank hosten. Wenn eine neue Transaktion initiiert wird, wird sie von den Nodes überprüft und in einem neuen Block gesammelt. Dieser Block wird durch einen Konsensmechanismus, wie Proof of Work oder Proof of Stake, validiert. Nach der Validierung wird der Block an die Kette angehängt, und alle Nodes aktualisieren ihre Kopie der Blockchain. Dies stellt sicher, dass Manipulationen praktisch unmöglich sind, da ein Angreifer die Mehrheit der Nodes kontrollieren müsste.

Anwendungen
Neben Kryptowährungen wie Bitcoin oder Ethereum wird die Blockchain-Technologie in zahlreichen Bereichen eingesetzt. Dazu gehören Smart Contracts (automatisch ausgeführte Verträge, die in der Blockchain gespeichert sind), Lieferkettenmanagement (zur Nachverfolgung von Produkten), Identitätsverifikation (zur sicheren Speicherung persönlicher Daten) und Finanzdienstleistungen (zur Reduzierung von Transaktionskosten). Ein Beispiel ist die Verwendung von Blockchain in der Lebensmittelindustrie, wo die Herkunft von Produkten wie Kaffee oder Fisch lückenlos dokumentiert werden kann.

Vorteile und Herausforderungen
Die Blockchain bietet hohe Sicherheit, Transparenz und Dezentralisierung, da keine zentrale Autorität benötigt wird. Gleichzeitig gibt es Herausforderungen wie hohen Energieverbrauch (insbesondere bei Proof of Work), Skalierbarkeitsprobleme (begrenzte Transaktionen pro Sekunde) und regulatorische Unsicherheiten. Dennoch wird die Technologie als revolutionär angesehen, da sie Vertrauen in digitalen Systemen ohne Intermediäre schafft.

Beispiel
Ein praktisches Beispiel ist die Verwendung von Blockchain für Smart Contracts auf der Ethereum-Plattform. Ein Vertrag könnte so programmiert werden, dass eine Zahlung automatisch freigegeben wird, sobald eine Lieferung bestätigt wird. Dies reduziert das Risiko von Betrug und macht den Prozess effizienter, da keine dritte Partei wie eine Bank benötigt wird.
"""

if __name__ == "__main__":
    # Beispiel in Deutsch
    print("Zusammenfassung auf Deutsch:")
    print(summarize_text(example_text, language="de"))
    
    # Beispiel in Englisch
    print("\nZusammenfassung auf Englisch:")
    print(summarize_text(example_text, language="en"))