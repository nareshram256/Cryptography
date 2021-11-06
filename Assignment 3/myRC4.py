import numpy as np
import random
import secrets
import matplotlib.pyplot as plt
plt.style.use('seaborn')

def xor_bytes(b1:bytes, b2:bytes) -> bytes:
    return bytes(byte1 ^ byte2 for byte1, byte2 in zip(b1, b2))

class RC4:
    def __init__(self, key:bytes) -> None:
        self.S = [i for i in range(256)]
        self.T = self.__repeat_string(key, 256)

        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.T[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
    
    def __repeat_string(self, a_string:str, target_length:int) -> str:
        number_of_repeats = target_length // len(a_string) + 1
        a_string_repeated = a_string * number_of_repeats
        a_string_repeated_to_target = a_string_repeated[:target_length]
        return a_string_repeated_to_target
        
    def __gen_key(self, len_text:int) -> bytes:
        i, j = 0, 0
        key = []
        for _ in range(len_text):
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            t = (self.S[i] + self.S[j]) % 256
            key.append(self.S[t])
        return bytes(key)
        
    def encrypt(self, p_text:str) -> bytes:
        p_text = bytes(p_text, 'utf-8')
        key = self.__gen_key(len(p_text))
        cipher = xor_bytes(p_text, key)
        return cipher

    def decrypt(self, cipher:bytes) -> str:
        key = self.__gen_key(len(cipher))
        dec = xor_bytes(cipher, key)
        return dec.decode('utf-8')

def toggle_bit(value, bit_index):
    return value ^ (1 << bit_index)

def random_flip(byte_str:bytes, bits_to_flip:int) -> bytes:
    byte_arr = bytearray(byte_str)
    for i in range(bits_to_flip):
        random_byte = random.randint(0,len(byte_arr)-1)
        random_bit = random.randint(0,7)
        byte_arr[random_byte] = toggle_bit(byte_arr[random_byte], random_bit)

    return bytes(byte_arr)

def count(text:bytes, size:int):
    total_counters = int(2**size)
    counters = [0 for i in range(total_counters)]
    bit_array = "".join(["{:b}".format(i) for i in text])

    for i in range(len(bit_array) - size):
        counters[int(bit_array[i : i+size], 2)] += 1
        
    return counters

def randomness(text:bytes, counter_size:int):
    counters = count(text, counter_size)
    C = len(counters)
    N = len(text)
    D = np.std(counters)
    # print("Text:", N)
    # print("Counters:", C)
    # print("Deviation:", D)

    return (C*D)/N

def rc4_analysis(key_size:int, counter_size:int, text:bytes):
    print("Calculating randomness...")

    # main
    indices = [2**j for j in range(1, 11)]

    # vendor
    # indices = [i for i in range(1,51)]

    k1 = secrets.token_bytes(key_size)

    r_dict = dict()
    for idx in indices:
        subtext = text[:idx]
        s1_rc4 = RC4(k1)
        c1 = s1_rc4.encrypt(subtext)

        r = []
        for i in range(1,33):
            temp = []
            for _ in range(20):
                k2 = random_flip(k1, i)
                s2_rc4 = RC4(k2)
                c2 = s2_rc4.encrypt(subtext)
                # if i == 0:
                #     print(f"idx: {idx} | key: {k1 == k2} | cipher, {c1 == c2}\n")
                mix = xor_bytes(c1, c2)
                
                temp.append(randomness(mix, counter_size))

            r.append(np.mean(temp))
            
        r_dict[idx] = r
    return r_dict

def plot_dict(r_dict:dict):
    indices = [2**j for j in range(1, 11)]
    
    fig = plt.figure(figsize=(20,20))
    for i, idx in enumerate(indices):
        plt.subplot(5,2,i+1)
        plt.plot(range(1,33), np.round(r_dict[idx], 2), label=idx, color='teal', marker="o")
        plt.xticks(range(1,33))
        plt.ylim(0,25)
        plt.title(f"Input size: {idx}", fontsize=18)
        plt.xlabel("Bit changes in the key (1-32)", fontsize=14, labelpad=10)
        plt.ylabel("Randomness", fontsize=14, labelpad=10)
    fig.tight_layout(pad=5)
    plt.savefig("bit_flips_vs_randomness")
    print("Saving plot...")

def plot_size_vs_randomness(r_dict:dict):
    # main
    indices = [2**j for j in range(1, 11)]

    # vendor
    # indices = [i for i in range(2,51)]

    fig = plt.figure(figsize=(10,8))

    y_values = []
    for idx in indices:
        y_values.append(np.round(np.mean(r_dict[idx])))

    for i, idx in enumerate(indices):
        plt.plot(range(len(indices)), y_values, color='teal', marker='o')

    plt.xticks(range(len(indices)), labels=indices)
    # plt.ylim(0,15)
    plt.title(f"Input size vs Randomness", fontsize=18)

    # main
    plt.xlabel("Input size (2-1024)", fontsize=14, labelpad=10)

    # vendor
    # plt.xlabel("Input size (2-50)", fontsize=14, labelpad=10)

    plt.ylabel("Randomness", fontsize=14, labelpad=10)
    fig.tight_layout(pad=5)
    plt.savefig("size_vs_randomness")
    print("Saving plot...")

def similarity(text1:bytes, text2:bytes):
    freq = 0
    for b1, b2 in zip(text1, text2):
        if b1 == b2:
            freq += 1
    return freq

def avg_similarity(text:str, flips:int):
    k1 = secrets.token_bytes(256)
    sim = []
    for _ in range(20):
        rc4_1 = RC4(k1)
        k2 = random_flip(k1, flips)
        rc4_2 = RC4(k2)

        c1 = rc4_1.encrypt(text)
        c2 = rc4_2.encrypt(text)

        sim.append(similarity(c1, c2))
    return int(np.mean(sim))

def plot_similarity(text:str):
    sim_list = []
    for bit_flips in range(1, 33):
        sim_list.append(avg_similarity(text, bit_flips))

    plt.figure(figsize=(12,6))
    plt.plot(range(1, len(sim_list)+1), sim_list, marker='o', color='teal')
    plt.ylim(0,15)
    plt.xticks(range(1, len(sim_list)+1), [i for i in range(1, len(sim_list) + 1)])
    plt.xlabel("Bit flips (1-32)", fontsize=14)
    plt.ylabel("Similarity", fontsize=14)
    plt.title("Similarity vs Bit flips", fontsize=18)
    plt.savefig("similarity")
    print("Saving plot...")
