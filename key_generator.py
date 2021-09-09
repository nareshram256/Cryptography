import numpy as np
import sys

key_size = int(sys.argv[1])
outputfile = sys.argv[2]

def generate_key(key_size):
    key = np.random.randint(low=0, high=100, size=(key_size, key_size)) % 26
    return key

def mat_to_str(mat):
    mat_str = ",".join(list(map(str, mat.ravel())))
    return mat_str

while True:
    key = generate_key(key_size)
    if np.linalg.det(key) % 26 != 0:
        break
print(key)
key_str = mat_to_str(key)

with open(outputfile, "w") as file:
    file.write(key_str)