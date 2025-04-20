from pdf2image import convert_from_path

try:
    pdf_path = "~/Desktop/test.pdf"  # Dein Test-PDF
    images = convert_from_path(pdf_path, poppler_path="/opt/homebrew/bin")
    print(f"Erfolgreich: {len(images)} Seiten konvertiert")
except Exception as e:
    print(f"Fehler: {str(e)}")