#import reqiured modules
from dotenv import load_dotenv
from confluent_kafka import Producer
import requests
import pandas as pd
import json
import csv
import os
import time

def get_data():
    # Load environment variables from .env file
    load_dotenv()

    api_key = os.getenv("API_KEY")

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            raw_data = res.json()
            filtered_data = []

            for currency in raw_data['data']:
                filtered_currency = {
                    "id": currency["id"],
                    "name": currency["name"],
                    "symbol": currency["symbol"],
                    "date_added": currency["date_added"],
                    "price": currency["quote"]["USD"]["price"],
                    "volume_24h": currency["quote"]["USD"]["volume_24h"],
                    "volume_change_24h": currency["quote"]["USD"]["volume_change_24h"],
                    "max_supply": currency["max_supply"],
                    "circulating_supply": currency["circulating_supply"],
                    "total_supply": currency["total_supply"],
                    "infinite_supply": currency["infinite_supply"],
                    "cmc_rank": currency["cmc_rank"],
                    "last_updated": currency["last_updated"]
                }
                filtered_data.append(filtered_currency)

            print("Filtered data extracted successfully.")
            return filtered_data
        else:
            print(f"API error: {res.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def stream_data():
    while True:
        data = get_data()
        conf = {"bootstrap.servers": "localhost:29092"} 
        producer = Producer(conf)
        if data:
            producer.produce("crypto-data", value=json.dumps(data, indent=4))
            producer.flush()
            print("Data loaded into kafkaProducer successfully")
        time.sleep(10)
stream_data()
