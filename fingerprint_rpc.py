import sys
import requests
import json

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

def analyze_wallet(address):
    print(f"\n🔍 Real Txn Fingerprint for: {address}")
    address = address.lower()

    latest_block_hex = rpc("eth_blockNumber", [])
    if not latest_block_hex:
        print("❌ Failed to fetch latest block")
        return
    latest_block = int(latest_block_hex, 16)
    print(f"• Latest Block: {latest_block}")

    from_block = hex(latest_block - 100)  # ❗ Limit = 100 blocks only
    to_block = hex(latest_block)

    logs = rpc("eth_getLogs", [{
        "fromBlock": from_block,
        "toBlock": to_block,
        "topics": [],
    }])

    if logs is None:
        print("❌ Could not fetch logs")
        return

    total_logs = 0
    token_transfers = 0
    contract_addresses = set()

    for log in logs:
        total_logs += 1
        topics = log.get("topics", [])
        addr = log.get("address", "").lower()

        if topics and topics[0].lower().startswith("0xddf252ad"):
            token_transfers += 1

        if addr and addr != address:
            contract_addresses.add(addr)

    print(f"• Total Logs: {total_logs}")
    print(f"• Token Transfers: {token_transfers}")
    print(f"• Contract Interactions: {len(contract_addresses)}")

    if total_logs > 200:
        print("• Activity Level: 🔥 Very High")
    elif total_logs > 50:
        print("• Activity Level: 🟡 Moderate")
    elif total_logs > 0:
        print("• Activity Level: 🟢 Low")
    else:
        print("• Activity Level: ❌ No Activity")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fingerprint_rpc.py <wallet_address>")
    else:
        analyze_wallet(sys.argv[1])
