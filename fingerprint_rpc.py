#!/usr/bin/env python3
import requests
import json
import argparse
from web3 import Web3
from datetime import datetime
import sys

# Configuration
DEFAULT_RPC_URLS = [
    "https://testnet-rpc.monad.xyz",  # Primary official endpoint
    "https://rpc.ankr.com/monad_testnet",  # Reliable backup
    "wss://monad-testnet.drpc.org"  # WebSocket alternative
]

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_working_rpc(rpc_urls):
    """Test RPC endpoints and return the first working one"""
    for url in rpc_urls:
        try:
            if url.startswith('http'):
                response = requests.post(url, json={"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}, timeout=5)
                if response.status_code == 200:
                    return url
            else:
                # Try WebSocket if needed
                w3 = Web3(Web3.WebsocketProvider(url))
                if w3.is_connected():
                    return url
        except:
            continue
    return None

def get_fingerprint_data(w3, address):
    """Get fingerprint data from blockchain"""
    try:
        address = Web3.to_checksum_address(address)
        balance = w3.eth.get_balance(address)
        tx_count = w3.eth.get_transaction_count(address)
        code = w3.eth.get_code(address)
        
        return {
            'address': address,
            'balance': balance,
            'balance_eth': Web3.from_wei(balance, 'ether'),
            'transaction_count': tx_count,
            'is_contract': len(code) > 0,
            'last_checked': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

def print_results(data, rpc_url):
    """Display results in a professional format"""
    print("\n" + "="*60)
    print(f"{Colors.HEADER}🔍 Monad Fingerprint Report{Colors.ENDC}")
    print("="*60)
    print(f"{Colors.BOLD}Address:{Colors.ENDC} {data['address']}")
    print(f"{Colors.BOLD}Balance:{Colors.ENDC} {data['balance_eth']} ETH ({data['balance']} wei)")
    print(f"{Colors.BOLD}Transactions:{Colors.ENDC} {data['transaction_count']}")
    print(f"{Colors.BOLD}Contract:{Colors.ENDC} {'Yes' if data['is_contract'] else 'No'}")
    print(f"{Colors.BOLD}RPC Node:{Colors.ENDC} {rpc_url}")
    print(f"{Colors.BOLD}Last Checked:{Colors.ENDC} {data['last_checked']}")
    print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description='Monad Blockchain Fingerprint Tool')
    parser.add_argument('address', help='Ethereum address to check')
    parser.add_argument('--rpc-url', help='Custom RPC endpoint URL')
    args = parser.parse_args()

    # Validate address
    if not Web3.is_address(args.address):
        print(f"{Colors.FAIL}❌ Invalid Ethereum address{Colors.ENDC}")
        sys.exit(1)

    # Determine RPC URL
    rpc_url = args.rpc_url
    if not rpc_url:
        print(f"{Colors.OKBLUE}⚡ Finding working RPC endpoint...{Colors.ENDC}")
        rpc_url = get_working_rpc(DEFAULT_RPC_URLS)
        if not rpc_url:
            print(f"{Colors.FAIL}❌ All RPC endpoints are unavailable{Colors.ENDC}")
            sys.exit(1)

    # Connect to Web3
    try:
        if rpc_url.startswith('http'):
            w3 = Web3(Web3.HTTPProvider(rpc_url))
        else:
            w3 = Web3(Web3.WebsocketProvider(rpc_url))
        
        if not w3.is_connected():
            raise Exception("Failed to connect to RPC")
    except Exception as e:
        print(f"{Colors.FAIL}❌ RPC Connection Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)

    # Get fingerprint data
    try:
        print(f"{Colors.OKBLUE}🔍 Fetching data for {args.address}...{Colors.ENDC}")
        data = get_fingerprint_data(w3, args.address)
        print_results(data, rpc_url)
    except Exception as e:
        print(f"{Colors.FAIL}❌ Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
