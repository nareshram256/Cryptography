import myRSA as rsa
import vignere as vig
import sys

# python dec.py <cipher> <vig_key_len> <sender> <reciever>

# cipher
cipher = sys.argv[1]
with open(cipher ,"r") as f:
    cipher_blocks = f.readlines()
    cipher_blocks = [c.strip() for c in cipher_blocks]

# vig_key_len
vig_key_len = int(sys.argv[2])

# sender's public key
sender_name = sys.argv[3]
sender_name_path = "public_keys/" + sender_name + ".txt"
with open(sender_name_path, "r") as f:
    pk_a = f.readlines()[:2]
    pk_a = [i.strip() for i in pk_a]
    pk_a = int(pk_a[0]), int(pk_a[1])

# receiver's secret key
user_name = sys.argv[4]
user_name_path = "secret_keys/" + user_name + ".txt"
with open(user_name_path, "r") as f:
    sk_b = f.readlines()
    sk_b = [i.strip() for i in sk_b]
    sk_b = int(sk_b[0]), int(sk_b[1])

# decryption using receiver's private key
rsa_dec = rsa.encrypt(cipher_blocks, sk_b)

# encryption using sender's public key
rsa_enc = rsa.encrypt(rsa_dec, pk_a)

# block to str
vig_string = rsa.blocks_to_str(rsa_enc)

# extract vig_key
vig_key, vig_string = vig_string[:vig_key_len], vig_string[vig_key_len:]

# decrypt using vig_key
plain = vig.vig_decrypt(vig_string, vig_key)

# write to disk
output_filename = "decrypts/" + sender_name + "_dec.txt"
with open(output_filename, "w") as w:
    w.write(plain)