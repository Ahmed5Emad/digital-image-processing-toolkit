# Digital Image Processing Toolkit

This repository contains a collection of tools for digital image processing, designed to help study and experiment with various image manipulation and restoration techniques.

## Project Structure

- `image-destroyer/`: A tool for generating noisy and distorted images, useful for testing the robustness of image processing algorithms.
- `image-restorer/`: A comprehensive toolkit for applying image restoration and enhancement filters.

## Tools Overview

### Image Destroyer
An application to systematically apply various types of noise (Gaussian, Salt & Pepper, Speckle, etc.) and transformations (Blur) to images. It serves as a data-generator for testing restoration algorithms.

### Image Restorer
A professional-grade toolkit that implements a wide suite of digital image processing filters, including:
- **Point Processing**: Intensity transformations and thresholding.
- **Histogram Processing**: Equalization and contrast adjustment.
- **Smoothing Filters**: Various mean, median, and order statistics filters.
- **Sharpening**: Laplacian, Sobel, and other gradient-based filters.
- **Frequency Domain**: Fast Fourier Transform-based filtering.

## Dependencies
This project uses:
- `Python 3.x`
- `PyQt6` for the graphical user interface.
- `OpenCV` (`cv2`) for image processing operations.
- `NumPy` for numerical data manipulation.

## Setup
It is recommended to use the provided virtual environment:
```bash
# Create and activate environment if needed
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install opencv-python PyQt6 numpy
```
