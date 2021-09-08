# Cryptography

## Hill Cipher
- The key should be supplied as a sequence of integers seperated by commas.
- The plaintext may include newlines as well.
- The key used in encryption and decryption must be the same. The key will be inverted by the decryption code itself.

### Encryption
Command to run from terminal:
`python hill_encrypt.py <plaintext_file> <keyfile> <outputfile>`

### Decryption
Command to run from terminal:
`python hill_decrypt.py <ciphertext_file> <keyfile> <outputfile>`
