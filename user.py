from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import serialization
import pickle
from hashlib import blake2b
import datetime

master_key = b'pseudorandomly generated server secret key'

auth_size = 16

def sign(user, in_key):
	h = blake2b(digest_size = auth_size, key = in_key)
	h.update(user)
	return h.hexdigest()

def encrypt_key(access_key, secret_key):
	encrypted = (sign(access_key, secret_key))

	return encrypted

class transaction():
	def __init__(self, sender_public_key, receiver_public_key, input_amount, fees):
		self.sender_sig = None
		self.transaction_data = None
		self.sender_public_key = sender_public_key

		self.receiver_public_key = receiver_public_key

		self.input_amount = input_amount
		self.fees = fees
		self.output_amount = input_amount - fees

		self.input_transactions = None

		self.status = "Requires Signature"

		self.txid = None

		self.timestamp = datetime.datetime.now()


	def update_data(self, data):
		self.transaction_data = data.decode('latin1')

	def update_sig(self, signature):
		self.sender_sig = signature
		self.status = "Signed" 

	def update_txid(self, txid):
		self.txid = txid.encode('UTF-8')



	#def __str__(self):
	#	return "\nsender_sig: %s\ntransaction_data: %s\n\nsender_public_key (serialized): %s\nreceiver_public_key (serialized): %s\n\ninput_amount: %s\nfees: %s\noutput_amount: %s\n\nstatus: %s" % (self.sender_sig, self.transaction_data, self.sender_public_key, self.receiver_public_key, self.input_amount, self.fees, self.output_amount, self.status)

class wallet():
	def __init__(self):
		self.private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
		self.serialized_private = self.private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())

		self.public_key = self.private_key.public_key()
		self.serialized_public = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)

		self.pending_output_transactions = []
		self.confirmed_output_transactions = []

		self.unspent_input_transactions = []
		self.spent_input_transactions = []

	def sign_transaction(self, data):
		sig = self.private_key.sign(data, ec.ECDSA(hashes.SHA256()))
		return sig
"""
	def create_transaction(self, receiver_public_key, input_amount, fees):
		new_transaction = transaction(self.serialized_public, receiver_public_key, input_amount, fees)
		pickled_transaction = pickle.dumps(new_transaction)

		new_transaction.update_sig(self.sign_transaction(pickled_transaction))
		new_transaction.update_data(pickled_transaction)
		new_transaction.update_txid(encrypt_key(pickled_transaction, master_key))

		updated_pickled_transaction = pickle.dumps(new_transaction)
		self.pending_output_transactions.append(updated_pickled_transaction)

		return new_transaction
"""

"""
sally = wallet()


test_transaction = transaction(sally.serialized_public, sally.serialized_public, 5, 2)

sally.create_transaction(sally.serialized_public, 5, 2)

print(sally.transaction_pool[0])


print(sally.public_key.verify(sally.transaction_pool[0].sender_sig, sally.transaction_pool[0].transaction_data, ec.ECDSA(hashes.SHA256())))
"""