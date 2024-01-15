import json
from requests import post as r_post
from sys import exit as sys_exit
from dotenv import load_dotenv
from pathlib import Path
from os import getenv as os_getenv


debug = False

home_path = str(Path.home())
env_path = Path(f"{home_path}/.massa_profile")

api_url = "http://127.0.0.1:33035/api/v2"

api_header = {
    "content-type": "application/json"
}

api_payload = {
    "id": 0,
    "jsonrpc": "2.0",
    "method": "",
    "params": []
}


def pull_api() -> object:
    try:
        api_resp = r_post(url=api_url, headers=api_header, data=json.dumps(api_payload))
        api_resp = api_resp.json()

    except Exception as E:
        if debug:
            print(f"\n API error: ({str(E)})")

        return {"error": "exception"}

    else:
        return api_resp


def main() -> int:
    if debug:
        print(f"\n Running main()")
        print(f"\n Loading '{env_path}' file")

    try:
        load_dotenv(dotenv_path=env_path)

        massa_wallet = os_getenv(key="MASSA_WALLET")
        massa_wallet = str(massa_wallet)

        massa_fee = os_getenv(key="MASSA_FEE")
        massa_fee = int(massa_fee)

    except Exception as E:
        if debug:
            print(f"\n Error loading '{env_path}' file or keys: ({str(E)})")

        print(0)
        return 1

    else:
        if debug:
            print(f"\n Loaded '{env_path}' file successfully!")


    if massa_wallet == "" or massa_wallet == "None":
        if debug:
            print(f"\n Error loading massa_wallet key: {massa_wallet=}")
        print(0)
        return 1

    if debug:
        print(f"\n {massa_wallet=}")
        print(f"\n {massa_fee=}")

    #Get Roll price
    api_payload['method'] = 'get_status'
    api_payload["params"] = []

    if debug:
        print(f"\n Entering pull_api() with {api_url=}, {api_header=}, {api_payload=}")

    api_resp = pull_api()

    if debug:
        print(f"\n Received {api_resp=}")

    try:
        roll_price = api_resp['result']['config']['roll_price']
        roll_price = float(roll_price)
        roll_price = int(roll_price)

    except Exception as E:
        if debug:
            print(f"\n Error loading roll_price: ({str(E)})")
        print(0)
        return 1

    else:
        if debug:
            print(f"\n {roll_price=}")

    #Get staker balance
    api_payload['method'] = 'get_addresses'
    api_payload["params"] = [[massa_wallet]]

    if debug:
        print(f"\n Entering pull_api() with {api_url=}, {api_header=}, {api_payload=}")

    api_resp = pull_api()

    if debug:
        print(f"\n Received {api_resp=}")

    try:
        staker_balance = api_resp['result'][-1]['final_balance']
        staker_balance = float(staker_balance)
        staker_balance = int(staker_balance)

    except Exception as E:
        if debug:
            print(f"\n Error loading roll_price: ({str(E)})")
        print(0)
        return 1

    else:
        if debug:
            print(f"\n {staker_balance=}")

    #Calculate Rolls to buy
    if (staker_balance - massa_fee) <= roll_price:
        print(0)
        return 0

    try:
        number_rolls = (staker_balance - massa_fee) // roll_price
        number_rolls = int(number_rolls)

    except Exception as E:
        if debug:
            print(f"\n Error calculating number_rolls: ({str(E)})")
        print(0)
        return 1

    else:
        print(number_rolls)

    return 0


if __name__ == "__main__":
    sys_exit(main())
