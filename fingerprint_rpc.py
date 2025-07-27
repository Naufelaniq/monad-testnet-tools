import sys
import requests
import json

def fetch_logs(address):
    print(f"\n🔍 Live Fingerprint for: {address}")

    rpc_url = "https://rpc.testnet.monad.xyz"  # Public Monad Testnet RPC
    headers = {"Content-Type": "application/json"}

    # Get latest block
    payload_block = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }

    try:
        response = requests.post(rpc_url, headers=headers, json=payload_block)
        latest_block_hex = response.json()["result"]
        latest_block = int(latest_block_hex, 16)
        print(f"• Latest Block: {latest_block}")

        # Set smaller range
        from_block = hex(latest_block - 2000)
        to_block = latest_block_hex

        # Fetch logs
        payload_logs = {
            "jsonrpc": "2.0",
            "method": "eth_getLogs",
            "params": [{
                "fromBlock": from_block,
                "toBlock": to_block,
                "address": address
            }],
            "id": 2
        }

        log_response = requests.post(rpc_url, headers=headers, json=payload_logs)
        log_data = log_response.json().get("result", [])

        if not log_data:
            print("• No logs found in last 2000 blocks.")
        else:
            print(f"• Logs Found: {len(log_data)}")
            for i, log in enumerate(log_data[:5], 1):  # show max 5 logs
                print(f"  {i}. Block: {int(log['blockNumber'], 16)} | Txn: {log['transactionHash'][:10]}...")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fingerprint_rpc.py <wallet_address>")
        sys.exit(1)

    fetch_logs(sys.argv[1])
