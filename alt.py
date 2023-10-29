import csv
import sys
import PyPDF2
import re
def sanitize_filepath(filepath):
    invalid_chars = r'[<>:"/\\|?*]'

    sanitized_filepath = re.sub(invalid_chars, '_', filepath)
    return sanitized_filepath

def extract_pages_from_pdf(input_pdf, csv_file):
    with open(input_pdf, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)

        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                chapter = sanitize_filepath(row["chapter"])
                filename = chapter + ".pdf"
                start_page = int(row["start_page"]) - 1  # Индексация страниц в PyPDF2 начинается с 0
                end_page = int(row["end_page"])

                writer = PyPDF2.PdfWriter()
                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])



                with open(filename, 'wb') as output_pdf:
                    writer.write(output_pdf)

                print(f"Saved {filename} with pages {start_page + 1} to {end_page}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script_name.py input_pdf_path csv_file_path")
        sys.exit(1)

    input_pdf = sys.argv[1]
    csv_path = sys.argv[2]

    extract_pages_from_pdf(input_pdf, csv_path)
