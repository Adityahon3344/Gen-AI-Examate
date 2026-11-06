
import requests
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

DOCUMENTS = {
    "farm_mechanization.html": (
        "https://mahadbt.maharashtra.gov.in/Farmer/"
        "SchemeData/SchemeData?str="
        "E9DDFA703C38E51A23C0254248DAFF28"
    ),
    "Scheme-SubMissionOnFarmMechanization.pdf": (
        "https://mahadbt.maharashtra.gov.in/Farmer/PDF/"
        "Scheme-SubMissionOnFarmMechanization.pdf"
    ),
    "DBT_Farmer_User_Manual.pdf": (
        "https://mahadbt.maharashtra.gov.in/Farmer/PDF/"
        "DBT_Farmer_User_Manual.pdf"
    )
}


def download_file(filename, url):
    file_path = RAW_DIR / filename

    try:
        print(f"\nDownloading: {filename}")

        response = requests.get(
            url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        file_path.write_bytes(response.content)

        print(f"Downloaded successfully: {filename}")

    except requests.exceptions.Timeout:
        print(f"Timeout error: {filename}")

    except requests.exceptions.RequestException as error:
        print(f"Download error: {error}")

    except OSError as error:
        print(f"File saving error: {error}")


def main():
    for filename, url in DOCUMENTS.items():
        download_file(filename, url)


if __name__ == "__main__":
    main()
