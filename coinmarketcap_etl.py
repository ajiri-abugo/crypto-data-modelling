#import reqiured modules
import requests
import pandas as pd
import json
import csv
import os
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

#not applicable
'''with open("credentials.txt", "r") as f:
    api_key = f.read()'''

api_key = os.getenv('API_KEY')

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

# API endpoint
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

csv_file = 'crypto_data.csv'

# Open the CSV file for writing
with open(csv_file, mode='w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(['id', 'name', 'symbol', 'date_added', 'Price', 'volume_24h', 'volume_change_24h', 'max_supply', 'circulating_supply', 'total_supply', 'infinite_supply', 'cmc_rank', 'last_updated'])
    
    # Making API request
    r = requests.get(url, headers=headers)
    data = r.json
    # print(data)

    if r.status_code == 200:
        data = r.json()
   
        for currency in data['data']:
            id = currency["id"]
            name = currency["name"]
            symbol = currency["symbol"]
            date_added = currency["date_added"]
            Price = currency['quote']['USD']['price']
            volume_24h = currency['quote']['USD']['volume_24h']
            volume_change_24h = currency['quote']['USD']['volume_change_24h']
            max_supply = currency["max_supply"]
            circulating_supply = currency["circulating_supply"]
            total_supply = currency["total_supply"]
            infinite_supply = currency["infinite_supply"]
            cmc_rank = currency["cmc_rank"]
            last_updated = currency["last_updated"]

            writer.writerow([id, name, symbol, date_added, Price, volume_24h, volume_change_24h, max_supply, circulating_supply, total_supply, infinite_supply, cmc_rank, last_updated])

        print(f"Data has been successfull written to csv")

    else:
        print(f"Error: {r.status_code} - {r.text}")

