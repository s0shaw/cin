# 🧞 CIN (Code Inside Nothing)

**CIN** is a Python-based command-line tool developed as a project for the **Image Processing** course. It implements **LSB (Least Significant Bit) Steganography** to hide secret text messages inside PNG images without noticeably altering their visual appearance.

-----

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Arastaci/cin.git
    cd cin
    ```

2.  **Install dependencies:**
    This project requires `OpenCV` and `NumPy`.

    ```bash
    pip install opencv-python numpy
    ```

-----

## Usage

### 1\. Preparation

Place the image you want to use as a cover in the project folder and name it **`input_image.png`**.

> **Note:** The input image supports **PNG** and **JPG**, but the output will always be saved as **PNG** to prevent data loss.

### 2\. Run the Tool

```bash
python cin.py
```

### 3\. Modes

  * **[1] Encode:** \* The tool reads `input_image.png`.

      * Asks for your secret message.
      * Saves the result as **`encoded_image.png`**.

  * **[2] Decode:**

      * The tool reads `encoded_image.png`.
      * Extracts and displays the hidden message in the terminal.

-----

## How it Works (LSB Algorithm)

CIN uses the **Least Significant Bit (LSB)** technique.

1.  **Binary Conversion:** The secret text is converted into binary (0s and 1s).
2.  **Pixel Manipulation:** The script iterates through the image pixels.
3.  **Bit Replacement:** It replaces the last bit of each color channel (Red, Green, Blue) with a bit from the secret message.
4.  **Delimiter:** A special delimiter (`#####`) is added to the end of the message so the decoder knows when to stop reading.
