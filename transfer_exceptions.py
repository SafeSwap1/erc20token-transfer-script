class InvalidAddressError(Exception):
    "Address is not valid"
    pass

class InvalidKeyError(Exception):
    "Invalid Private Key Provided"
    pass

class InsufficientBalanceError(Exception):
    "Amount exceed availaible balance"
    pass



