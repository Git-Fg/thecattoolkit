#!/usr/bin/env python3
"""
Rendering utilities for presentation tasks.
Duplicated from sys-multimodal to maintain plugin independence.
See CLAUDE.md: Cross-Plugin Import Anti-Pattern (CRITICAL)
"""

from pathlib import Path
from typing import List, Optional

try:
    from PIL import Image
except ImportError:
    Image = None

# Try to import pymupdf (preferred - no external dependencies)
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


def combine_images_to_pdf(image_paths: List[Path], output_path: Path,
                         dpi: int = 150, verbose: bool = False) -> bool:
    """
    Combine multiple images into a single PDF.

    Args:
        image_paths: List of image file paths
        output_path: Output PDF path
        dpi: Resolution for the PDF (default: 150)
        verbose: Print progress information

    Returns:
        True if successful, False otherwise
    """
    if Image is None:
        print("Error: Pillow library not found. Install with: pip install Pillow")
        return False

    if not image_paths:
        if verbose:
            print("Error: No image files found")
        return False

    if verbose:
        print(f"Combining {len(image_paths)} images into PDF...")

    # Load all images
    images = []
    for i, img_path in enumerate(image_paths):
        try:
            img = Image.open(img_path)
            # Convert to RGB if necessary (PDF doesn't support RGBA)
            if img.mode in ('RGBA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            images.append(img)

            if verbose:
                print(f"  [{i+1}/{len(image_paths)}] Loaded: {img_path.name} ({img.size[0]}x{img.size[1]})")
        except Exception as e:
            if verbose:
                print(f"Error loading {img_path}: {e}")
            return False

    if not images:
        if verbose:
            print("Error: No images could be loaded")
        return False

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save as PDF
    try:
        # First image
        first_image = images[0]

        # Remaining images (if any)
        remaining_images = images[1:] if len(images) > 1 else []

        # Save to PDF
        first_image.save(
            output_path,
            "PDF",
            resolution=dpi,
            save_all=True,
            append_images=remaining_images
        )

        if verbose:
            print(f"\nPDF created: {output_path}")
            print(f"  Total slides: {len(images)}")
            file_size = output_path.stat().st_size
            if file_size > 1024 * 1024:
                print(f"  File size: {file_size / (1024 * 1024):.1f} MB")
            else:
                print(f"  File size: {file_size / 1024:.1f} KB")

        return True
    except Exception as e:
        if verbose:
            print(f"Error creating PDF: {e}")
        return False
    finally:
        # Close all images
        for img in images:
            img.close()


class PDFToImagesConverter:
    """Converts PDF presentations to images."""

    def __init__(
        self,
        pdf_path: str,
        output_prefix: str,
        dpi: int = 150,
        format: str = 'jpg',
        first_page: Optional[int] = None,
        last_page: Optional[int] = None
    ):
        self.pdf_path = Path(pdf_path)
        self.output_prefix = output_prefix
        self.dpi = dpi
        self.format = format.lower()
        self.first_page = first_page
        self.last_page = last_page

        # Validate format
        if self.format not in ['jpg', 'jpeg', 'png']:
            raise ValueError(f"Unsupported format: {format}. Use jpg or png.")

    def convert(self, verbose: bool = True) -> List[Path]:
        """Convert PDF to images using PyMuPDF."""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        if verbose:
            print(f"Converting: {self.pdf_path.name}")
            print(f"Output prefix: {self.output_prefix}")
            print(f"DPI: {self.dpi}")
            print(f"Format: {self.format}")

        if HAS_PYMUPDF:
            return self._convert_with_pymupdf(verbose)
        else:
            raise RuntimeError(
                "PyMuPDF not installed. Install it with:\n"
                "  pip install pymupdf\n\n"
                "PyMuPDF is a self-contained library - no external dependencies needed."
            )

    def _convert_with_pymupdf(self, verbose: bool = True) -> List[Path]:
        """Convert using PyMuPDF library (no external dependencies)."""
        if verbose:
            print("Using PyMuPDF (no external dependencies required)...")

        # Open the PDF
        doc = fitz.open(self.pdf_path)

        # Determine page range
        start_page = (self.first_page - 1) if self.first_page else 0
        end_page = self.last_page if self.last_page else doc.page_count

        # Calculate zoom factor from DPI (72 DPI is the base)
        zoom = self.dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        output_files = []
        output_dir = Path(self.output_prefix).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        for page_num in range(start_page, end_page):
            page = doc[page_num]

            # Render page to pixmap
            pixmap = page.get_pixmap(matrix=matrix)

            # Determine output path
            output_path = Path(f"{self.output_prefix}-{page_num + 1:03d}.{self.format}")

            # Save the image
            if self.format in ['jpg', 'jpeg']:
                pixmap.save(str(output_path), output="jpeg")
            else:
                pixmap.save(str(output_path), output="png")

            output_files.append(output_path)
            if verbose:
                print(f"  Created: {output_path.name}")

        doc.close()
        return output_files
