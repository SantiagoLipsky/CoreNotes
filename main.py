import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np
import os
import glob
import ollama

# Set Tesseract path for macOS
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def preprocess_image(image):
    """
    Optimized preprocessing for handwritten notes and slides.
    """
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=2.5, beta=0)
    
    # Noise reduction
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Combined binarization
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 21, 8)
    _, global_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = cv2.bitwise_and(thresh, global_thresh)
    
    # Sharpening
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    thresh = cv2.filter2D(thresh, -1, kernel)
    
    return Image.fromarray(cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB))

def pdf_to_text(pdf_path, lang='deu'):
    """
    Converts a PDF to text via OCR, optimized for UML slides and handwriting.
    """
    try:
        # Higher DPI for better recognition
        images = convert_from_path(pdf_path, dpi=600, poppler_path="/opt/homebrew/bin")
        full_text = []
        
        # Get the base name of the PDF file (without extension)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        for i, image in enumerate(images):
            processed_image = preprocess_image(image)
            # Tesseract configuration
            text = pytesseract.image_to_string(processed_image, lang=lang)
            full_text.append(text)
            print(f"Page {i+1} of {pdf_name} processed")
        
        return "\n\n".join(full_text)
    
    except Exception as e:
        return f"Error during processing {pdf_path}: {str(e)}"

def interpret_text(input_text):
    """
    Corrects errors in the raw Tesseract-extracted text without summarizing, restructuring, or adding content.
    """
    prompt = """You are an expert in correcting OCR-extracted text. The following text may contain errors (e.g., typos, misread characters like 'l' instead of '1', formatting issues like incorrect line breaks or spaces) due to OCR processing of handwritten notes or slides. Your task is to correct these errors to produce a clean, accurate version of the text. 

    **Instructions**:
    - Do NOT summarize the text.
    - Do NOT restructure the text (e.g., do not convert paragraphs into bullet points or vice versa).
    - Do NOT add any new content, explanations, or interpretations.
    - Do NOT remove any content unless it is clearly an OCR artifact (e.g., random symbols like '~~~' or '|||').
    - Preserve the original structure, including line breaks, paragraphs, bullet points, and numbering exactly as they appear.
    - Only correct OCR errors such as misread characters, incorrect punctuation, or formatting issues.
    - Respond in the same language as the input text.

    Text to correct:

    {input_text}"""
    
    response = ollama.generate(
        model="llama3.1:8b",
        prompt=prompt.format(input_text=input_text),
        options={
            "num_predict": 2000,
            "temperature": 0.1,  # Even lower temperature for strict error correction
            "top_p": 0.9
        }
    )
    return response['response'].strip()

def translate_text(input_text, target_language):
    """
    Translates the text to the target language if needed.
    """
    if target_language.lower() == "en":
        prompt = """Translate the following text to English, ensuring accuracy and preserving the meaning: 

        {input_text}"""
    else:
        prompt = """Translate the following text to German, ensuring accuracy and preserving the meaning: 

        {input_text}"""
    
    response = ollama.generate(
        model="llama3.1:8b",
        prompt=prompt.format(input_text=input_text),
        options={
            "num_predict": 2000,
            "temperature": 0.5,
            "top_p": 0.9
        }
    )
    return response['response'].strip()

