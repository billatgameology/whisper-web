#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add image_optimize to path
sys.path.insert(0, 'image_optimize')
from optimize_images import optimize_image

# Directories
foods_dir = Path('FOODS')
output_dir = Path('FOODS_optimized')

# Process all images
for img_file in foods_dir.glob('*'):
    if img_file.suffix.lower() in ['.jpg', '.jpeg']:
        output_name = img_file.stem.lower() + '.jpg'
        output_path = output_dir / output_name
        
        print(f"\nProcessing: {img_file.name}")
        try:
            optimize_image(
                str(img_file),
                str(output_path),
                target_size_mb=0.5,
                max_dimension=1200,
                quality=85
            )
            print(f"  ✓ Saved to {output_path}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

print("\n✓ All food photos optimized!")
