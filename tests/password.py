from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

private_key_passp = ec.generate_private_key(ec.SECP384R1(), default_backend())

serialized_private_passp = private_key_passp.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.BestAvailableEncryption(b'testpassword'))
#print(serialized_private_passp)

loaded_private_key_passp = serialization.load_pem_private_key(serialized_private_passp,password=b'testpassword',backend=default_backend())



private_key_nop = ec.generate_private_key(ec.SECP384R1(), default_backend())

serialized_private_nop = private_key_nop.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
#print(serialized_private_nop)

loaded_private_key_nop = serialization.load_pem_private_key(serialized_private_nop,password=None ,backend=default_backend())

print(loaded_private_key_passp.private_numbers().private_value)
#print(loaded_private_key_nop) 