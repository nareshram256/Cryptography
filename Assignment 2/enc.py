import myRSA as rsa
import vignere as vig
import sys

# python enc.py <msg> <vig_key> <sender> <reciever>

# message
msg = sys.argv[1]
with open(msg, "r") as f:
    msg = f.read()

# preprocess msg
msg = vig.process_inp(msg)

# vignere key
vig_key = sys.argv[2]
with open(vig_key, "r") as f:
    vig_key = f.read()

# sender's secret key
user_name = sys.argv[3]
user_name_path = "secret_keys/" + user_name + ".txt"
with open(user_name_path, "r") as f:
    sk_a = f.readlines()
    sk_a = [i.strip() for i in sk_a]
    sk_a = int(sk_a[0]), int(sk_a[1])

# receiver's public key
receiver_name = sys.argv[4]
receiver_name_path = "public_keys/" + receiver_name + ".txt"
with open(receiver_name_path, "r") as f:
    pk_b = f.readlines()[:2]
    pk_b = [i.strip() for i in pk_b]
    pk_b = int(pk_b[0]), int(pk_b[1])

# vignere encryption
vig_cipher = vig.vig_encrypt(inp=msg, key=vig_key)
# vig_key + vignere encrypted text
vig_cipher = vig_key + vig_cipher

# break into blocks
# n = sk_a[0] if sk_a[0] < pk_b[0] else pk_b[0]
# block_size = len(str(n)) - 1
block_size = len(str(pk_b[0])) - 1
if block_size % 2 != 0:
    block_size -= 1


# print(vig_cipher)
# print("bl_size", block_size)
vig_blocks = rsa.str_to_blocks(vig_cipher, block_size)

# decryption using sender's secret key
rsa_dec = rsa.encrypt(vig_blocks, sk_a)

# encryption using receiver's public key
rsa_enc = rsa.encrypt(rsa_dec, pk_b)

# write to disk
output_filename = "ciphers/" + user_name + "_cipher.txt"
with open(output_filename, "w") as w:
    for block in rsa_enc:
        w.write(block + "\n")