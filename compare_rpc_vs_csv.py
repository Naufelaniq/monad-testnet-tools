import csv
import sys
import requests
import json

CSV_PATH = "transactions-0xaf9e50c42b568f668b5a3b2573c7098e5460d174-20250727100730.csv"
QUICKNODE_RPC = "https://restless-smart-gas.monad-testnet.quiknode.pro/95dda28d5846ffed3cc5589f018b94a68431317e"

def rpc(method, params):
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        headers = {"Content-Type": "application/json"}
        res = requests.post(QUICKNODE_RPC, headers=headers, data=json.dumps(payload))
        return res.json()["result"]
    except Exception as e:
        print(f"⚠️ RPC Error: {e}")
        return None

def analyze_csv():
    try:
        with open(CSV_PATH, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            txns = list(reader)

        total_txns = len(txns)
        unique_addresses = set()
        token_transfers = 0

        for txn in txns:
            to = txn.get("to", "").lower().strip()
            if to:
                unique_addresses.add(to)

        return {
            "txns": total_txns,
            "unique": len(unique_addresses),
        }
    except Exception as e:
        print(f"❌ CSV Error: {e}")
        return None

def analyze_rpc():
    latest_block_hex = rpc("eth_blockNumber", [])
    latest_block = int(latest_block_hex, 16)
    from_block = hex(latest_block - 100)
    to_block = hex(latest_block)

    logs = rpc("eth_getLogs", [{
        "fromBlock": from_block,
        "toBlock": to_block,
        "topics": [],
    }])

    if logs is None:
        return None

    token_transfers = 0
    unique_addresses = set()

    for log in logs:
        topics = log.get("topics", [])
        log_address = log.get("address", "").lower()
        if topics and topics[0].lower().startswith("0xddf252ad"):
            token_transfers += 1
        unique_addresses.add(log_address)

    return {
        "logs": len(logs),
        "tokens": token_transfers,
        "unique": len(unique_addresses),
    }

if __name__ == "__main__":
    print("\n🔍 Comparing CSV vs RPC data...")

    csv_data = analyze_csv()
    rpc_data = analyze_rpc()

    if csv_data and rpc_data:
        print("\n📊 CSV Explorer Data:")
        print(f"• Total Transactions: {csv_data['txns']}")
        print(f"• Unique To Addresses: {csv_data['unique']}")

        print("\n🌐 Live RPC Data:")
        print(f"• Total Logs: {rpc_data['logs']}")
        print(f"• Token Transfers: {rpc_data['tokens']}")
        print(f"• Unique Addresses: {rpc_data['unique']}")
    else:
        print("❌ Data comparison failed.")
