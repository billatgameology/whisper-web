#!/usr/bin/env python3
"""
Image Optimization Script for Web Use
Compresses images to be under 1MB while maintaining quality
"""

import os
import sys
from PIL import Image
import argparse

def get_file_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def optimize_image(input_path, output_path=None, target_size_mb=1.0, max_dimension=1920, quality=85):
    """
    Optimize an image for web use
    
    Args:
        input_path: Path to input image
        output_path: Path to save optimized image (if None, creates '_optimized' version)
        target_size_mb: Target maximum file size in MB
        max_dimension: Maximum width or height
        quality: Initial JPEG quality (1-95)
    """
    # Open image
    img = Image.open(input_path)
    
    # Convert RGBA to RGB if necessary
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize if image is too large
    width, height = img.size
    if width > max_dimension or height > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        else:
            new_height = max_dimension
            new_width = int(width * (max_dimension / height))
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"  Resized from {width}x{height} to {new_width}x{new_height}")
    
    # Set output path
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_optimized{ext}"
    
    # Try different quality settings to get under target size
    current_quality = quality
    min_quality = 20
    
    while current_quality >= min_quality:
        img.save(output_path, 'JPEG', quality=current_quality, optimize=True)
        file_size_mb = get_file_size_mb(output_path)
        
        if file_size_mb <= target_size_mb:
            print(f"  Optimized: {file_size_mb:.2f}MB at quality {current_quality}")
            return output_path, file_size_mb
        
        # Reduce quality and try again
        current_quality -= 5
    
    # If still too large, try more aggressive resizing
    print(f"  Warning: Could not reach target size with current dimensions")
    print(f"  Final size: {file_size_mb:.2f}MB at quality {min_quality}")
    return output_path, file_size_mb

def batch_optimize(directory, target_size_mb=1.0, max_dimension=1920, quality=85):
    """Optimize all images in a directory"""
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp')
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(supported_formats) and '_optimized' not in filename:
            input_path = os.path.join(directory, filename)
            original_size = get_file_size_mb(input_path)
            
            print(f"\nProcessing: {filename} ({original_size:.2f}MB)")
            
            try:
                output_path, new_size = optimize_image(
                    input_path,
                    target_size_mb=target_size_mb,
                    max_dimension=max_dimension,
                    quality=quality
                )
                reduction = ((original_size - new_size) / original_size) * 100
                print(f"  ✓ Saved {reduction:.1f}% - {output_path}")
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Optimize images for web use')
    parser.add_argument('input', help='Input image file or directory')
    parser.add_argument('-o', '--output', help='Output file path (for single file only)')
    parser.add_argument('-s', '--size', type=float, default=1.0, 
                       help='Target maximum size in MB (default: 1.0)')
    parser.add_argument('-d', '--dimension', type=int, default=1920,
                       help='Maximum width/height in pixels (default: 1920)')
    parser.add_argument('-q', '--quality', type=int, default=85,
                       help='Starting JPEG quality 1-95 (default: 85)')
    
    args = parser.parse_args()
    
    if os.path.isfile(args.input):
        # Single file
        original_size = get_file_size_mb(args.input)
        print(f"Processing: {args.input} ({original_size:.2f}MB)")
        
        output_path, new_size = optimize_image(
            args.input,
            args.output,
            args.size,
            args.dimension,
            args.quality
        )
        reduction = ((original_size - new_size) / original_size) * 100
        print(f"✓ Saved {reduction:.1f}% - {output_path}")
        
    elif os.path.isdir(args.input):
        # Directory
        print(f"Batch processing directory: {args.input}")
        batch_optimize(args.input, args.size, args.dimension, args.quality)
        
    else:
        print(f"Error: '{args.input}' is not a valid file or directory")
        sys.exit(1)

if __name__ == '__main__':
    main()
