import sys
import requests

def analyze_wallet(wallet_address):
    print(f"\n🔍 Live Txn Fingerprint for wallet: {wallet_address}")

    url = f"https://api.layerhub.xyz/api/wallet/{wallet_address}?chain=monad_testnet"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        txns = data.get("txs", [])
        tokens = data.get("tokens", [])
        nfts = data.get("nfts", [])
        contracts = [tx for tx in txns if tx.get("method") not in [None, "", "transfer"]]

        print(f"• Total Transactions: {len(txns)}")
        print(f"• Tokens Held: {len(tokens)}")
        print(f"• NFTs Held: {len(nfts)}")
        print(f"• Smart Contract Interactions: {len(contracts)}")

        if len(txns) > 500:
            print("• Activity Level: 🔥 Very High")
        elif len(txns) > 100:
            print("• Activity Level: 🔥 High")
        elif len(txns) > 20:
            print("• Activity Level: 🟡 Moderate")
        elif len(txns) > 0:
            print("• Activity Level: 🟢 Low")
        else:
            print("• Activity Level: ❌ No Activity")

    except Exception as e:
        print("⚠️ Error:", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fingerprint_live.py <wallet_address>")
    else:
        analyze_wallet(sys.argv[1])
