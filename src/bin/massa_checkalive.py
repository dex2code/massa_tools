import json
from sys import exit as sys_exit
from requests import post as r_post


node_api = "http://127.0.0.1:33035/api/v2"

api_header = {
    "content-type": "application/json"
}

api_payload = {
    "id": 0,
    "jsonrpc": "2.0",
    "method": "get_status",
    "params": []
}


def pull_api() -> int:

    try:
        api_resp = r_post(url=node_api, headers=api_header, data=json.dumps(api_payload))
        api_resp = api_resp.json()
    except Exception:
        return 0

    try:
        api_resp = api_resp['result']['chain_id']
        api_resp = int(api_resp)
    except Exception:
        return 0

    return api_resp


def main() -> int:
    api_resp = pull_api()

    if not api_resp:
        print("dead")
        return 1
    else:
        print(api_resp)
        return 0


if __name__ == "__main__":
    sys_exit(main())
