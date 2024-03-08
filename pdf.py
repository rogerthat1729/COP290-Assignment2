import PyPDF2

# Path to your PDF file
pdf_file_path = 'file.pdf'

# Open the PDF file in binary mode
with open(pdf_file_path, 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)
    
    # Get the number of pages in the PDF file
    num_pages = len(pdf_reader.pages)
    print(f"Total number of pages: {num_pages}")

    # Iterate through each page of the PDF
    for page_num in range(num_pages):
        # Get a specific page from the PDF
        page = pdf_reader.pages[page_num]
        
        # Extract text from the page
        text = page.extract_text()
        print(f"Text on page {page_num + 1}:\n{text}\n")

        # Optionally, you can process the text further here
