# TokenTransfer

This Python script provides a simple class, `TokenTransfer`, for transferring Ethereum-based tokens (including Ether and ERC20 tokens) from one address to another using the `web3.py` library.

## Prerequisites

- Python 3.6 or higher
- `web3.py` library installed

## Usage

1. Import the `TokenTransfer` class from the script:

```python
from token_transfer import TokenTransfer
```

2. Create an instance of the `TokenTransfer` class with the necessary parameters:

```python
rpc_url = "YOUR_RPC_URL"
private_key = "YOUR_PRIVATE_KEY"
contract_address = "TOKEN_CONTRACT_ADDRESS"  # Optional for ERC20 tokens, leave it empty for Ether
token_transfer = TokenTransfer(rpc_url, private_key, contract_address)
```

3. Get the token balance of the sender's address:

```python
balance = token_transfer.get_balance()
print("Balance:", balance)
```

4. Transfer tokens to a recipient address:

```python
recipient_address = "RECIPIENT_ADDRESS"
amount = 10  # Change this to the desired amount of tokens
transaction_hash = token_transfer.transfer_tokens(recipient_address, amount)
print("Transaction Hash:", transaction_hash)
```

For more detailed usage and customization options, refer to the source code.

DONATE: 0xb9C1de0E8764Ac737A114cfD9831eacE78e47856
