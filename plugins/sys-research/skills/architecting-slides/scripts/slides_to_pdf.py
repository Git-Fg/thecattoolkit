#!/usr/bin/env python3
"""
Combine slide images into a single PDF presentation.

This script takes multiple slide images (PNG, JPG) and combines them
into a single PDF file, maintaining aspect ratio and quality.

Usage:
    # Combine all PNG files in a directory
    python slides_to_pdf.py slides/*.png -o presentation.pdf
    
    # Combine specific files in order
    python slides_to_pdf.py slide_01.png slide_02.png slide_03.png -o presentation.pdf
    
    # From a directory (sorted by filename)
    python slides_to_pdf.py slides/ -o presentation.pdf
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List

# Add the toolkit plugin path to sys.path to allow importing from other plugins
# This is a bit of a hack but ensures portability across different environments
toolkit_root = Path(__file__).resolve().parents[4]
multimodal_utils = toolkit_root / "plugins" / "sys-multimodal"
if multimodal_utils.exists() and str(multimodal_utils) not in sys.path:
    sys.path.append(str(multimodal_utils))

try:
    from utils.rendering import combine_images_to_pdf
except ImportError:
    # Fallback to local implementation if multimodal plugin is not available
    # but we want to encourage using the shared one
    print("Warning: Could not import from sys-multimodal. Ensure sys-multimodal utility is present.")
    sys.exit(1)


def get_image_files(paths: List[str]) -> List[Path]:
    """
    Get list of image files from paths (files or directories).
    
    Args:
        paths: List of file paths or directory paths
        
    Returns:
        Sorted list of image file paths
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
    image_files = []
    
    for path_str in paths:
        path = Path(path_str)
        
        if path.is_file():
            if path.suffix.lower() in image_extensions:
                image_files.append(path)
            else:
                print(f"Warning: Skipping non-image file: {path}")
        elif path.is_dir():
            # Get all images in directory
            for ext in image_extensions:
                image_files.extend(path.glob(f"*{ext}"))
                image_files.extend(path.glob(f"*{ext.upper()}"))
        else:
            # Try glob pattern
            parent = path.parent
            pattern = path.name
            if parent.exists():
                matches = list(parent.glob(pattern))
                for match in matches:
                    if match.suffix.lower() in image_extensions:
                        image_files.append(match)
    
    # Remove duplicates and sort
    image_files = list(set(image_files))
    image_files.sort(key=lambda x: x.name)
    
    return image_files



def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Combine slide images into a single PDF presentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Combine PNG files using glob pattern
  python slides_to_pdf.py slides/*.png -o presentation.pdf
  
  # Combine specific files in order
  python slides_to_pdf.py title.png intro.png methods.png results.png -o talk.pdf
  
  # Combine all images from a directory (sorted by filename)
  python slides_to_pdf.py slides/ -o presentation.pdf
  
  # With custom DPI and verbose output
  python slides_to_pdf.py slides/*.png -o presentation.pdf --dpi 200 -v

Supported formats: PNG, JPG, JPEG, GIF, WEBP, BMP

Tips:
  - Name your slide images with numbers for correct ordering:
    01_title.png, 02_intro.png, 03_methods.png, etc.
  - Use the generate_slide_image.py script to create slides first
  - Standard presentation aspect ratio is 16:9 (1920x1080 or 1280x720)
        """
    )
    
    parser.add_argument("images", nargs="+", 
                       help="Image files, directories, or glob patterns")
    parser.add_argument("-o", "--output", required=True,
                       help="Output PDF file path")
    parser.add_argument("--dpi", type=int, default=150,
                       help="PDF resolution in DPI (default: 150)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    # Get image files
    image_files = get_image_files(args.images)
    
    if not image_files:
        print("Error: No image files found matching the specified paths")
        print("\nUsage examples:")
        print("  python slides_to_pdf.py slides/*.png -o presentation.pdf")
        print("  python slides_to_pdf.py slide1.png slide2.png -o presentation.pdf")
        sys.exit(1)
    
    print(f"Found {len(image_files)} image(s)")
    if args.verbose:
        for f in image_files:
            print(f"  - {f}")
    
    # Combine into PDF
    output_path = Path(args.output)
    success = combine_images_to_pdf(
        image_files, 
        output_path, 
        dpi=args.dpi, 
        verbose=args.verbose
    )
    
    if success:
        print(f"\n✓ PDF created: {output_path}")
        sys.exit(0)
    else:
        print(f"\n✗ Failed to create PDF")
        sys.exit(1)


if __name__ == "__main__":
    main()
