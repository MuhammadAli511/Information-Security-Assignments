from cryptography.fernet import Fernet
import os

with open('hello_world.py', 'rb') as file:
    original = file.read()


if "print" in original.decode():
    bool2 = False
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(original)
    with open('hello_world.py', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

else:
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
        fernet = Fernet(key)


print("Before encryption (Signature):")
os.system("certutil -hashfile hello_world.py")
print("\n******************************************************\n")


with open('hello_world.py', 'rb') as file:
    original = file.read()
    decrypted = fernet.decrypt(original)
    

with open('hello_world.py', 'wb') as decrypted_file:
    decrypted_file.write(decrypted)

key = Fernet.generate_key()

fernet = Fernet(key)
with open('filekey.key', 'wb') as filekey:
    filekey.write(key)

encrypted = fernet.encrypt(decrypted)
with open('hello_world.py', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

print("After encryption (Signature):")
os.system("certutil -hashfile hello_world.py")
print("\n******************************************************\n")