import json
from requests import post as r_post
from sys import exit as sys_exit
from dotenv import load_dotenv
from pathlib import Path
from os import getenv as os_getenv


home_path = str(Path.home())
env_path = Path(f"{home_path}/.massa_profile")

node_api = "http://127.0.0.1:33035/api/v2"

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
        api_resp = r_post(url=node_api, headers=api_header, data=json.dumps(api_payload))
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

    if massa_wallet == "" or massa_wallet == "None" or massa_wallet is None:
        print(0)
        return 1

    #Get stakers active rolls
    api_payload["params"] = [[massa_wallet]]
    api_resp = pull_api()

    try:
        staker_active_rolls = api_resp['result'][-1]['cycle_infos'][-1]['active_rolls']
        if staker_active_rolls is None:
            staker_active_rolls = 0
        staker_active_rolls = int(staker_active_rolls)
    except Exception:
        print(0)
        return 1

    print(staker_active_rolls)
    return 0


if __name__ == "__main__":
    sys_exit(main())
