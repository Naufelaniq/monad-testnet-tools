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
        return f"Address {address} is valid. Faucet simulation: OK"
    return f"Invalid address: {address}"

def rpc_health_check(rpc_url):
    import requests
    try:
        res = requests.post(rpc_url, json={"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1})
        if res.status_code == 200:
            return f"✅ RPC working: {rpc_url}"
        else:
            return f"❌ RPC failed with status {res.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

---

## 🔍 Run Monad Wallet Analyzer Online (No Setup Needed)

You can run this tool in your **browser using GitHub Codespaces** — no need to install Python, pip, or Termux.

👉 [Click to Open in Codespaces](https://github.com/codespaces/new?hide_repo_select=true&repo=naufelaniq%2Fmonad-testnet-tools)

---

### 🧪 Usage inside Codespaces

After opening in Codespaces:

1. Open the terminal (press `Ctrl + backtick` or click on terminal)
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the tool:

```bash
python fingerprint_rpc.py 0xYourWalletAddress
```

---

### ⭐ Example:

```bash
python fingerprint_rpc.py 0xAF9e50c42b568F668b5a3B2573c7098e5460d174
```

---

If this helped you, please consider giving the repo a ⭐ on GitHub — it motivates me to build more 🙏
