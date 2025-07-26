import argparse
from utils import is_valid_monad_address, mock_faucet_checker, rpc_health_check

def main():
    parser = argparse.ArgumentParser(description="Monad Wallet & RPC Checker CLI")
    parser.add_argument("--wallet", type=str, required=True, help="Monad wallet address (starts with 0x...)")
    parser.add_argument("--rpc", type=str, required=False, help="RPC URL to check (optional)")

    args = parser.parse_args()

    print("\n🔍 Checking Wallet Address:")
    print(mock_faucet_checker(args.wallet))

    if args.rpc:
        print("\n🛰️ Checking RPC Health:")
        print(rpc_health_check(args.rpc))

if __name__ == "__main__":
    main()