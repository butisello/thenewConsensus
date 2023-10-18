from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import uuid
import time

class Transaction:
    #def __init__(self, senderPublicKey, receiverPublicKey, amount, type):
    def __init__(self, senderPublicKey, receiverPublicKey, amount, type, signature):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.fee = 5
        self.signature = signature

    def verify_signature(self, public_key):
        verifier = pkcs1_15.new(public_key)
        #hashed_msg = SHA256.new((self.senderPublicKey + self.receiverPublicKey + str(self.amount) + self.type).encode('utf-8'))
        hashed_msg = SHA256.new((self.senderPublicKey.decode('utf-8') + self.receiverPublicKey.decode('utf-8') + str(self.amount) + self.type).encode('utf-8'))

        try:
            verifier.verify(hashed_msg, self.signature)
            return True
        except (ValueError, TypeError):
            return False
