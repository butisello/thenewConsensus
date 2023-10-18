from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Wallet:
    def __init__(self):
        print("Generating a new Wallet...")
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

    def sign(self, message):
        signer = pkcs1_15.new(self.private_key)
        hashed_msg = SHA256.new(message.encode('utf-8'))
        return signer.sign(hashed_msg)

    def get_public_key(self):
        return self.public_key.export_key()
