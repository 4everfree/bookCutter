import PyPDF2
import sys
import re


def split_by_chapters(pdf_path, keyword_pattern, output_prefix):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(reader.pages)

        chapter_starts = []

        pattern = re.compile(keyword_pattern)

        for page_num in range(total_pages):
            text = reader.pages[page_num].extract_text()
            lines = text.split("\n")
            for line in lines:
                if pattern.match(line):
                    chapter_starts.append(page_num)
                    break

        if not chapter_starts:
            print("Главы не найдены!")
            return

        chapter_starts.append(total_pages)

        for i in range(len(chapter_starts) - 1):
            writer = PyPDF2.PdfWriter()
            for page_num in range(chapter_starts[i], chapter_starts[i + 1]):
                writer.add_page(reader.pages[page_num])

            output_file = f"{output_prefix}_chapter_{i + 1}.pdf"
            with open(output_file, 'wb') as output_pdf:
                writer.write(output_pdf)

            print(f"Глава {i + 1} сохранена как {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Пожалуйста, укажите путь к PDF файлу как первый аргумент и регулярное выражение для определения начала главы как второй аргумент.")
        sys.exit(1)

    pdf_path = sys.argv[1]
    keyword_pattern = sys.argv[2]
    output_prefix = 'chapter'
    split_by_chapters(pdf_path, keyword_pattern, output_prefix)
