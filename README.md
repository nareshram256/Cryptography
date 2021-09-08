# Cryptography

## Hill Cipher
- The keyfile should contain the key as a sequence of integers seperated by commas. No new lines should be used.
- The plaintext may include newlines as well.
- The key used in encryption and decryption must be the same. The key will be inverted by the decryption code itself.

### Libraries used
- numpy
- string
- sympy
- sys

### Encryption
Command to run from terminal:
`python hill_encrypt.py <plaintext_file> <keyfile> <outputfile>`

### Decryption
Command to run from terminal:
`python hill_decrypt.py <ciphertext_file> <keyfile> <outputfile>`
