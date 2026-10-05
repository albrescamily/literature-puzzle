""" Load → Iterate Pages → Extract → Clean → Save """

from pypdf import PdfReader
import os
import re

def preprocess_text(text: str) -> str:
    if not text:
        return ""

    #collapse multiple newlines into a single newline
    text = re.sub(r'\n+', '\n', text)
    #collapse multiple spaces and tabs into a single space
    text = re.sub(r'[ \t]+', ' ', text)
    #remove leading and trailing whitespace from each line
    text = text.encode("utf-8", errors="ignore").decode()
    #split text into lines, strip leading and trailing whitespace from each line, and remove empty lines
    lines = [line.strip() for line in text.split('\n')]
    #remove empty lines
    lines = [line for line in lines if line]
    
    return '\n'.join(lines)


def process_page(text: str) -> str:
    if not text:
        return ""

    match = re.search(r'\[\s*(\d+)\s*\]', text)

    page_number = ""
    if match:
        page_number = match.group(1)
        text = text.replace(match.group(0), "")

    text = preprocess_text(text)

    return f"{page_number}\n{text}"


def pdf_to_txt_per_page(pdf_path: str, output_dir: str):
    """
    Converts each page of a PDF into a separate .txt file.
    """
    os.makedirs(output_dir, exist_ok=True)

    reader = PdfReader(pdf_path)
    print(reader.pages)

    for i, page in enumerate(reader.pages):
        if i == 100:
            break

        raw_text = page.extract_text()
        processed_text = process_page(raw_text)
        output_file = os.path.join(output_dir, f"page_{i+1}.txt")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(processed_text)

        print(f"[OK] Saved: {output_file}")

if __name__ == "__main__":

    pdf_path = "data/raw/torquemada-en.pdf"
    output_dir = "data/processed"

    pdf_to_txt_per_page(pdf_path, output_dir)