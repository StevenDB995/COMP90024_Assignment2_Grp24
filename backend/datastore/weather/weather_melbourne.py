import requests
from elasticsearch import Elasticsearch
import csv
from io import StringIO
from datetime import datetime

# Elasticsearch setup
es_client = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    basic_auth=("elastic", "elastic")
)

def upload_to_elasticsearch(data):
    for entry in data:
        es_client.index(index="weather_melbourne", document=entry)

def parse_and_upload_csv(csv_content):
    f = StringIO(csv_content)
    reader = csv.reader(f)
    headers = next(reader)  # First, read the first line which could be a header
    while "Date" not in headers:  # Check if 'Date' is in the header
        headers = next(reader)  # If not, keep reading until we find the correct headers
    # Create a DictReader starting from the current point
    dict_reader = csv.DictReader(f, fieldnames=headers, restval=None)
    data = []
    for row in dict_reader:
        formatted_date = datetime.strptime(row["Date"], "%Y-%m-%d").strftime("%Y-%m-%d")
        try:
            wind_speed = int(row["Speed of maximum wind gust (km/h)"])
        except ValueError:
            wind_speed = 0  # Default value if the conversion fails
        doc = {
            "Date": formatted_date,
            "Rainfall (mm)": float(row["Rainfall (mm)"]),
            "Sunshine (hours)": float(row["Sunshine (hours)"]),
            "Speed of maximum wind gust (km/h)": wind_speed
        }
        data.append(doc)
    upload_to_elasticsearch(data)

def fetch_and_process_csv():
    for year in range(2023, 2025):
        for month in (range(6, 13) if year == 2023 else range(1, 6) if year == 2024 else []):
            url = f"https://reg.bom.gov.au/climate/dwo/{year}{month:02d}/text/IDCJDW3050.{year}{month:02d}.csv"
            response = requests.get(url)
            if response.status_code == 200:
                parse_and_upload_csv(response.text)
            else:
                print(f"Failed to fetch data from {url}, status code: {response.status_code}")

if __name__ == "__main__":
    fetch_and_process_csv()