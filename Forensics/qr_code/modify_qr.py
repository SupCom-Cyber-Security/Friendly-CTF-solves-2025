import os
from PIL import Image
import numpy as np

# Load QR code
qr = Image.open("wav.png").convert("RGB")
qr_np = np.array(qr)

# Create a CHECKERBOARD pattern overlay (much harder to scan)
overlay = np.zeros_like(qr_np)
height, width, _ = qr_np.shape

# Create checkerboard pattern
block_size = 20
for i in range(0, height, block_size):
    for j in range(0, width, block_size):
        if (i // block_size + j // block_size) % 2 == 0:
            overlay[i:i+block_size, j:j+block_size, 0] = 255  # Red
            overlay[i:i+block_size, j:j+block_size, 1] = 255
            overlay[i:i+block_size, j:j+block_size, 2] = 125

obfuscated = np.bitwise_xor(qr_np, overlay)
Image.fromarray(obfuscated).save("qr_obfuscated.png")
print("Saved with checkerboard pattern - very hard to scan")