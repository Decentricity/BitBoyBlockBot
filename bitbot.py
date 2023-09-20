import requests
import json
import time
from typing import List
import csv

api_key = "Etherscan API key, see readme, wassie."
base_url = "https://api.etherscan.io/api"

def write_to_csv(data):
    with open('bitbot.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Writing the header row
        writer.writerow(["ADDRESS", "JSON DATA"])
        
        for item in data:
            address = item.get('address', 'N/A')
            json_data = item.get('data', {})
            # Writing each row
            writer.writerow([address, json.dumps(json_data)])


def fetch_user_info(address: str, auth_token: str):
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Referer': 'https://www.friend.tech/',
        'User-Agent': 'curl/7.64.1'
    }
    
    url = f"https://prod-api.kosetto.com/users/{address}"
    #print(f"Fetching with headers: {headers}")  # Debugging line to check headers aw
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for address {address}: {response.status_code}, {response.text}")
        return None


def fetch_and_process(senders: List[str], auth_token: str):
    processed_data = []
    for address in senders:
        print(f"Fetching info for address {address}... 🚀")
        user_info = fetch_user_info(address, auth_token)
        
        if user_info:
            print(f"Successfully fetched data for {address}")
            processed_data.append({'address': address, 'data': user_info})
        else:
            print(f"No friendtech / twatter username for {address}")
            processed_data.append({'address': address, 'data': {"message": "Address/User not found."}})
        # Optional: rate-limiting, so we don't overwhelm the API.
        time.sleep(0.1)
    return processed_data


def fetch_token_transactions(address, api_key, base_url):
    payload = {
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    
    response = requests.get(base_url, params=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def extract_senders(data, target_address):
    senders = set()
    if data is not None and 'result' in data:
        for tx in data['result']:
            if tx['to'].lower() == target_address.lower():
                senders.add(tx['from'])
    return senders


def main():
    target_address = "0xa6079bC88540cC9360D3c8D6f9cE583cdCcC3dC6" #Bitboy's addie
    
    auth_token = "[FriendTech JWT token, see readme wassiefren]"

    print("Fetching transactions wit ze etherscan... 🕵️‍♀️")
    data = fetch_token_transactions(target_address, api_key, base_url)
    
    print("Extracting sender addies aw... 🎯")
    senders = list(extract_senders(data, target_address))
    
    print("Fetching n processing user info... 🎭")
    processed_data = fetch_and_process(senders, auth_token)
    
    if processed_data:
        print("Successful wassie has fetched user info:")
        print(json.dumps(processed_data, indent=4))
        
        print("Writing to CSV... 📝")
        write_to_csv(processed_data)
    else:
        print(f"No user info found. Dis fridge is liek a ghost town! 👻")
    
if __name__ == "__main__":
    main()
