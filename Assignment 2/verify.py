import sys
import myRSA as rsa
import hashlib
import re

# python verify.py <username>

# CA's public key
ca_pk = (3311489, 17)

# read key and signature
user = sys.argv[1]
user_path = "public_keys/" + user + ".txt"

with open(user_path, "r") as f:
    temp = f.readlines()[:-1]
    temp = [i.strip() for i in temp]
    pk = int(temp[0]), int(temp[1])

with open(user_path, "r") as f:
    sign = f.readlines()[2:]
    sign = [i.strip() for i in sign]

# decrypt sign
hash = rsa.encrypt(sign, ca_pk)
hash = rsa.blocks_to_str(hash)

# hash user's key
encoding = (str(pk[0]) + str(pk[1])).encode()
key_hash = hashlib.sha1(encoding).hexdigest()
hash_alphas = "".join(re.findall("[A-Z]+", key_hash.upper()))
len_hash_nums = len(key_hash) - len(hash_alphas)
key_hash = hash_alphas + len_hash_nums * "X"

print(key_hash, hash, sep="\n")
# comapre with signature
print(hash == key_hash)