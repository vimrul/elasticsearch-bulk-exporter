import json
import csv
import requests
from requests.auth import HTTPBasicAuth

# Elasticsearch details
ES_URL = "http://192.168.1.12:9200" # Change this
USERNAME = "your_username"  # Change this
PASSWORD = "your_password"  # Change this
INDEX = "filebeat-*"
QUERY = {
    "size": 5000,  # Fetch 5000 records at a time (reduces memory usage)
    "_source": ["@timestamp", "message"],
    "query": {
        "match_phrase": {
            "message": "*NID API call endpoint*"
        }
    }
}

# Start scroll
response = requests.post(f"{ES_URL}/{INDEX}/_search?scroll=5m", 
                         json=QUERY, 
                         auth=HTTPBasicAuth(USERNAME, PASSWORD))

data = response.json()

# Get scroll ID
scroll_id = data.get("_scroll_id", None)
hits = data["hits"]["hits"]

if not hits:
    print("No data found.")
    exit()

# Open JSON and CSV files for writing
json_file = open("export.json", "w")
csv_file = open("export.csv", "w", newline="")
csv_writer = csv.writer(csv_file)

# Write CSV header
csv_writer.writerow(["timestamp", "message"])

total_records = 0

# Function to save data to files incrementally
def save_data(hits):
    global total_records
    json.dump(hits, json_file, indent=4)  # Save JSON data
    for record in hits:
        csv_writer.writerow([record["_source"]["@timestamp"], record["_source"]["message"]])  # Save CSV data
    total_records += len(hits)
    print(f"Exported {total_records} records so far...")

# Save first batch
save_data(hits)

# Fetch remaining records in a loop
while len(hits) > 0:
    response = requests.post(f"{ES_URL}/_search/scroll", 
                             json={"scroll": "5m", "scroll_id": scroll_id}, 
                             auth=HTTPBasicAuth(USERNAME, PASSWORD))
    
    data = response.json()
    hits = data["hits"]["hits"]

    if hits:
        save_data(hits)

# Close files
json_file.close()
csv_file.close()

# Clear scroll ID to free memory in Elasticsearch
requests.delete(f"{ES_URL}/_search/scroll", 
                json={"scroll_id": scroll_id}, 
                auth=HTTPBasicAuth(USERNAME, PASSWORD))

print(f"Export completed successfully! Total records exported: {total_records}")
