#!/usr/bin/env python3
"""
Script to invert image colors and remove background for web logo use
"""

from PIL import Image, ImageOps
import numpy as np
import sys
import os

def invert_and_remove_background(input_path, output_path=None):
    """
    Invert image colors and remove background (make transparent)
    """
    # Open the image
    img = Image.open(input_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get original pixel data to identify background
    img_array = np.array(img)
    original_data = img_array.copy()
    
    # Invert RGB channels, keep alpha channel
    img_array[:, :, 0] = 255 - img_array[:, :, 0]  # Red
    img_array[:, :, 1] = 255 - img_array[:, :, 1]  # Green
    img_array[:, :, 2] = 255 - img_array[:, :, 2]  # Blue
    
    # Create image from inverted array
    inverted_img = Image.fromarray(img_array, 'RGBA')
    
    # Remove background - make dark pixels (originally dark background) transparent
    data = inverted_img.getdata()
    original_pixels = original_data.reshape(-1, 4)
    new_data = []
    
    for idx, item in enumerate(data):
        # Check the ORIGINAL pixel value (before inversion)
        # If it was dark (background), make it transparent after inversion
        orig = original_pixels[idx]
        if orig[0] < 50 and orig[1] < 50 and orig[2] < 50:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)
    
    inverted_img.putdata(new_data)
    
    # Determine output path
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_inverted.png"
    
    # Save as PNG to preserve transparency
    inverted_img.save(output_path, 'PNG')
    print(f"Processed: {input_path}")
    print(f"Saved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python invert_logo.py <input_image> [output_image]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    invert_and_remove_background(input_file, output_file)
