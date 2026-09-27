# SearchIQS Ashford Land Records Scraper

A Python-based web scraper developed for the Adoraxe Python Web Scraper Challenge.

The scraper extracts Land Records from the SearchIQS Ashford, Connecticut website and exports the collected records to CSV and Google Sheets.

## Features

- Python-based scraping
- Dynamic date range
- Searches the previous 80 days from the current date
- Land Records filtering
- Handles multiple result pages
- Extracts all required record fields
- Removes duplicate records
- Exports results to CSV
- Uploads results to Google Sheets

## Data Extracted

The scraper extracts:

- Party 1
- Party 2
- Type
- Book-Page
- Date
- Description
- Additional Description
- Related

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- gspread
- Google Sheets API

## Project Structure

```text
python-web-scraper/
│
├── scraper.py
├── upload_to_sheet.py
├── requirements.txt
├── README.md
├── .gitignore
├── sample_output.csv
├── results.html
└── results_page2.html