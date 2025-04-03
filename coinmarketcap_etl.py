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
    #load environment variables from .env file
    load_dotenv()

    api_key = os.getenv("API_KEY")

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    # API endpoint
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    # Making API request
    try:
        res = requests.get(url, headers=headers)
        data = res.json()
        # print(data)
        print("Data extracted successfully")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def stream_data():
    while True:
        data = get_data()
        conf = {"bootstrap.servers": "localhost:29092"} 
        producer = Producer(conf)
        if data:
            producer.produce("crypto-data", value=json.dumps(data))
            producer.flush()
            print("Data loaded into kafkaProducer successfully")
        time.sleep(30)
stream_data()
