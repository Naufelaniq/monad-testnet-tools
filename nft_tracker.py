import requests
import json
import sys

RPC_URL = "https://restless-smart-gas.monad-testnet.quiknode.pro/95dda28d5846ffed3cc5589f018b94a68431317e"

def rpc(method, params):
    try:
        res = requests.post(RPC_URL, headers={"Content-Type": "application/json"}, data=json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }))
        return res.json()["result"]
    except Exception as e:
        print("RPC Error:", e)
        return None

def track_nfts(address):
    print(f"\n🔍 NFT Transfers for: {address}")
    address = address.lower()

    latest_block = int(rpc("eth_blockNumber", []), 16)
    from_block = hex(latest_block - 100)
    to_block = hex(latest_block)

    logs = rpc("eth_getLogs", [{
        "fromBlock": from_block,
        "toBlock": to_block,
        "topics": ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]
    }])

    if logs is None:
        print("❌ Could not fetch logs")
        return

    nft_logs = [log for log in logs if log.get("address", "") != address]
    print(f"• Total NFT Logs Found: {len(nft_logs)}")

    unique_contracts = set()
    for log in nft_logs:
        unique_contracts.add(log.get("address", ""))

    print(f"• Unique NFT Contracts: {len(unique_contracts)}")
    for contract in unique_contracts:
        print(f"→ {contract}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nft_tracker.py <wallet_address>")
    else:
        track_nfts(sys.argv[1])
