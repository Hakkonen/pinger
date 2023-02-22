import time, json, math, requests
from discordwebhook import Discord
from functions import xcp

# 777743

def ping(last_read_block):

    # Ping chain for block
    print("Querying chain status")
    running_info = xcp.get_running_info()

    if running_info["last_block"] == "":
        return last_read_block
    else:
        print(str(running_info["last_block"]["block_index"]) + ": " + str(running_info["server_ready"]))

        return running_info["last_block"]["block_index"]

def check_sales(block, asset_index):
    print("Checking for sales from block: " + str(block))

    DIVISION = 500
    asset_matrix = []
    row_count = math.ceil(len(asset_index) / DIVISION)

    # add sub arrays to asset_list
    for x in range(row_count):
        asset_matrix.append([])

    count = 0
    for asset in asset_index:
        # Splits asset into sets of n   
        batch = math.floor(count / DIVISION)
        # print(batch)
        
        asset_matrix[batch].append({"field": "asset", "op": "==", "value": asset["long_name"] })
        count += 1

    # Create list of results
    final_list = []
    for x in range(row_count):
        data = xcp.get_dispenses_by_list(asset_matrix[x], block)

        for dispenser in data:
            final_list.append(dispenser)
    
    # print(filters)
    # sales_data = xcp.get_dispenses_by_list(asset_matrix, block)

    return final_list

def discord_post(text):
    discord = Discord(url="https://discord.com/api/webhooks/1074947631693959259/vDMejPHMg1rJ0KlO37cp3nrueGBFqck5-SAzX-vorJUbu4-YZjJixHXPCYnTQNOeK5G8")
    discord.post(content=text)

def telegram_post(text, token, chatID, method="sendMessage"):
    # tele_api = "https://api.telegram.org/bot5709658070:AAHfgijeOPt6XCL2aDhzRY82_59KDI0v8Yk/sendMessage"
    # token = "5709658070:AAHfgijeOPt6XCL2aDhzRY82_59KDI0v8Yk"
    # method = "sendMessage"

    response = requests.post(
        url="https://api.telegram.org/bot" + token + "/" + method,
        data = {'chat_id': chatID, 'text': text}
    ).json()
    print(response)

# Searches for mint broadcasts and executes them if found
def mint_qf(block_index):

    messages = xcp.get_messages(block_index)

    for message in messages:
        # print(message["text"][:4].lower())
        if message["text"][:14].lower() == "mint questfren":
            print(message["text"])

            # split message
            split_message = message["text"].split()

            number = split_message[2]
            print("QF num: " + str(number))

            if len(split_message) > 3:
                name = split_message[3]
                print("Alias: " + str(name))

            # Post to mint api
            res = requests.get(
                "https://questfrens.herokuapp.com/mint?fren=" + str(number)
            )

            print(res.text)

            time.sleep(4)

            # Push to telegram
            print("Pushing mint to TG")

            # get fren json
            new_fren = requests.get("https://frenzone.net/questfrens/data/" + str(number) + ".json").json()
            print(new_fren["image_large"])

            message = str(new_fren["name"]) + " minted by " + str(new_fren["mint_address"]) + "\n" + str(new_fren["image_large"])

            telegram_post(message, "6274053426:AAHRMdhSFMqKvrCrT1Z-bpW7Dmz-bFoqX-Q", "-1001764091229")

            time.sleep(1)

def app():

    # Load fren data
    fren_index = []
    with open('./data/punklist.json') as f:
        fren_list = json.load(f)
        
        for fren in fren_list:
            new_fren = {
                "name": fren["name"],
                "long_name": fren["a_name"]
            }
            fren_index.append(new_fren)
    

    while True:

        # Set last_read block height
        last_read = 700000

        with open('./data/block_height.json') as f:
            block_stored = json.load(f)
            last_read = block_stored["block"]
        
        print("\nLast read block: " + str(last_read))

        # Ping for current block
        # Returned false if no block_index
        block_index = ping(last_read)

        print("Last read: " + str(last_read))
        print("Block Index: " + str(block_index))
        
        # If index > last read then search for sales within gap
        if block_index > last_read:
            sales_result = check_sales(last_read, fren_index)

            # Check for QF mints
            print("Checking for mint sigs...")
            mint_qf(last_read)

            # Human read print
            for sale in sales_result:

                ## Create sales message
                # 1. Combine asset with human readable name
                for fren in fren_list:
                    if fren["a_name"] == sale["asset"]:
                        sale["name"] = fren["name"]
                        sale["image"] = fren["image_large"]

                # Get dispense value
                dispenser = xcp.get_dispenser_by_tx(sale["dispenser_tx_hash"])
                value = str(dispenser["satoshirate"] / 100000000) + " BTC"

                # Asset name
                asset_link = "[**" + sale["name"] + "**](https://xchain.io/asset/" + sale["name"] + ")"

                # Tx hyperlink
                tx_link = "[Tx Hash](https://xchain.io/tx/" + sale["tx_hash"] + ")"

                message = str("*SOLD*" + "\n" + sale["name"] + " for " + value + " \n" + "TX: " + sale["tx_hash"] + "\n" + "Block: " + str(sale["block_index"]) + "\n" + sale["image"])

                # Push to discord
                print("Pushing: " + str(sale["name"]))
                discord_post(message)

                # Push to telegram
                print("Pushing to TG")
                telegram_post(message, "5709658070:AAHfgijeOPt6XCL2aDhzRY82_59KDI0v8Yk", "-1001808330179" , "sendMessage")

            # Update last read
            last_read = block_index

        else:
            print("Up to date")

        # Write last read block to json
        last_block = {
            "block": last_read
        }

        with open('./data/block_height.json', 'w', encoding='utf-8') as f:
            json.dump(last_block, f, ensure_ascii=False, indent=4)

        # Sleep
        print("")
        print("Sleeping for 10 minutes...")
        time.sleep(600)

## Main
if __name__ == "__main__":
    app()