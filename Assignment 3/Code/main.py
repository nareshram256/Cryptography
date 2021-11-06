import myRC4 as rc4
import sys

text_path = sys.argv[1]

with open(text_path, 'r') as f:
    text = f.read()

r_dict = rc4.rc4_analysis(key_size=256, counter_size=8, text=text)

# comment following line if vendor
rc4.plot_dict(r_dict)

rc4.plot_size_vs_randomness(r_dict)
rc4.plot_similarity(text)