# SearchIQS Ashford Land Records Scraper

A Python-based web scraping project developed for the Adoraxe Python Web Scraper Challenge.

The project extracts Land Records from the SearchIQS Ashford, Connecticut website and exports the collected records to CSV and Google Sheets.

## Features

- Python-based web scraping
- Dynamic 80-day date range
- Land Records filtering
- Multiple-page result handling
- Extraction of all required fields
- Duplicate removal
- CSV export
- Google Sheets export

## Data Extracted

- Party 1
- Party 2
- Type
- Book-Page
- Date
- Description
- Additional Description
- Related

## Technologies

- Python
- Requests
- BeautifulSoup
- Pandas
- gspread
- Google Authentication
- Google Sheets API

## Project Structure

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

## Installation

Install the required dependencies:

pip install -r requirements.txt

## Running the Scraper

Run:

python scraper.py

The date range is calculated dynamically using the current date and the previous 80 days.

The extracted records are saved to:

sample_output.csv

## Google Sheets Export

Google Sheets export uses a Google Cloud service account.

Place the service account credentials locally as:

credentials.json

Run:

python upload_to_sheet.py

The credentials file is excluded from version control through .gitignore.

## Results

The completed test run produced:

Page 1: 100 records
Page 2: 55 records
Total: 155 records
Unique records: 155

## Google Sheet

The scraped records are available here:

[Google Sheet - SearchIQS Ashford Land Records] (https://docs.google.com/spreadsheets/d/1Dvbo3yjN5x2nwxxmwppzpYuvXQUJ18JGGPe_-krwCXc/edit?usp=sharing)

## Challenge Compliance

- Python used
- Selenium not used
- Playwright not used
- Puppeteer not used
- Dates calculated dynamically
- Pagination handled
- Required fields extracted