from bs4 import BeautifulSoup
from html import unescape
from datetime import date, timedelta
import pandas as pd
import re


RESULTS_FILE = "results.html"


REQUIRED_COLUMNS = [
    "Party 1",
    "Party 2",
    "Type",
    "Book-Page",
    "Date",
    "Description",
    "Additional Description",
    "Related",
]


def calculate_dates():
    """Calculate the dynamic 80-day date range."""

    today = date.today()
    from_date = today - timedelta(days=80)

    return (
        from_date.strftime("%m/%d/%Y"),
        today.strftime("%m/%d/%Y"),
    )


def clean_text(text):
    """Normalize whitespace."""

    if not text:
        return ""

    return " ".join(text.split()).strip()


def load_html(filename):
    """
    Load SearchIQS HTML.

    If the file was saved using Ctrl+U / View Source,
    Edge wraps the original HTML inside td.line-content.
    We reconstruct the original HTML here.
    """

    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    viewer = BeautifulSoup(html, "lxml")

    # Detect browser View Source wrapper
    source_lines = viewer.select("td.line-content")

    if source_lines:
        print("Detected browser View Source format.")

        raw_html = "\n".join(
            line.get_text()
            for line in source_lines
        )

        return unescape(raw_html)

    # Normal HTML
    return html


def find_results_table(soup):
    """Find the SearchIQS result table."""

    for table in soup.find_all("table"):

        for row in table.find_all("tr"):

            cells = row.find_all("td")

            values = [
                clean_text(cell.get_text(" ", strip=True))
                for cell in cells
            ]

            if all(column in values for column in REQUIRED_COLUMNS):

                return table

    return None


def parse_results(filename):

    html = load_html(filename)

    soup = BeautifulSoup(html, "lxml")

    table = find_results_table(soup)

    if table is None:
        print("ERROR: Could not find SearchIQS results table.")
        return []

    print("SearchIQS result table found.")

    records = []

    for row in table.find_all("tr"):

        cells = row.find_all("td")

        values = [
            clean_text(cell.get_text(" ", strip=True))
            for cell in cells
        ]

        # Expected structure:
        #
        # 0 = empty
        # 1 = empty
        # 2 = Select
        # 3 = RecordID
        # 4 = Party 1
        # 5 = Party 2
        # 6 = Type
        # 7 = Book-Page
        # 8 = Date
        # 9 = Description
        # 10 = Additional Description
        # 11 = Related

        if len(values) < 12:
            continue

        record_id = values[3]

        # Only process actual record rows
        if not re.fullmatch(r"L\|\d+", record_id):
            continue

        record = {
            "Party 1": values[4],
            "Party 2": values[5],
            "Type": values[6],
            "Book-Page": values[7],
            "Date": values[8],
            "Description": values[9],
            "Additional Description": values[10],
            "Related": values[11],
        }

        records.append(record)

    return records


def main():

    print("=" * 60)
    print("SEARCHIQS ASHFORD LAND RECORD SCRAPER")
    print("=" * 60)

    from_date, to_date = calculate_dates()

    print(f"From Date : {from_date}")
    print(f"To Date   : {to_date}")
    print("Document  : LAND RECORDS")
    print()

    # Page 1
    print("Parsing Page 1...")
    records_page1 = parse_results("results.html")
    print(f"Page 1 records: {len(records_page1)}")

    # Page 2
    print("\nParsing Page 2...")
    records_page2 = parse_results("results_page2.html")
    print(f"Page 2 records: {len(records_page2)}")

    # Combine
    all_records = records_page1 + records_page2

    print("\n" + "-" * 60)
    print(f"Total records collected: {len(all_records)}")

    if not all_records:
        print("No records found.")
        return

    df = pd.DataFrame(all_records)

    # Remove duplicates
    df = df.drop_duplicates()

    print(f"Total after duplicates removed: {len(df)}")

    # Save final CSV
    df.to_csv(
        "sample_output.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nCreated: sample_output.csv")

    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()