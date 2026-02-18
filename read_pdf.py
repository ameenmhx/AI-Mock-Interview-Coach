from pypdf import PdfReader

print("--- PDF Reader Test ---")

try:
    # 1. Open the PDF file
    reader = PdfReader("resume.pdf")
    
    # 2. Extract text from all pages
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # 3. Print the result
    print("\n--- Extracted Resume Text ---\n")
    print(full_text)
    print("\n-----------------------------")
    
except FileNotFoundError:
    print("Error: Could not find 'resume.pdf' in this folder!")
except Exception as e:
    print(f"An error occurred: {e}")