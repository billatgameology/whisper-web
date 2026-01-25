# Image Optimization Script

This script optimizes images for web use by compressing them to be under a target file size while maintaining visual quality.

## Requirements

```bash
pip install Pillow
```

## Usage

### Optimize a single image

```bash
python optimize_images.py hero.jpeg
```

This will create `hero_optimized.jpeg` in the same directory.

### Specify custom output path

```bash
python optimize_images.py hero.jpeg -o hero_web.jpeg
```

### Optimize all images in a directory

```bash
python optimize_images.py /path/to/images/
```

### Custom options

```bash
# Target size of 500KB instead of 1MB
python optimize_images.py hero.jpeg -s 0.5

# Maximum dimension of 1200px
python optimize_images.py hero.jpeg -d 1200

# Starting quality of 90
python optimize_images.py hero.jpeg -q 90

# Combine options
python optimize_images.py hero.jpeg -s 0.8 -d 1600 -q 90 -o hero_final.jpeg
```

## Options

- `-o, --output`: Output file path (for single file only)
- `-s, --size`: Target maximum size in MB (default: 1.0)
- `-d, --dimension`: Maximum width/height in pixels (default: 1920)
- `-q, --quality`: Starting JPEG quality 1-95 (default: 85)

## Features

- Automatically resizes images that are too large
- Progressively reduces quality to meet target file size
- Converts RGBA/PNG to RGB/JPEG
- Batch processing support
- Preserves image aspect ratio
