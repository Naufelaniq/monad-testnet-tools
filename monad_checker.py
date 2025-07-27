#!/usr/bin/env python3
import requests
from datetime import datetime

def check_wallet(address, rpc_url="https://testnet-rpc.monad.xyz"):
    try:
        # 1. Fetch MON Balance (in wei)
        balance = requests.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [address, "latest"],
            "id": 1
        }, timeout=10).json()

        # 2. Fetch Transaction Count
        tx_count = requests.post(rpc_url, json={
            "jsonrpc": "2.0",
            "method": "eth_getTransactionCount",
            "params": [address, "latest"],
            "id": 1
        }, timeout=10).json()

        # 3. Convert wei to MON (1 MON = 10^18 wei)
        mon_balance = int(balance['result'], 16) / 10**18

        # 4. Print Results
        print("\n═══════════════════════════════")
        print(f"Address: {address}")
        print(f"MON Balance: {mon_balance} MON")  # Changed ETH to MON
        print(f"Transactions: {int(tx_count['result'], 16)}")
        print(f"Last Checked: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print("═══════════════════════════════\n")

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    import sys
    wallet_address = sys.argv[1] if len(sys.argv) > 1 else "0xaf9e50c42b568f668b5a3b2573c7098e5460d174"
    check_wallet(wallet_address)
