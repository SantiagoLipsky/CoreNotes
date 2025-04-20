import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np
import os
import ollama
import glob

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

def pdf_to_text(pdf_path, lang='deu', output_dir='OUT'):
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
            # Save preprocessed image in the OUT folder
            processed_image_path = os.path.join(output_dir, f"{pdf_name}_processed_page_{i+1}.png")
            processed_image.save(processed_image_path)
            
            # Tesseract configuration
            text = pytesseract.image_to_string(processed_image, lang=lang)
            full_text.append(text)
            print(f"Page {i+1} of {pdf_name} processed")
        
        return "\n\n".join(full_text)
    
    except Exception as e:
        return f"Error during processing {pdf_path}: {str(e)}"

def summarize_text(input_text, language="de", max_length=2000):
    """
    Summarizes text using Ollama, in specified language.
    """
    # System prompt based on language
    if language.lower() == "en":
        system_prompt = """You are an expert in text summarization. Summarize the following text concisely, translate to English if necessary, retaining the core messages and providing a brief explanation of the main concepts. Include an example to illustrate the content. Respond in English: """
    else:  # Default to German
        system_prompt = """Du bist ein Experte für Textzusammenfassungen. Fasse den folgenden Text präzise zusammen, übersetze auf Deutsch wenn nötig, behalte die Kernaussagen bei und liefere eine kurze Erklärung der Hauptkonzepte. Gib ein Beispiel, um die Inhalte zu verdeutlichen. Antworte auf Deutsch: """
    
    # Format input
    prompt = f"{system_prompt} {input_text}"
    
    # Call Ollama API
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

def main():
    # Define input and output directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, "Input")
    output_dir = os.path.join(script_dir, "OUT")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return
    
    # Find all PDF files in the Input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}.")
        return
    
    for pdf_path in pdf_files:
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"\nProcessing {pdf_name}...")
        
        # Extract text from PDF
        extracted_text = pdf_to_text(pdf_path, lang='deu', output_dir=output_dir)
        print("\nExtracted Text:\n")
        print(extracted_text)
        
        # Save extracted text in the OUT folder
        output_text_path = os.path.join(output_dir, f"{pdf_name}_output.txt")
        with open(output_text_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
        # Summarize text in German and English
        print("\nZusammenfassung auf Deutsch:")
        german_summary = summarize_text(extracted_text, language="de")
        print(german_summary)
        
        print("\nZusammenfassung auf Englisch:")
        english_summary = summarize_text(extracted_text, language="en")
        print(english_summary)
        
        # Save summaries in the OUT folder
        with open(os.path.join(output_dir, f"{pdf_name}_summary_de.txt"), "w", encoding="utf-8") as f:
            f.write(german_summary)
        with open(os.path.join(output_dir, f"{pdf_name}_summary_en.txt"), "w", encoding="utf-8") as f:
            f.write(english_summary)
        
        print(f"Finished processing {pdf_name}. Outputs saved in {output_dir}.")

if __name__ == "__main__":
    main()