#!/usr/bin/env python3
import requests
from termcolor import colored
from datetime import datetime

# Colors
G = lambda x: colored(x, 'green')
Y = lambda x: colored(x, 'yellow')
B = lambda x: colored(x, 'blue')
R = lambda x: colored(x, 'red')

def check_wallet(address):
    try:
        # Data fetch karo
        balance = requests.post(
            "https://testnet-rpc.monad.xyz",
            json={
                "jsonrpc":"2.0",
                "method":"eth_getBalance",
                "params":[address,"latest"],
                "id":1
            }, timeout=10
        ).json()
        
        tx_count = requests.post(
            "https://testnet-rpc.monad.xyz",
            json={
                "jsonrpc":"2.0",
                "method":"eth_getTransactionCount",
                "params":[address,"latest"],
                "id":1
            }, timeout=10
        ).json()

        # Result show karo
        print(f"\n{B('═══ MONAD WALLET CHECKER ═══')}")
        print(f"{G('✓ Address:')} {address}")
        print(f"{G('✓ Balance:')} {Y(str(int(balance['result'],16)/10**18)+' ETH')}")
        print(f"{G('✓ Transactions:')} {Y(tx_count['result'])}")
        print(f"{G('✓ Last Checked:')} {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print(B('═══════════════════════════════\n'))

    except Exception as e:
        print(f"\n{R('✗ Error:')} {str(e)}")

if __name__ == "__main__":
    import sys
    wallet = sys.argv[1] if len(sys.argv)>1 else "0xaf9e50c42b568f668b5a3b2573c7098e5460d174"
    check_wallet(wallet)
