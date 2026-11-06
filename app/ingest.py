
from pathlib import Path
from bs4 import BeautifulSoup
from pypdf import PdfReader

RAW_DIR = Path("data/raw")
OUTPUT_FILE = RAW_DIR / "extracted_text.txt"


def extract_html():
    try:
        file_path = RAW_DIR / "farm_mechanization.html"

        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        return soup.get_text(separator="\n", strip=True)

    except (OSError, UnicodeError) as error:
        print("HTML extraction error:", error)
        return ""


def extract_pdf():
    try:
        file_path = RAW_DIR / "Scheme-SubMissionOnFarmMechanization.pdf"
        pdf = PdfReader(file_path)

        text = ""

        for page_number, page in enumerate(pdf.pages, start=1):
            try:
                text += page.extract_text() or ""
                text += "\n"
            except Exception as error:
                print(f"Skipping PDF page {page_number}: {error}")

        return text

    except Exception as error:
        print("PDF extraction error:", error)
        return ""


def main():
    html_text = extract_html()
    pdf_text = extract_pdf()

    combined_text = (
        "===== SCHEME WEBPAGE =====\n"
        + html_text
        + "\n===== SCHEME PDF =====\n"
        + pdf_text
    )

    try:
        OUTPUT_FILE.write_text(combined_text, encoding="utf-8")
        print("Text extraction completed.")
        print("HTML characters:", len(html_text))
        print("PDF characters:", len(pdf_text))
        print("Saved to:", OUTPUT_FILE)

    except OSError as error:
        print("File saving error:", error)


if __name__ == "__main__":
    main()
