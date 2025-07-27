import sys
import requests
from bs4 import BeautifulSoup

def analyze_wallet(wallet_address):
    print(f"\n🔍 Txn Fingerprint for wallet: {wallet_address}")

    url = f"https://monad-testnet.socialscan.io/address/{wallet_address}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching data: {e}")
        return

    soup = BeautifulSoup(response.text, "lxml")
    txns = soup.select("a.tx-hash-link")

    if not txns:
        print("🚫 No transactions found.")
        return

    print(f"• Total Transactions Found: {len(txns)}")

    contracts = set()
    tokens_received = 0

    for tx_link in txns[:10]:  # Sirf latest 10 txn check kar rahe
        tx_url = "https://monad-testnet.socialscan.io" + tx_link.get("href")
        tx_page = requests.get(tx_url, headers=headers)
        tx_soup = BeautifulSoup(tx_page.text, "lxml")
        tags = tx_soup.select("a[href*='/address/']")

        for tag in tags:
            address = tag.text.strip()
            if address.lower() != wallet_address.lower():
                contracts.add(address)

        if "Receive" in tx_soup.text:
            tokens_received += 1

    print(f"• Contracts interacted: {len(contracts)}")
    print(f"• Tokens received (latest 10 txns): {tokens_received}")

    if len(contracts) >= 5 and tokens_received >= 2:
        print("• Farming signature: ✅ Probable")
    else:
        print("• Farming signature: ❌ Not strong")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fingerprint.py <wallet_address>")
    else:
        analyze_wallet(sys.argv[1])
