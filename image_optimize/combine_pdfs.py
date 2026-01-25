#!/usr/bin/env python3
"""
Combine multiple PDF files into one.
"""
from pypdf import PdfWriter
import sys
import os

def combine_pdfs(output_filename, *input_files):
    """Combine multiple PDF files into one output file."""
    writer = PdfWriter()
    
    for pdf_file in input_files:
        if not os.path.exists(pdf_file):
            print(f"Error: File not found: {pdf_file}")
            sys.exit(1)
        
        writer.append(pdf_file)
        print(f"Added: {pdf_file}")
    
    with open(output_filename, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"\nCombined PDF created: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 combine_pdfs.py output.pdf input1.pdf input2.pdf ...")
        sys.exit(1)
    
    output = sys.argv[1]
    inputs = sys.argv[2:]
    
    combine_pdfs(output, *inputs)
