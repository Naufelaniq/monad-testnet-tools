import csv
import sys

def analyze_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        txns = list(reader)

    total_txns = len(txns)
    unique_tokens = set()
    nft_txns = 0
    contract_calls = 0

    for txn in txns:
        method = txn.get("Method", "").lower()
        to_address = txn.get("To", "").lower()

        # Token detection (ERC20/Swap etc.)
        if "token" in method or "swap" in method:
            unique_tokens.add(txn.get("To Token", "").strip())

        # NFT detection (ERC721/1155 etc.)
        if "nft" in method or "erc721" in method or "erc1155" in method:
            nft_txns += 1

        # Contract call
        if method not in ["transfer", "approve"] and method != "":
            contract_calls += 1

    print(f"\n🔍 Txn Fingerprint from CSV file: {file_path}")
    print(f"• Total Transactions: {total_txns}")
    print(f"• Unique Tokens Interacted: {len(unique_tokens)}")
    print(f"• NFT-related Transactions: {nft_txns}")
    print(f"• Smart Contract Interactions: {contract_calls}")

    if total_txns > 100:
        print("• Activity Level: 🔥 High")
    elif total_txns > 20:
        print("• Activity Level: 🟡 Moderate")
    elif total_txns > 0:
        print("• Activity Level: 🟢 Low")
    else:
        print("• Activity Level: ❌ No Activity")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fingerprint_csv.py <csv_file_path>")
    else:
        analyze_csv(sys.argv[1])
