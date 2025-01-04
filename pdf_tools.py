import PyPDF2
from termcolor import colored

def extract_text_from_pdf(pdf_path):
    try:
        print(colored(f"→ Opening PDF file: {pdf_path}", "yellow"))
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ''
            total_pages = len(pdf_reader.pages)
            print(colored(f"→ Processing {total_pages} pages...", "cyan"))
            
            for i, page in enumerate(pdf_reader.pages, 1):
                try:
                    text += page.extract_text()
                    print(colored(f"✓ Processed page {i}/{total_pages}", "green"), end='\r')
                except Exception as e:
                    print(colored(f"\n✗ Error extracting text from page {i}: {str(e)}", "red"))
            
            print(colored("\n✓ PDF extraction completed", "green"))
            return text
    except Exception as e:
        error_msg = f"✗ Error processing PDF: {str(e)}"
        print(colored(error_msg, "red"))
        raise