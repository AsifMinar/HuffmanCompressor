import os
import heapq
import struct
import sys

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def get_frequencies(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        return None
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    frequencies = {}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies

def build_tree(frequencies):
    nodes = []
    for char, freq in frequencies.items():
        heapq.heappush(nodes, Node(char, freq))
    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heapq.heappush(nodes, parent)
    return nodes[0]

def build_codes(tree):
    codes = {}
    def make_codes(node, code=""):
        if node.char is not None:
            codes[node.char] = code if code else "0"
        else:
            if node.left:
                make_codes(node.left, code + "0")
            if node.right:
                make_codes(node.right, code + "1")
    make_codes(tree)
    return codes

def write_header(frequencies, output_file, text_length):
    with open(output_file, 'wb') as f:
        f.write(struct.pack('>I', text_length))
        f.write(struct.pack('>I', len(frequencies)))
        for char, freq in frequencies.items():
            f.write(char.encode('ascii'))
            f.write(struct.pack('>I', freq))

def compress(input_file, output_file):
    frequencies = get_frequencies(input_file)
    if not frequencies:
        return
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    tree = build_tree(frequencies)
    codes = build_codes(tree)
    write_header(frequencies, output_file, len(text))
    bits = "".join(codes[char] for char in text)
    padding = 8 - (len(bits) % 8)
    if padding == 8:
        padding = 0
    bits += "0" * padding
    with open(output_file, 'ab') as f:
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            f.write(bytes([int(byte, 2)]))

def read_header(input_file):
    with open(input_file, 'rb') as f:
        total_chars = struct.unpack('>I', f.read(4))[0]
        num_chars = struct.unpack('>I', f.read(4))[0]
        frequencies = {}
        for _ in range(num_chars):
            char = f.read(1).decode('ascii')
            freq = struct.unpack('>I', f.read(4))[0]
            frequencies[char] = freq
    return total_chars, frequencies

def decompress(input_file, output_file):
    total_chars, frequencies = read_header(input_file)
    tree = build_tree(frequencies)
    with open(input_file, 'rb') as f:
        f.read(8)
        f.read(5 * len(frequencies))
        bits = ''.join(f'{byte:08b}' for byte in f.read())
    node = tree
    decoded = ""
    for bit in bits:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.char is not None:
            decoded += node.char
            node = tree
            if len(decoded) == total_chars:
                break
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decoded)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python huffman.py [encode|decode] input_file output_file")
        sys.exit(1)
    
    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    if mode == "encode":
        compress(input_file, output_file)
        print(f"Compressed {input_file} to {output_file}")
    elif mode == "decode":
        decompress(input_file, output_file)
        print(f"Decompressed {input_file} to {output_file}")
    else:
        print("Use 'encode' or 'decode' only!")
        sys.exit(1)
        
