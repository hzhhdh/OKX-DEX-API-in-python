# OKX DEX Price Fetcher (Python)

This Python project fetches the best WETH → USDT swap price from the OKX decentralized exchange (DEX) aggregator API. It uses your OKX API credentials to authenticate and retrieve real-time quotes with slippage tolerance.

---

## Features

- Fetches the current best price for swapping WETH to USDT on Ethereum mainnet via OKX DEX.
- Compares prices across multiple DEXs and shows trade fees.
- Uses HMAC authentication to securely sign API requests.
- Configurable swap amount (default 1 ETH).

---

## Setup

1. Clone this repository or download the files.

2. Install the required Python package:

```bash
pip install requests
```

3. Create an apikeys.json file in the project directory with your OKX API credentials:

```
{
  "API_KEY": "your_api_key_here",
  "SECRET_KEY": "your_secret_key_here",
  "PASSPHRASE": "your_passphrase_here",
  "OKX_PROJECT_ID": "your_project_id_here"
}
```

Make sure you have an OKX API key with appropriate permissions.
---

## Usage
Run the script to fetch the current best WETH to USDT price on OKX DEX:

```
python fetch_dex_prices.py
```
The script will output the price quotes from various DEXs along with their trade fees.

---

## Code Overview
-sign_request(): Signs the request using your secret key and the HMAC SHA256 algorithm.
- get_weth_usdt_price(): Fetches the best quote for swapping WETH to USDT on Ethereum mainnet.
- API request includes slippage tolerance (default 1%).
- Prints detailed price info per DEX.
---

## Notes
- Amounts are converted to wei (smallest ETH unit) before sending.
