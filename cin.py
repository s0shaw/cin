import cv2
import numpy as np
import os
import sys
import argparse

def text_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_text(binary_data):
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data.endswith("#####"):
            return decoded_data[:-5]
    return decoded_data

def check_capacity(img, message):
    rows, cols, channels = img.shape
    max_bits = rows * cols * channels
    required_bits = (len(message) * 8) + 40 
    
    if required_bits > max_bits:
        raise ValueError(f"Message too long! Need {required_bits} bits, but image has {max_bits}.")
    return True

def encode_data(image_path, secret_message, output_path):
    if not os.path.exists(image_path):
        print(f"[Error] Input file '{image_path}' not found.")
        return

    img = cv2.imread(image_path)
    if img is None:
        print(f"[Error] Could not read '{image_path}'.")
        return
    
    try:
        check_capacity(img, secret_message + "#####")
    except ValueError as e:
        print(f"[Error] {e}")
        return

    secret_message += "#####"
    binary_message = text_to_binary(secret_message)
    data_len = len(binary_message)
    
    rows, cols, channels = img.shape
    data_index = 0
    
    print(f"[Info] Encoding {data_len} bits into '{image_path}'...")

    for row in range(rows):
        for col in range(cols):
            for channel in range(3):
                if data_index < data_len:
                    pixel = img[row, col, channel]
                    img[row, col, channel] = (pixel & 254) | int(binary_message[data_index])
                    data_index += 1
                else:
                    break
            if data_index >= data_len: break
        if data_index >= data_len: break
        
    cv2.imwrite(output_path, img)
    print(f"[Success] Saved to '{output_path}'")

def decode_data(image_path):
    if not os.path.exists(image_path):
        print(f"[Error] File '{image_path}' not found.")
        return

    print(f"[Info] Scanning '{image_path}'...")
    img = cv2.imread(image_path)
    
    binary_data = ""
    rows, cols, channels = img.shape
    
    for row in range(rows):
        for col in range(cols):
            for channel in range(3):
                pixel = img[row, col, channel]
                binary_data += str(pixel & 1)
                
    raw_message = binary_to_text(binary_data)
    print(f"\n[+] DECODED MESSAGE: {raw_message}\n")

def visualize_lsb(image_path, output_path="visualization.png"):
    if not os.path.exists(image_path):
        print(f"[Error] File '{image_path}' not found.")
        return

    print(f"[Info] Creating LSB map for '{image_path}'...")
    img = cv2.imread(image_path)
    lsb_map = (img & 1) * 255
    cv2.imwrite(output_path, lsb_map)
    print(f"[Success] Map saved as '{output_path}'")

if __name__ == "__main__":
    banner = r"""
   ______ ____ _   _ 
  / _____|_  _| \ | |
 | |       | ||  \| |
 | |_____ _| || |\  |
  \______|____|_| \_| 
  Code Inside Nothing 
    """
    
    parser = argparse.ArgumentParser(
        epilog="Example: python cin.py -e -i input.png -m 'Secret'"
    )
    
    mode_group = parser.add_argument_group('Modes')
    mode_group.add_argument("-e", "--encode", action="store_true", help="Encode (Hide) mode")
    mode_group.add_argument("-d", "--decode", action="store_true", help="Decode (Read) mode")
    mode_group.add_argument("-v", "--visualize", action="store_true", help="Visualize LSB noise map")

    args_group = parser.add_argument_group('Arguments')
    args_group.add_argument("-i", "--input", type=str, help="Input image path")
    args_group.add_argument("-o", "--output", type=str, default="output.png", help="Output image path (for encoding)")
    args_group.add_argument("-m", "--message", type=str, help="Message to hide (for encoding)")

    if len(sys.argv) == 1:
        print(banner)
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.encode:
        if not args.input or not args.message:
            print("[Error] Encode mode requires --input (-i) and --message (-m)")
        else:
            encode_data(args.input, args.message, args.output)
            
    elif args.decode:
        if not args.input:
            print("[Error] Decode mode requires --input (-i)")
        else:
            decode_data(args.input)
            
    elif args.visualize:
        if not args.input:
            print("[Error] Visualize mode requires --input (-i)")
        else:
            visualize_lsb(args.input)
            
    else:
        print("[Error] Please select a mode: -e, -d, or -v")
        parser.print_help()