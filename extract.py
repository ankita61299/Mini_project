import os
import json
import time
import logging
import requests
import psycopg2
from datetime import datetime


# Database connection parameters
DB_PARAMS = {
    "dbname": "RANDOMUSER",
    "user": "ANKITA123",
    "password": "ANKITA",
    "host": "localhost",
    "port": "5432"
}

# API endpoint
API_URL = "https://randomuser.me/api/"

# File storage paths
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
LOGS_PATH = "logs/etl.log"

# Ensure directories exist
os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOGS_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_data():
    """Fetch data from API."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            logging.info("API request successful.")
            return response.json()
        else:
            logging.error(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching data: {str(e)}")
        return None

def store_raw_data(data):
    """Store raw data in JSON file and PostgreSQL."""
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(RAW_DATA_PATH, f"raw_{timestamp}.json")
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO raw_data (data, timestamp) VALUES (%s, %s)
        """, (json.dumps(data), datetime.utcnow()))
        conn.commit()
        cur.close()
        conn.close()
        
        logging.info(f"Raw data saved successfully: {file_path}")
    except Exception as e:
        logging.error(f"Error storing raw data: {str(e)}")

def transform_data(data):
    """Transform data by normalizing structure and formatting timestamps."""
    try:
        transformed = []
        for result in data.get("results", []):
            transformed.append({
                "name": f"{result['name']['first']} {result['name']['last']}",
                "email": result["email"],
                "location": result["location"]["country"],
                "dob": datetime.strptime(result["dob"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ").isoformat()
            })
        logging.info("Data transformation successful.")
        return transformed
    except Exception as e:
        logging.error(f"Error transforming data: {str(e)}")
        return []

def store_transformed_data(transformed_data):
    """Store transformed data in JSON file."""
    try:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(PROCESSED_DATA_PATH, f"processed_{timestamp}.json")
        with open(file_path, "w") as file:
            json.dump(transformed_data, file, indent=4)
        logging.info(f"Transformed data saved successfully: {file_path}")
    except Exception as e:
        logging.error(f"Error storing transformed data: {str(e)}")

def etl_pipeline():
    """Run the ETL pipeline every 30 seconds."""
    while True:
        data = fetch_data()
        if data:
            store_raw_data(data)
            transformed = transform_data(data)
            store_transformed_data(transformed)
        time.sleep(30)

if __name__ == "__main__":
    etl_pipeline()
