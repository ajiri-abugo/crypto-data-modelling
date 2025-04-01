#import reqiured modules
from dotenv import load_dotenv
from confluent_kafka import Producer
import requests
import pandas as pd
import json
import csv
import os


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
    r = requests.get(url, headers=headers)
    data = r.json()
    # print(data)
    print("Data extracted successfully")
    return data

def stream_data(data):
    conf = {"bootstrap.servers": "localhost:9092"}

    producer = Producer(conf)

    producer.produce(topic="crypto-data", value=json.dumps(data))

    producer.flush()
    print("Data loaded into kafkaProducer successfully")
data = get_data()
stream_data(data)
