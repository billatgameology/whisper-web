#!/usr/bin/env python3
"""
Convert PDF pages to JPEG images
Usage: python3 pdf_to_jpeg.py <input_pdf> <output_folder>
Example: python3 pdf_to_jpeg.py menu.pdf photos/
"""

import sys
import os
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])
    import fitz

def pdf_to_jpeg(pdf_path, output_folder, dpi=300):
    """
    Convert each page of a PDF to a JPEG image
    
    Args:
        pdf_path: Path to input PDF file
        output_folder: Folder to save output JPEG files
        dpi: Resolution for output images (default 300)
    """
    # Create output folder if it doesn't exist
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Get base filename without extension
    base_name = Path(pdf_path).stem
    
    print(f"Converting {len(pdf_document)} page(s) from {pdf_path}...")
    
    # Convert each page
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_num]
        
        # Calculate zoom factor for desired DPI
        zoom = dpi / 72  # 72 is the default DPI
        mat = fitz.Matrix(zoom, zoom)
        
        # Render page to an image
        pix = page.get_pixmap(matrix=mat)
        
        # Generate output filename
        output_file = output_path / f"{base_name}_page{page_num + 1}.jpg"
        
        # Save as JPEG
        pix.save(output_file, "jpeg")
        print(f"  Saved: {output_file}")
    
    pdf_document.close()
    print(f"\nConversion complete! {len(pdf_document)} page(s) saved to {output_folder}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_to_jpeg.py <input_pdf> [output_folder] [dpi]")
        print("Example: python3 pdf_to_jpeg.py menu.pdf photos/ 300")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else "."
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found")
        sys.exit(1)
    
    pdf_to_jpeg(pdf_path, output_folder, dpi)
