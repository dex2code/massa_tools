import json
from requests import post as r_post
from sys import exit as sys_exit
from dotenv import load_dotenv
from pathlib import Path
from os import getenv as os_getenv


home_path = str(Path.home())
env_path = Path(f"{home_path}/.massa_profile")

api_url = "http://127.0.0.1:33035/api/v2"

api_header = {
    "content-type": "application/json"
}

api_payload = {
    "id": 0,
    "jsonrpc": "2.0",
    "method": "get_addresses",
    "params": []
}


def pull_api() -> object:
    try:
        api_resp = r_post(url=api_url, headers=api_header, data=json.dumps(api_payload))
        api_resp = api_resp.json()
    except Exception:
        return {"error": "exception"}
    else:
        return api_resp


def main() -> int:

    try:
        load_dotenv(dotenv_path=env_path)
        massa_wallet = os_getenv(key="MASSA_WALLET")
        massa_wallet = str(massa_wallet)
    except Exception:
        print(0)
        return 1

    if massa_wallet == "" or massa_wallet == "None":
        print(0)
        return 1

    #Get stakers balance
    api_payload["params"] = [[massa_wallet]]
    api_resp = pull_api()

    try:
        staker_final_balance = api_resp['result'][-1]['final_balance']
        staker_final_balance = float(staker_final_balance)
        staker_final_balance = int(staker_final_balance)
    except Exception:
        print(0)
        return 1

    print(staker_final_balance)
    return 0


if __name__ == "__main__":
    sys_exit(main())
