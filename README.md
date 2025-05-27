# HuffmanCompressor

HuffmanCompressor is a Python tool for lossless text compression and decompression using Huffman coding. It assigns shorter binary codes to frequently occurring characters, reducing file size. The program reads a text file, builds a Huffman tree based on character frequencies, generates a prefix-code table, and compresses the text into a binary file with a header for decoding. The decoder reconstructs the original text. Designed for beginners, it supports ASCII text with robust error handling.

## Features
- Compresses text files using Huffman coding
- Decompresses back to the original text
- Command-line interface for easy use
- Handles ASCII characters with error checking

## Requirements
- Python 3.x

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AsifMinar/HuffmanCompressor.git
   ```
2. Ensure `huffman.py` is in the project directory.

## Usage
Run the program via the command line:
- **Compress**: `python huffman.py encode input.txt compressed.huff`
- **Decompress**: `python huffman.py decode compressed.huff output.txt`

Example:
```bash
echo "aaabbc" > test.txt
python huffman.py encode test.txt compressed.huff
python huffman.py decode compressed.huff output.txt
```

## Testing
- Create a `test.txt` with sample text (e.g., "aaabbc").
- Compress and decompress to verify the output matches the input.
- Try with larger files like *Les Misérables* for real-world testing.

## Limitations
- Supports ASCII characters only.
- Small files may result in larger compressed files due to header overhead.
