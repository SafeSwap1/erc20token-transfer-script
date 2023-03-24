from web3 import Web3
from web3.middleware import geth_poa_middleware
import sys

class TokenTransfer:
    def __init__(self, rpc_url, private_key, contract_address=None):
        if len(private_key) != 64:
            sys.exit("Invalid private key supplied") 
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.private_key = private_key
        self.sender_address = self.w3.eth.account.from_key(private_key).address
        if contract_address:
            self.contract_address = Web3.to_checksum_address(contract_address)
            self.contract_abi = [
                {"constant":False,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
                {"constant":True,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},
                {"constant":True,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
                {"constant":False,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}
            ]
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        else:
            self.contract_address = None
            self.contract_abi = None
            self.contract = None

    def get_token_decimals(self):
        if self.contract:
            return self.contract.functions.decimals().call()
        else:
            return 18
        
    def get_balance(self):
        if self.contract:
            return self.w3.eth.functions.balanceOf(self.sender_address).call()
        else:
            return self.w3.eth.get_balance(self.sender_address)

    def transfer_tokens(self, recipient_address, amount, gas = None, time_out = None):
        if not self.w3.is_checksum_address(recipient_address):
            sys.exit("recipient address is invalid")
            
        if not gas:
            gas = 21000
            
        if not time_out:
            time_out = 120
            
        recipient_address = Web3.to_checksum_address(recipient_address)
        nonce = self.w3.eth.get_transaction_count(self.sender_address)

        decimals = self.get_token_decimals()
        token_amount = int(amount * (10 ** decimals))
        
        if self.get_balance() < token_amount:
            sys.exit('Amount exceeded balance')
            
        elif self.contract:
            # Transfer ERC20 tokens
            token_txn = self.contract.functions.transfer(
                recipient_address,
                token_amount
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': gas,
                'gasPrice': self.w3.eth.gasPrice,
                'nonce': nonce,
            })
        else:
            # Transfer ETH
            token_txn = {
                'to': recipient_address,
                'value': token_amount,
                'gas': gas,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': self.w3.eth.chain_id
            }

        # Sign the transaction
        signed_txn = self.w3.eth.account.sign_transaction(token_txn, self.private_key)

        # Send the transaction
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash, 120)
        txn_receipt = dict(txn_receipt) #convert attributeDict to regular dict
        transaction_hash = txn_receipt['transactionHash']

        return f"Transaction Hash: {self.w3.to_hex(transaction_hash)}"

