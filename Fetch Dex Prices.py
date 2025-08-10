import requests
import time
import hmac
import base64
import json
import os

#fill in your API keys in apikeys.json
current_dir = os.path.dirname(os.path.abspath(__file__))
with open("apikeys.json", "r") as f:
    keys = json.load(f)

api_key = keys["API_KEY"]
secret_key = keys["SECRET_KEY"]
passphrase = keys["PASSPHRASE"]
project_id = keys["OKX_PROJECT_ID"]

#check if API keys are set
print(api_key)

BASE_URL = "https://www.okx.com"
ENDPOINT = "/api/v5/dex/aggregator/quote"

# Ethereum mainnet WETH and USDT contract addresses
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDT_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

def sign_request(method, path, query_string="", body=""):
    """
    Create OKX API signature for authenticated requests
    """
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
    prehash = f"{timestamp}{method}{path}{query_string}{body}"
    signature = base64.b64encode(
        hmac.new(secret_key.encode(), prehash.encode(), digestmod='sha256').digest()
    ).decode()
    return timestamp, signature

def get_weth_usdt_price(amount_eth=1):
    """
    Fetch best WETH -> USDT quote from OKX DEX
    """
    # Amount in wei (1 ETH = 10**18 wei)
    amount_wei = str(int(amount_eth * 10**18))

    params = {
        "chainId": "1",  # Ethereum mainnet
        "fromTokenAddress": WETH_ADDRESS,
        "toTokenAddress": USDT_ADDRESS,
        "amount": amount_wei,
        "slippage": "1"  # 1% slippage tolerance
    }

    query_string = "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    timestamp, signature = sign_request("GET", ENDPOINT, query_string)

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    }

    url = BASE_URL + ENDPOINT
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data.get("data"):
        best_route = data["data"][0]

        quote_compare_list = best_route.get("quoteCompareList", [])
        if not quote_compare_list:
            print("No price comparison data found.")
        else:
            for dex_quote in quote_compare_list:
                dex_name = dex_quote.get("dexName", "Unknown DEX")
                amount_out = dex_quote.get("amountOut", "N/A")
                trade_fee = dex_quote.get("tradeFee", "N/A")
                print(f"{dex_name}: {amount_out} USDT (Trade Fee: {trade_fee})")
    else:
        print("No quote found:", data)

if __name__ == "__main__":
    get_weth_usdt_price(1)
