from pdfminer.high_level import extract_text

def extract_pdf_text(file_path):
    text = extract_text(file_path)
    return text

# Example usage
pdf_text = extract_pdf_text('C:\\Users\\Sri Ranjini kavita\\Desktop\\bhumi\\IndianAdvisory\\pdf\\Karnataka_Ballari_English_2024-07-26.pdf')
print(pdf_text)  # Check if the text is being extracted
