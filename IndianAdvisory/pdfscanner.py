import os
import PyPDF2

# Directory containing the PDFs
PDF_DIRECTORY = "C:\\Users\\Sri Ranjini kavita\\Desktop\\bhumi\\IndianAdvisory\\pdf"

def extract_pdf_data(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return "\n".join(text)

def parse_pdf_text(text):
    # Implement parsing logic here
    # Extracting weather forecast and advisories
    data = {
        "weather_forecast": [],
        "agro_advisories": [],
        # Additional fields as necessary
    }
    # Populate data dictionary based on parsing
    return data

def process_all_pdfs_in_directory(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")  # Debugging output
            pdf_text = extract_pdf_data(file_path)
            structured_data = parse_pdf_text(pdf_text)
            results.append({
                "file": filename,
                "data": structured_data
            })
    return results

# Process all PDFs in the directory
pdf_results = process_all_pdfs_in_directory(PDF_DIRECTORY)

# Example: Output the results for verification
for result in pdf_results:
    print(f"File: {result['file']}")
    print(f"Data: {result['data']}")
