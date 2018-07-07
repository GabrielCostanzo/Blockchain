from user import wallet
from user import transaction 
from user import sign
from user import encrypt_key
from user import master_key
import time
import json
import pickle
import pymongo
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from json_serialize import wallet_to_json
from json_serialize import transaction_to_json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from tqdm import tqdm 

client = pymongo.MongoClient()
db = client.database

blocks = db.blocks
utxo_pool = db.utxo_pool


def user_login():
	valid_selection = False
	pass_conf = False
	valid_file = False
	while valid_selection == False:
		print("\n\n")
		print("[1] Login With file")
		print("[2] New Wallet\n")
		selection = int(input())
		time.sleep(1)

		if selection == 1:
			print("\nPlease select file:")
			time.sleep(0.5)
			try:
				Tk().withdraw()
				selected_file = askopenfilename() 
				with open("%s"%selected_file, "r") as json_selection:
					pulled_file = json.loads(json_selection.read())
			except:
				while valid_file == False:
					try:
						print("please enter a wallet file name:")
						selected_file = input(">")
						with open("%s.json"%selected_file, "r") as json_selection:
							pulled_file = json.loads(json_selection.read())
						valid_file = True
					except:
						print("invalid file selection.")

			return pulled_file
			valid_selection = True

		elif selection == 2:
			while pass_conf == False:
				print("\nCreate password:")
				initial_password = input(">")
				time.sleep(1)
				print("\nConfirm password:")
				confirmation_password = input(">")
				time.sleep(1)

				if initial_password == confirmation_password:
					password = initial_password
					created_wallet = wallet()
					json_wallet = wallet_to_json(created_wallet)

					with open("test_wallet_file.json", "w") as wallet_file:
						wallet_file.write(json_wallet)

					print("new wallet created!")

					pass_conf = True
					return created_wallet
				else:
					print("\npasswords do not match.\n")
					time.sleep(1)

				valid_selection = True

		else:
			print("\ninvalid selection!")
			time.sleep(1)

class loaded_wallet(wallet):
	def __init__(self, json_wallet):
		#private_key, public_key, pending_out, conf_out, unspent_out, spent_out
		#transaction.__init__(self, sender_public_key, receiver_public_key, input_amount, fees)
		self.serialized_private = json_wallet["serialized_private"].encode('UTF-8')
		self.serialized_public = json_wallet["serialized_public"].encode('UTF-8')
		self.pending_output_transactions = json_wallet["pending_output_transactions"]
		self.confirmed_output_transactions = json_wallet["confirmed_output_transactions"]
		self.unspent_input_transactions = json_wallet["unspent_input_transactions"]
		self.spent_input_transactions = json_wallet["spent_input_transactions"]
		self.private_key = serialization.load_pem_private_key(self.serialized_private, password=None ,backend=default_backend())
		self.public_key = serialization.load_pem_public_key(self.serialized_public, backend=default_backend())

	def update_input_transactions(self):
		for i in range(0, blocks.count()):
			current = blocks.find_one({"_id": i})
			for j in current["transactions"]:
				if (j["receiver_public_key"].encode('UTF-8') == self.serialized_public and [j["txid"], j["output_amount"]] not in self.unspent_input_transactions):
					(self.unspent_input_transactions).append([j["txid"], j["output_amount"]])

				if (j["sender_public_key"].encode('UTF-8') == self.serialized_public and j["status"] != "coinbase"):
					for n in j["input_transactions"]:
						if n in self.unspent_input_transactions:
							self.unspent_input_transactions.remove(n)
							self.spent_input_transactions.append(n)

	def set_input_transactions(self, input_val):
		running_val = 0 
		input_list = []
		for i in self.unspent_input_transactions:
			running_val += i[1]
			input_list.append(i)
			if running_val >= input_val:
				for i in input_list:
					self.unspent_input_transactions.remove(i)
					self.spent_input_transactions.append(i)
				return input_list


	def create_transaction(self, receiver_public_key, input_amount, fees):
		self.update_input_transactions()
		new_transaction = transaction(self.serialized_public, receiver_public_key, input_amount, fees)
		if self.set_input_transactions(new_transaction.input_amount) == None:
			new_transaction.input_transactions = []
		else:
			new_transaction.input_transactions = self.set_input_transactions(new_transaction.input_amount)

		pickled_transaction = pickle.dumps(new_transaction)

		new_transaction.update_sig(self.sign_transaction(pickled_transaction))
		new_transaction.update_data(pickled_transaction)
		new_transaction.update_txid(encrypt_key(pickled_transaction, master_key))

		final_transaction = json.loads(transaction_to_json(new_transaction))

		self.pending_output_transactions.append(final_transaction)

		return final_transaction