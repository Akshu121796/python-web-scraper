from bs4 import BeautifulSoup
from html import unescape
from datetime import date, timedelta
import pandas as pd
import re


# -----------------------------
# Configuration
# -----------------------------

PAGE_FILES = [
    "results.html",
    "results_page2.html",
]

OUTPUT_FILE = "sample_output.csv"


# -----------------------------
# Date handling
# -----------------------------

def get_date_range():
    """Return the dynamic 80-day search range."""

    today = date.today()
    from_date = today - timedelta(days=80)

    return (
        from_date.strftime("%m/%d/%Y"),
        today.strftime("%m/%d/%Y"),
    )


# -----------------------------
# HTML handling
# -----------------------------

def load_source_html(filename):
    """Load normal HTML or browser View Source HTML."""

    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "lxml")

    # Edge/Chrome View Source wraps original HTML in line-content cells
    source_lines = soup.select("td.line-content")

    if source_lines:
        print("Detected browser View Source format.")
        return unescape(
            "\n".join(line.get_text() for line in source_lines)
        )

    return html


def clean_text(value):
    """Normalize whitespace."""

    return " ".join(value.split()).strip()


# -----------------------------
# Record parsing
# -----------------------------

def find_results_table(soup):
    """Find the SearchIQS table containing the required columns."""

    required = {
        "Party 1",
        "Party 2",
        "Type",
        "Book-Page",
        "Date",
        "Description",
        "Additional Description",
        "Related",
    }

    for table in soup.find_all("table"):

        for row in table.find_all("tr"):

            values = [
                clean_text(cell.get_text(" ", strip=True))
                for cell in row.find_all("td")
            ]

            if required.issubset(set(values)):
                return table

    return None


def parse_page(filename):
    """Parse one SearchIQS results page."""

    html = load_source_html(filename)
    soup = BeautifulSoup(html, "lxml")

    table = find_results_table(soup)

    if table is None:
        raise RuntimeError(
            f"Could not find results table in {filename}"
        )

    print("SearchIQS result table found.")

    records = []

    for row in table.find_all("tr"):

        values = [
            clean_text(cell.get_text(" ", strip=True))
            for cell in row.find_all("td")
        ]

        # SearchIQS result structure:
        # [empty, empty, Select, RecordID,
        #  Party 1, Party 2, Type, Book-Page,
        #  Date, Description, Additional Description, Related]

        if len(values) < 12:
            continue

        record_id = values[3]

        # Actual records have IDs such as L|12345
        if not re.fullmatch(r"L\|\d+", record_id):
            continue

        records.append({
            "Party 1": values[4],
            "Party 2": values[5],
            "Type": values[6],
            "Book-Page": values[7],
            "Date": values[8],
            "Description": values[9],
            "Additional Description": values[10],
            "Related": values[11],
        })

    return records


# -----------------------------
# Main scraper
# -----------------------------

def main():

    print("=" * 60)
    print("SEARCHIQS ASHFORD LAND RECORD SCRAPER")
    print("=" * 60)

    from_date, to_date = get_date_range()

    print(f"From Date : {from_date}")
    print(f"To Date   : {to_date}")
    print("Document  : LAND RECORDS")
    print()

    all_records = []

    for page_number, filename in enumerate(PAGE_FILES, start=1):

        print(f"Parsing Page {page_number}...")

        records = parse_page(filename)

        print(f"Page {page_number} records: {len(records)}")

        all_records.extend(records)

    print()
    print("-" * 60)

    print(f"Total records collected: {len(all_records)}")

    # Remove duplicate records
    df = pd.DataFrame(all_records).drop_duplicates()

    print(f"Total after duplicates removed: {len(df)}")

    # Export
    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nCreated: {OUTPUT_FILE}")

    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()