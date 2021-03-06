# Cryptography: Assignment 1

2021VSN9003 : Burouj Armgaan <br>
2017CS50421 : Vijay Kumar Meena

## Hill Cipher
- The keyfile should contain the key as a sequence of integers seperated by commas. No new lines should be used.
- The plaintext may include newlines as well.
- The key used in encryption and decryption must be the same. The key will be inverted by the decryption code itself.

### Libraries used
- collections
- numpy
- string
- sympy
- sys

### Encryption
Command to run from terminal:
`python hill_encrypt.py <plaintext_file> <key_file> <output_file>`

### Decryption
Command to run from terminal:
`python hill_decrypt.py <ciphertext_file> <key_file> <output_file>`

### Analysis
Command to run from terminal:<br>
`python analysis.py <known_ciphertext_file> <known_plaintext_file> <complete_ciphertext_file> <output_file>`

### Key Generator
Command to run from terminal:
`python key_generator.py <key_size> <output_file>`

## Assumptions
- Python version 3.7.11 or higher.
- Write the file extensions when providing filepaths.
- The chosen `<known_ciphertext_file>` and `<known_plaintext_file>` must be extracted from main ciphertext and plaintext starting at an integer multiple of the key_size used. For example: If the key_size is 5, the chosen ciphertext must be extracted started at index 5 or 10 or 15 and so on. Note that indexing starts at 0, not 1.