def summarize_text(input_text, language="de", max_length=2000):
    """
    Summarizes text using Ollama, in specified language.
    """
    if language.lower() == "en":
        system_prompt = """You are an expert in text summarization. Summarize the following text concisely, retaining the core messages and providing a brief explanation of the main concepts. Include an example to illustrate the content. Respond in English: """
    else:  # Default to German
        system_prompt = """Du bist ein Experte für Textzusammenfassungen. Fasse den folgenden Text präzise zusammen, behalte die Kernaussagen bei und liefere eine kurze Erklärung der Hauptkonzepte. Gib ein Beispiel, um die Inhalte zu verdeutlichen. Antworte auf Deutsch: """
    
    prompt = f"{system_prompt} {input_text}"
    
    response = ollama.generate(
        model="llama3.1:8b",
        prompt=prompt,
        options={
            "num_predict": max_length,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    return response['response'].strip()

def generate_detailed_explanation(input_text, language="de"):
    """
    Generates a detailed explanation in Notion-compatible Markdown format for exam preparation.
    """
    if language.lower() == "en":
        prompt = """You are an expert in creating detailed educational content for exam preparation. Using the following text, create a compact, structured explanation in Notion-compatible Markdown format. Do not omit any key information, as this will be used for exam preparation. Extract key points, explain them in detail, and include relevant mathematical formulas in LaTeX (using $$ for block formulas) and code snippets in Markdown code blocks. Use the following template exactly, without any introduction, conclusion, or summary:

# [Lecture Topic]

## 1. [Key Point 1]

### 1.1 [Subpoint 1]
**Definition/Description**:  
[Detailed explanation of the concept, including context and relevance. Include an example if necessary.]

## Terminology (if necessary, only important technical terms)

**Mathematical Formula** (if applicable):  
$$ [LaTeX Formula] $$

**Code** (if applicable):  
```[Programming Language]
[Code Snippet]
```

Text to process: 

{input_text}

Respond in English."""
    else:
        prompt = """Du bist ein Experte für die Erstellung detaillierter Lerninhalte zur Klausurvorbereitung. Erstelle aus dem folgenden Text eine kompakte, strukturierte Erklärung im Notion-kompatiblen Markdown-Format. Lasse keine wichtigen Informationen weg, da dies für die Klausurvorbereitung genutzt wird. Extrahiere Schlüsselpunkte, erkläre sie detailliert und füge relevante mathematische Formeln in LaTeX (mit $$ für Blockformeln) sowie Code in Markdown-Codeblöcken hinzu. Verwende ausschließlich das folgende Template, ohne Einleitung, Fazit oder Zusammenfassung:

# [Thema der Vorlesung]

## 1. [Schlüsselpunt 1]

### 1.1 [Unterpunkt 1]
**Definition/Beschreibung**:  
[Detaillierte Erklärung des Konzepts, inklusive Kontext und Relevanz. Beispiel falls nötig.]

## Begriffserklärung (falls nötig, nur wichtige Fachbegriffe)

**Mathematische Formel** (falls zutreffend):  
$$ [LaTeX-Formel] $$

**Code** (falls zutreffend):  
```[Programmiersprache]
[Code-Snippet]
```

Text to process: 

{input_text}

Antworte auf Deutsch."""
    
    response = ollama.generate(
        model="llama3.1:8b",
        prompt=prompt.format(input_text=input_text),
        options={
            "num_predict": 3000,
            "temperature": 0.5,
            "top_p": 0.9
        }
    )
    return response['response'].strip()

def main():
    # Prompt user to select input and output languages
    while True:
        input_language = input("Select input language of the PDF (de/en): ").strip().lower()
        if input_language in ["de", "en"]:
            break
        print("Invalid input. Please enter 'de' for German or 'en' for English.")

    while True:
        output_language = input("Select desired output language for summaries and explanations (de/en): ").strip().lower()
        if output_language in ["de", "en"]:
            break
        print("Invalid input. Please enter 'de' for German or 'en' for English.")

    # Define input and output directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, "IN")
    output_dir = os.path.join(script_dir, "OUT")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return
    
    # Find all PDF files in the IN directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}.")
        return
    
    for pdf_path in pdf_files:
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"\nProcessing {pdf_name}...")
        
        # Set Tesseract language based on input language
        tesseract_lang = 'deu' if input_language == "de" else 'eng'
        
        # Extract text from PDF
        extracted_text = pdf_to_text(pdf_path, lang=tesseract_lang)
        print("\nRaw Tesseract Extracted Text:\n")
        print(extracted_text)
        
        # Save raw extracted text in the OUT folder
        raw_output_text_path = os.path.join(output_dir, f"{pdf_name}_raw_output.txt")
        with open(raw_output_text_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
        # Interpret the raw extracted text (correct errors only)
        print("\nInterpreted Text by KI (Errors Corrected):\n")
        interpreted_text = interpret_text(extracted_text)
        print(interpreted_text)
        
        # Save interpreted text in the OUT folder
        interpreted_output_path = os.path.join(output_dir, f"{pdf_name}_interpreted.txt")
        with open(interpreted_output_path, "w", encoding="utf-8") as f:
            f.write(interpreted_text)
        
        # Translate if input and output languages differ
        if input_language != output_language:
            text_to_process = translate_text(interpreted_text, output_language)
        else:
            text_to_process = interpreted_text
        
        # Summarize text in the output language
        print(f"\nSummary in {output_language.upper()}:\n")
        summary = summarize_text(text_to_process, language=output_language)
        print(summary)
        
        # Save summary in the OUT folder
        summary_output_path = os.path.join(output_dir, f"{pdf_name}_summary_{output_language}.txt")
        with open(summary_output_path, "w", encoding="utf-8") as f:
            f.write(summary)
        
        # Generate detailed explanation in Notion-compatible Markdown
        print(f"\nDetailed Explanation in {output_language.upper()} (Notion Markdown):\n")
        detailed_explanation = generate_detailed_explanation(text_to_process, language=output_language)
        print(detailed_explanation)
        
        # Save detailed explanation in the OUT folder
        explanation_output_path = os.path.join(output_dir, f"{pdf_name}_explanation_{output_language}.md")
        with open(explanation_output_path, "w", encoding="utf-8") as f:
            f.write(detailed_explanation)
        
        print(f"Finished processing {pdf_name}. Outputs saved in {output_dir}.")

if __name__ == "__main__":
    main()