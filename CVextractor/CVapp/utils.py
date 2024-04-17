import docx
import PyPDF2
import re

def extract_information_from_cv(cv_file):
    """
    Extracts email ID, contact number, and overall text from a CV file.
    Supports both DOCX and PDF formats.
    """
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    contact_regex = r'\b(?:\d[ -]*?){9,11}\b'  # Assumes contact numbers have 9-11 digits

    # Initialize variables to store extracted information
    email = ''
    contact_number = ''
    overall_text = ''

    try:
        # Read the content of the CV file
        if cv_file.name.endswith('.pdf'):
            with open(cv_file.name, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    overall_text += page.extractText() + '\n'

        elif  cv_file.name.endswith('.docx'):
            doc = docx.Document(cv_file)
            for para in doc.paragraphs:
                overall_text += para.text + '\n'
        else:
            raise ValueError("Unsupported file type:", cv_file.name)

        # Extract email ID using regex
        email_match = re.search(email_regex, overall_text)
        if email_match:
            email = email_match.group(0)

        # Extract contact number using regex
        contact_match = re.search(contact_regex, overall_text)
        if contact_match:
            contact_number = contact_match.group(0)

    except Exception as e:
        print(f"Error extracting information from CV: {e}")

    return email, contact_number, overall_text
