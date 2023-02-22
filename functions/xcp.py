import json
from webbrowser import get
import requests
import json
from requests.auth import HTTPBasicAuth

# RPC 2.0 Headers -- Counterparty
url = "http://api.counterparty.io:4000/api/"
headers = {"content-type": "application/json"}
auth = HTTPBasicAuth("rpc", "rpc")

# RPC 2.0 Headers -- Coindaddy
COINDADDY = {
    "url": "http://public.coindaddy.io:4000/api/",
    "headers": {"content-type": "application/json"},
    "auth": HTTPBasicAuth("rpc", "1234")
}

# # RPC 2.0 Headers -- Counterparty
# url = "http://localhost:4000/api/"
# headers = {"content-type": "application/json"}
# auth = HTTPBasicAuth("rpc", "rpc")

#################################################
## Filter params
# get_:
#   asset_longname / block_index / 

TIMER = 200

#################################################
# Takes in list of names and returns asset info
#   Accepts longname as name if asset is subasset
def get_asset_info(asset):

    payload = {
        "method": "get_asset_info",
        "params": {
            "assets": asset # asset id?
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    ## Returns:
    #   {'asset': 'LEPEPENOIR', 'asset_longname': None, 'owner': '1EWFR9dMzM2J', 'divisible': False, 
    #   'locked': True, 'supply': 21, 'description': 'https://fakeasf.', 'issuer': '1EWFR9d5'}
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=TIMER)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()

    return data["result"]

#################################################
# Takes in asset and block number and return asset id and names
def get_asset(asset, block=280000):
    payload = {
        "method": "get_assets",
        "params": {
            "filters": 
                [
                    {"field": "asset_name", "op": "==", "value": asset },
                    {"field": "block_index", "op": ">", "value": block }
                ],
                "filterop": "AND"
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    ## Returns:
    # {'asset_id': '363785', 'asset_name': 'USDT', 'block_index': 297420, 'asset_longname': None,

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()
    return data["result"]

# print(get_asset("LEPEPENOIR"))

#################################################
# Takes in asset of dispensers and return dispenser list
def get_dispensers(asset, block=280000):
    payload = {
        "method": "get_dispensers",
        "params": {
            "filters": [
                {"field": "asset", "op": "==", "value": asset }
            ],
            "start_block": block,
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    ## Returns:
    #   {'tx_index': 1718598, 'tx_hash': '6510c11de5b7384e3d1675aba56a0a085b7ac075293aff2eb67e6b65fad7e2f1', 'block_index': 702997, 
    #   'source': '1BUnu1i5KHTRW5hv38XLEEVv7JqM9ecN2j', 'asset': 'VINCEMCPEPE', 'give_quantity': 1, 'escrow_quantity': 1, 'satoshirate': 180000, 
    #   'status': 10, 'give_remaining': 0}

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()

    return data["result"]

# Get dispenser by tx
def get_dispenser_by_tx(tx_hash, block=700000):
    
    payload = {
        "method": "get_dispensers",
        "params": {
            "filters": [
                {"field": "tx_hash", "op": "==", "value": tx_hash }
            ],
            "start_block": block,
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    ## Returns:
    #   {'tx_index': 1718598, 'tx_hash': '6510c11de5b7384e3d1675aba56a0a085b7ac075293aff2eb67e6b65fad7e2f1', 'block_index': 702997, 
    #   'source': '1BUnu1i5KHTRW5hv38XLEEVv7JqM9ecN2j', 'asset': 'VINCEMCPEPE', 'give_quantity': 1, 'escrow_quantity': 1, 'satoshirate': 180000, 
    #   'status': 10, 'give_remaining': 0}

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()
    
    return data["result"][0]

#################################################
# Takes in asset and returns dispense tx related
def get_dispenses(asset, block=700000):
    payload = {
        "method": "get_dispenses",
        "params": {
            "filters": 
                [
                    {"field": "asset", "op": "==", "value": asset },
                ],
            "order_by": "tx_index",
            "order_dir": "ASC",
            "start_block": block,
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    ## Returns:
    #   {'tx_index': 1775857, 'dispense_index': 0, 'tx_hash': '545c5076188affd36bb00f2cc5c2cfe3ba0c6f499dccc407496f0ea883660419', 'block_index': 708829, 
    #   'source': '1AWBGoa6cnda92Rxmo1QpsoPE3rvbPsqf7', 'destination': '14udFRS6AdnQNJZn9RZ1H3LtSqP7k2UeTC', 'asset': 'BITPAPER', 
    #   'dispense_quantity': 30000000000000, 'dispenser_tx_hash': '9a8e957e6823355fcc2e489579cedc5ba38e10865282e606847448c858fa80de'}

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()
    
    return data["result"]

# print(get_dispensers("LEPEPENOIR"))

# Takes in asset list and returns dispense tx related
def get_dispenses_by_list(assets, block=700000):

    payload = {
        "method": "get_dispenses",
        "params": {
            "filters": 
                assets,
            "filterop": "OR",
            "order_by": "tx_index",
            "order_dir": "ASC",
            "start_block": block,
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    ## Returns:
    #   {'tx_index': 1775857, 'dispense_index': 0, 'tx_hash': '545c5076188affd36bb00f2cc5c2cfe3ba0c6f499dccc407496f0ea883660419', 'block_index': 708829, 
    #   'source': '1AWBGoa6cnda92Rxmo1QpsoPE3rvbPsqf7', 'destination': '14udFRS6AdnQNJZn9RZ1H3LtSqP7k2UeTC', 'asset': 'BITPAPER', 
    #   'dispense_quantity': 30000000000000, 'dispenser_tx_hash': '9a8e957e6823355fcc2e489579cedc5ba38e10865282e606847448c858fa80de'}

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()
    
    return data["result"]

#################################################
# Takes in address and returns balances for address
def get_balances(address):
    payload = {
        "method": "get_balances",
        "params": {
            "filters": [
                {"field": "address", "op": "==", "value": address},
                {"field": "quantity", "op": ">", "value": 0},
            ],
            "filterop": "AND",
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    ## Returns:
    #   {'address': '1EWFR9dMzM2JtrXeqwVCY1LW6KMZ1iRhJ5', 'asset': 'YVESPEPKLEIN', 'quantity': 28}

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=TIMER)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()

    return data["result"]

#################################################
# Get asset names
def get_names(block=708000):
    payload = {
        "method": "get_asset_names",
        "params": {
            # "filters": [
            #     {"field": "block_index", "op": ">", "value": block},
            # ],
        },
        "jsonrpc": "2.0",
        "id": 0,
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=TIMER)

    if "Response [503]" in str(response):   
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()

    return data["result"]

#################################################   
# Get asset holders
def get_holders(asset):
    payload = {
        "method": "get_holders",
        "params": {
            "asset": asset
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=TIMER)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()

    return data["result"]

#################################################   
# Get address balance
def get_balances(address):
    payload = {
        "method": "get_balances",
        "params": {
            "filters": [
                {"field": "address", "op": "==", "value": address},
                {"field": "quantity", "op": ">", "value": "0"},
            ],
            "filterop": "AND",
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=TIMER)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()
    return data["result"]

# print(get_balances("1EWFR9dMzM2JtrXeqwVCY1LW6KMZ1iRhJ5"))

def get_running_info():
    payload = {
        "method": "get_running_info",
        "params": {},
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=TIMER)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()
    print(data)
    return data["result"]

def get_messages(block_index):
    payload = {
        "method": "get_broadcasts",
        "params": {
            "filters": [
                # {"field": "address", "op": "==", "value": address},
                {"field": "block_index", "op": ">", "value": block_index},
            ],
            # "filterop": "AND",
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=TIMER)

    if "Response [503]" in str(response):
        print("trying coindaddy")
        response = requests.post(COINDADDY["url"], data=json.dumps(payload), headers=headers, auth=COINDADDY["auth"])

    data = response.json()
    # print(data)
    return data["result"]