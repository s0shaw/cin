# CIN (Code Inside Nothing)

**CIN** is a Python-based **Command Line Tool** developed as a project for the **Image Processing** course. It implements **LSB (Least Significant Bit) Steganography** to hide secret text messages inside PNG images without noticeably altering their visual appearance.

-----

## Setup

You can clone the repository and install the necessary dependencies with these commands:

```bash
git clone https://github.com/Arastaci/cin.git && cd cin
pip install -r requirements.txt
```

---

## Usage

CIN is a pure CLI tool. You can run it with arguments to perform operations instantly.

### General Syntax

```bash
python cin.py [MODE] [ARGUMENTS]
```

### 1. Encode (Hide Data)

Hides a secret message inside an image.

* **Basic Usage:**
```bash
python cin.py -e -i input.png -m "This is a secret message"
```

* **Custom Output Filename:**
```bash
python cin.py -e -i input.png -m "Hello World" -o secret_result.png
```

### 2. Decode (Read Data)

Extracts the hidden message from an encoded image.

```bash
python cin.py -d -i output.png
```

### 3. Visualize (Bit Plane Slicing)

Creates a visual map of the Least Significant Bits. This is used to demonstrate where the data is hidden by highlighting the modified pixels.

```bash
python cin.py -v -i output.png
```

> *This will generate a `visualization.png` file where white dots represent the LSB noise pattern.*

### 4. Compare (Find Differences)

Compares two images and highlights the differences with red rectangles.

* **Basic Usage:**
```bash
python cin.py -c -i image1.png -i2 image2.png
```

* **Custom Sensitivity (lower = more sensitive):**
```bash
python cin.py -c -i image1.png -i2 image2.png -t 15 -o differences.png
```

> *This will generate an output image with red boxes marking all detected differences.*

---

## Arguments Reference

| Argument | Full Flag | Description |
| --- | --- | --- |
| **-e** | `--encode` | Enable **Hide Mode**. Requires `-i` and `-m`. |
| **-d** | `--decode` | Enable **Read Mode**. Requires `-i`. |
| **-v** | `--visualize` | Enable **Visualization Mode**. Requires `-i`. |
| **-c** | `--compare` | Enable **Compare Mode**. Requires `-i` and `-i2`. |
| **-i** | `--input` | Path to the source image file (Required). |
| **-i2** | `--input2` | Path to second image (Required for compare). |
| **-o** | `--output` | Path for the saved image (Default: `output.png`). |
| **-m** | `--message` | The text message to hide (Required for encoding). |
| **-t** | `--threshold` | Sensitivity for compare mode (Default: 30). |

---

## Technical Details

### 1. LSB Algorithm

CIN manipulates the last bit (8th bit) of pixel values. Since the change is only +/- 1 in value (e.g., changing a Red value from 200 to 201), the human eye cannot detect the difference.

* **Original Pixel:** `1101001[0]` (Even Number)
* **Modified Pixel:** `1101001[1]` (Odd Number - Message Bit Inserted)

### 2. Bit Plane Slicing (Visualization)

To prove that data is hidden, the visualization mode extracts only the LSB plane.

* **Logic:** `Pixel Value & 1` -> If 1, make it White (255); if 0, make it Black (0).
* **Result:** A noisy image showing exactly where the text bits are stored.

### 3. Capacity Check

The script calculates `Width * Height * 3` to determine the maximum bit capacity of the image. If your message is too long, the program prevents execution to avoid data loss.