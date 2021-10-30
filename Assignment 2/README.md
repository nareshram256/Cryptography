# Cryptography: Assignment 2

2021VSN9003 : Burouj Armgaan <br>
2017CS50421 : Vijay Kumar Meena

### Libraries used
- sympy
- gmpy2
- numpy
- hashlib

### Encryption
Command to run from terminal:<br>
`python enc.py <plaintext_file> <vignere_key_file> <sender_name> <receiver_name>`

### Decryption
Command to run from terminal:<br>
`python dec.py <ciphertext_file> <known_vig_key_len> <sender_name> <receiver_name>`

### Key Generation and Signature
Command to run from terminal:<br>
`python CA.py <user_name>`

### Verify Key using Signature
Command to run from terminal:<br>
`python verify.py <user_name>`

### Assumption
- When passing filenames write .txt as well.
- Exponentiation handled by sympy.Pow()
- Receiver's value of n in RSA key should be larger than sender's value of n. Check `Limitation.png` for its reason.
