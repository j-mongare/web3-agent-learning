from web3 import Web3
import time

# Connect to Anvil
rpc_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check connection
if not web3.is_connected():
    print("Connection failed")
    exit()

print("Connected to Anvil")

# Contract address
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# ABI
abi = [
    {
        "inputs": [],
        "name": "number",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "increment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Account setup
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
account = web3.eth.account.from_key(private_key)

print(f"Agent started with address: {account.address}")

# Agent loop
while True:
    current_number = contract.functions.number().call()
    print(f"Current number: {current_number}")

    if current_number < 10:
        print("Incrementing...")

        tx = contract.functions.increment().build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 100000,
            'gasPrice': web3.to_wei('1', 'gwei')
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"Transaction sent: {tx_hash.hex()}")

    else:
        print("Target reached. Stopping agent.")
        break

    time.sleep(3)