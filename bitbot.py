import requests
import json
import time
from typing import List
import csv

api_key = "Etherscan API key, see readme, wassie."
base_url = "https://api.etherscan.io/api"


# Your API key (replace with your actual key)
API_KEY = "YourApiKeyToken"

BASESCANAPI_URL = "https://api.basescan.org/api"

def basescan_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_friendtech_addresses(ADDRESS):
    url = f"{BASESCANAPI_URL}?module=account&action=txlist&address={ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
    api_response = basescan_api(url)
    
    unique_to_addresses = set()  # Using a set to automatically handle deduplication

    if api_response and api_response.get('status') == "1":
        transactions = api_response.get('result', [])
        
        if transactions:
            for transaction in transactions:
                from_address = transaction.get("from", "Unknown")
                to_address = transaction.get("to", "Unknown")
                
                if from_address != to_address:
                    unique_to_addresses.add(to_address)
                    
                    
        else:
            print("No transactions found.")
    else:
        print("Nothing on BaseScan.")

    # Checking the first transaction for each unique TO address
    final_addresses = []
    for to_address in unique_to_addresses:
        url = f"{BASESCANAPI_URL}?module=account&action=txlist&address={to_address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}&page=1&offset=1"
        api_response = basescan_api(url)
        
        if api_response and api_response.get('status') == "1":
            transactions = api_response.get('result', [])
            
            if transactions:
                first_transaction = transactions[0]
                if first_transaction.get("from") == ADDRESS:
                    final_addresses.append(to_address)
                    print(f"Found Base address initiated by the last address: {to_address}")
    
    return final_addresses

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
    #print(f"Fetching with headers: {headers}")  # Debugging line to check headers
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"No FriendTech user for {address}")
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
            #processed_data.append({'address': address, 'data': {"message": "Address/User not found."}})
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
    
    auth_token = "FriendTech JWT token, see readme wassiefren"


    print("Fetching all transactions... 🕵️‍♀️")
    data = fetch_token_transactions(target_address, api_key, base_url)
    
    print("Extracting sender addresses... 🎯")
    senders = list(extract_senders(data, target_address))
    
    print("Going to BaseScan to find possible FriendTech addresses... 🛰️")
    friendtech_senders = []  # Empty list to hold the converted addresses
    
    for sender in senders:
        print(f"Checking {sender}:")
        friendtech_address = get_friendtech_addresses(sender)  # Convert each sender to its FriendTech version
        if friendtech_address:  # If conversion is successful, add to list
            friendtech_senders.extend(friendtech_address)
    
    print("Fetching and processing user info... 🎭")
    processed_data = fetch_and_process(friendtech_senders, auth_token)  # Use the converted addresses
    
    if processed_data:
        print("Successfully fetched user info:")
        print(json.dumps(processed_data, indent=4))
        
        print("Writing to CSV... 📝")
        write_to_csv(processed_data)
    else:
        print(f"No user info found. It's like a ghost town in here! 👻")
if __name__ == "__main__":
    main()
