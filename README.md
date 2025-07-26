# Monad Utils Kit 🚀

A lightweight Python toolset for Monad testnet interactions.

---

## ✨ Features

- ✅ Monad address validator  
- 🛰️ RPC endpoint health checker  
- 🧪 Faucet claim simulator (dummy logic)  
- 🧠 Dev-ready structure for more Monad utilities

---

## 📦 File: utils.py

```python
def is_valid_monad_address(address):
    return address.startswith("0x") and len(address) == 42

def mock_faucet_checker(address):
    if is_valid_monad_address(address):
        return f"Address {address} is valid. Faucet simulation: ✅ success (dummy)"
    return f"Invalid address: {address}"

def rpc_health_check(rpc_url):
    import requests
    try:
        res = requests.post(rpc_url, json={"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}, timeout=5)
        if res.status_code == 200:
            return f"✅ RPC working: {rpc_url}"
        else:
            return f"⚠️ RPC error: {res.status_code}"
    except Exception as e:
        return f"❌ RPC failed: {str(e)}"
