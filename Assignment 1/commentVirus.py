from cryptography.fernet import Fernet
import os
import random

key = "tPK2MPjCrioTQCf9KZn55AP7ndrAi2oy6pCUmwRB3Lw="
fernet = Fernet(key)

with open('hello_world.py', 'rb') as file:
    original = file.read()

if "print" in original.decode():
    encrypted = fernet.encrypt(original)
    with open('hello_world.py', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

print("Before encryption (Signature):")
os.system("certutil -hashfile hello_world.py")
print("\n******************************************************\n")

with open('hello_world.py', 'rb') as file:
    original = file.read()
    decrypted = fernet.decrypt(original)

with open('hello_world.py', 'wb') as decrypted_file:
    decrypted_file.write(decrypted)

with open("hello_world.py", "r") as f:
    lines = f.readlines()

with open("hello_world.py", "w") as f:
    for line in lines:
        if "#" not in line:
            f.write(line)


num = random.randint(0, 99999)
print(num)


file_object = open('hello_world.py', 'a')
file_object.write("\n#" + str(num))
file_object.close()


with open('hello_world.py', 'rb') as file:
    original = file.read()

encrypted = fernet.encrypt(original)
with open('hello_world.py', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

print("After encryption (Signature):")
os.system("certutil -hashfile hello_world.py")
print("\n******************************************************\n")