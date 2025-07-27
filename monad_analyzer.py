#!/usr/bin/env python3
"""
Monad Blockchain Analyzer
- Wallet Monitoring
- Transaction Analysis
- NFT Detection
- Gas Tracker
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
RPC_URL = "https://testnet-rpc.monad.xyz"
ETHERSCAN_API = ""  # Optional for full history

class MonadAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def rpc_call(self, method, params=[]):
        """Generic RPC call handler"""
        try:
            response = self.session.post(
                RPC_URL,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": method,
                    "params": params
                },
                timeout=15
            )
            response.raise_for_status()
            return response.json().get("result")
        except Exception as e:
            print(f"RPC Error: {str(e)}")
            return None

    def analyze_wallet(self, address):
        """Complete wallet analysis"""
        print(f"\n{' Monad Blockchain Analyzer ':=^50}")
        print(f"📅 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"👛 {address}\n")

        # 1. Basic Info
        self.show_balance(address)
        self.show_transaction_count(address)
        
        # 2. Advanced Features
        self.show_recent_activity(address)
        self.detect_nfts(address)
        self.check_gas_prices()

    def show_balance(self, address):
        if balance := self.rpc_call("eth_getBalance", [address, "latest"]):
            print(f"💰 Balance: {int(balance, 16)/10**18:.6f} MONAD")

    def show_transaction_count(self, address):
        if tx_count := self.rpc_call("eth_getTransactionCount", [address, "latest"]):
            print(f"📜 Transactions: {int(tx_count, 16)}")

    def show_recent_activity(self, address):
        if block := self.rpc_call("eth_getBlockByNumber", ["latest", True]):
            print("\n🔥 Recent Activity:")
            for tx in block.get('transactions', [])[:5]:
                if tx['from'].lower() == address.lower():
                    print(f"  ↪️ Sent {int(tx['value'], 16)/10**18:.4f} MONAD")
                elif tx.get('to', '').lower() == address.lower():
                    print(f"  ↩️ Received {int(tx['value'], 16)/10**18:.4f} MONAD")

    def detect_nfts(self, address):
        print("\n🖼️ NFT Detection:")
        if code := self.rpc_call("eth_getCode", [address, "latest"]):
            print("  ✅ Smart Contract Detected" if code != "0x" else "  ❌ No NFTs Found")

    def check_gas_prices(self):
        if gas := self.rpc_call("eth_gasPrice"):
            print(f"\n⛽ Current Gas: {int(gas, 16)/10**9:.2f} Gwei")

if __name__ == "__main__":
    analyzer = MonadAnalyzer()
    
    if len(sys.argv) > 1:
        analyzer.analyze_wallet(sys.argv[1].lower())
    else:
        print("Usage: python monad_analyzer.py 0xYourAddress")
        print("Example: python monad_analyzer.py 0xaf9e50c42b568f668b5a3b2573c7098e5460d174")
