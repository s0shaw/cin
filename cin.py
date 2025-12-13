import cv2
import numpy as np
import os

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

def encode_data(image_path, secret_message, output_path):

    img = cv2.imread(image_path)
    
    if img is None:
        print(f"[Error] The image file '{image_path}' was not found.")
        return

    secret_message += "#####"
    
    binary_message = text_to_binary(secret_message)
    data_index = 0
    data_len = len(binary_message)
    
    rows, cols, channels = img.shape
    
    print(f"[Info] Encoding message... Total bits to hide: {data_len}")
    
    for row in range(rows):
        for col in range(cols):
            for channel in range(3):  
                
                if data_index < data_len:
                    pixel = img[row, col, channel]
                    
                    # --- LSB LOGIC ---
                    # pixel & 254 (11111110) -> Makes the last bit 0
                    # int(binary_message[data_index]) -> The bit to hide (0 or 1)
                    # The result is the new pixel value
                    
                    img[row, col, channel] = (pixel & 254) | int(binary_message[data_index])
                    data_index += 1
                else:
                    break
            if data_index >= data_len: break
        if data_index >= data_len: break
        
    # Note: Must be saved as PNG to prevent data loss due to compression
    cv2.imwrite(output_path, img)
    print(f"[Success] Message encoded! Image saved as '{output_path}'")

def decode_data(image_path):

    print(f"[Info] Reading image from '{image_path}'...")
    
    img = cv2.imread(image_path)
    
    if img is None:
        print("[Error] Image could not be read.")
        return ""
    
    binary_data = ""
    rows, cols, channels = img.shape
    
    for row in range(rows):
        for col in range(cols):
            for channel in range(3):
                pixel = img[row, col, channel]
                
                binary_data += str(pixel & 1)
                
    decoded_message = binary_to_text(binary_data)
    return decoded_message

if __name__ == "__main__":
    banner = r"""
   ______ ____ _   _ 
  / _____|_  _| \ | |
 | |       | ||  \| |
 | |_____ _| || |\  |
  \______|____|_| \_|
  
  Code Inside Nothing 
    """
    print(banner)
    print("========================================")
    print(" [1] Encode (Hide Message into Image)")
    print(" [2] Decode (Read Message from Image)")
    print(" [Q] Quit")
    print("========================================")
    
    choice = input("\nroot@cin:~$ Select option (1/2): ")
    
    if choice == '1':
        input_file = "input_image.png" # Make sure this file exists
        output_file = "encoded_image.png"
        
        if not os.path.exists(input_file):
            print(f"\n[!] Error: '{input_file}' not found.")
        else:
            message = input("Enter secret message: ")
            encode_data(input_file, message, output_file)
            
    elif choice == '2':
        target_file = "encoded_image.png"
        
        if not os.path.exists(target_file):
             print(f"\n[!] Error: '{target_file}' not found.")
        else:
            hidden_msg = decode_data(target_file)
            print(f"\n[+] DECODED MESSAGE: {hidden_msg}")
            
    elif choice.lower() == 'q':
        print("\n[!] Exiting...")
        exit()
        
    else:
        print("\n[!] Invalid selection.")