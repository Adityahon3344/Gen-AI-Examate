
import json
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("data/chunks.json")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def extract_pdf_chunks(file_path):
    """Extract PDF text page by page and create chunks."""
    results = []

    try:
        pdf = PdfReader(file_path)
        title = pdf.metadata.title if pdf.metadata and pdf.metadata.title else file_path.stem

        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""

            for index, chunk in enumerate(split_text(text)):
                results.append({
                    "id": f"{file_path.stem}_page{page_number}_chunk{index + 1}",
                    "text": chunk,
                    "source": file_path.name,
                    "page": page_number,
                    "title": title
                })

    except Exception as error:
        print(f"PDF extraction error ({file_path.name}): {error}")

    return results


def extract_html_chunks(file_path):
    """Extract HTML text and create chunks."""
    results = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.get_text(strip=True) if soup.title else file_path.stem
        text = soup.get_text(separator=" ", strip=True)

        for index, chunk in enumerate(split_text(text)):
            results.append({
                "id": f"{file_path.stem}_chunk{index + 1}",
                "text": chunk,
                "source": file_path.name,
                "page": None,
                "title": title
            })

    except Exception as error:
        print(f"HTML extraction error ({file_path.name}): {error}")

    return results


def create_chunks():
    """Process all PDF and HTML documents."""
    all_chunks = []

    for file_path in RAW_DIR.glob("*.pdf"):
        print(f"Processing PDF: {file_path.name}")
        all_chunks.extend(extract_pdf_chunks(file_path))

    for file_path in RAW_DIR.glob("*.html"):
        print(f"Processing HTML: {file_path.name}")
        all_chunks.extend(extract_html_chunks(file_path))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(all_chunks, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nChunking completed!")
    print("Total chunks:", len(all_chunks))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    create_chunks()
