#!/usr/bin/env python3
"""
Script to make white background in logo transparent
"""

from PIL import Image
import numpy as np
import sys
import os

def make_white_transparent(input_path, output_path=None, threshold=240):
    """
    Make white pixels in image transparent
    
    Args:
        input_path: Path to input image
        output_path: Path for output image (optional)
        threshold: RGB value threshold for considering pixels as white (default 240)
    """
    # Open the image
    img = Image.open(input_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get pixel data
    img_array = np.array(img)
    
    # Create a mask for white pixels (all RGB channels > threshold)
    white_mask = (img_array[:, :, 0] >= threshold) & \
                 (img_array[:, :, 1] >= threshold) & \
                 (img_array[:, :, 2] >= threshold)
    
    # Set alpha channel to 0 (transparent) for white pixels
    img_array[:, :, 3] = np.where(white_mask, 0, img_array[:, :, 3])
    
    # Create image from modified array
    transparent_img = Image.fromarray(img_array, 'RGBA')
    
    # Determine output path
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_transparent.png"
    
    # Ensure output is PNG (for transparency support)
    if not output_path.lower().endswith('.png'):
        output_path = os.path.splitext(output_path)[0] + '.png'
    
    # Save the image
    transparent_img.save(output_path, 'PNG')
    print(f"Transparent logo saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 make_logo_transparent.py <input_image> [output_image] [threshold]")
        print("Example: python3 make_logo_transparent.py logo.png logo_transparent.png 240")
        sys.exit(1)
    
    input_img = sys.argv[1]
    output_img = sys.argv[2] if len(sys.argv) > 2 else None
    threshold = int(sys.argv[3]) if len(sys.argv) > 3 else 240
    
    if not os.path.exists(input_img):
        print(f"Error: Input file '{input_img}' not found")
        sys.exit(1)
    
    make_white_transparent(input_img, output_img, threshold)
