import myRSA as rsa
import sympy as sy
import hashlib
import re
import sys

# python CA.py <username>

user = sys.argv[1]
user_pk_path = "public_keys/" + user + ".txt"
user_sk_path = "secret_keys/" + user + ".txt"

# ca_n, ca_e, ca_d = rsa.gen_keys(sy.Pow(2, 8))
# ca_sk = (ca_n, ca_d)
# ca_pk = (ca_n, ca_e)

ca_n, ca_e, ca_d = 3311489, 17, 1751201
ca_sk = (ca_n, ca_d)
ca_pk = (ca_n, ca_e)

# Key generation for user
n, e, d = rsa.gen_keys(sy.Pow(2, 8))
sk = (n, d)
pk = (n, e)

encoding = (str(pk[0]) + str(pk[1])).encode()
hash = hashlib.sha1(encoding).hexdigest()
hash_alphas = "".join(re.findall("[A-Z]+", hash.upper()))
len_hash_nums = len(hash) - len(hash_alphas)
hash = hash_alphas + len_hash_nums * "X"

# block size
block_size = len(str(ca_n)) - 1
if block_size % 2 != 0:
    block_size -= 1

hash_blocks = rsa.str_to_blocks(hash, block_size)
signature = rsa.encrypt(hash_blocks, ca_sk)

# write keys to disk
with open(user_pk_path, "w") as w_pk:
    w_pk.write(str(pk[0]) + "\n" + str(pk[1]) + "\n")

    for block in signature:
        w_pk.write(block + "\n")

with open(user_sk_path, "w") as w_sk:
    w_sk.write(str(sk[0]) + "\n" + str(sk[1]))