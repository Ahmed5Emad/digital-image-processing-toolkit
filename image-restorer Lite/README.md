# Image Restorer - Code Documentation

This document explains the codebase for the Image Restorer tool.

## restorer_gui.py
- **`FILTERS_CONFIG`**: A dictionary that maps filter categories (e.g., "POINT", "SMOOTHING") to a list of tuples. Each tuple contains the display name and the reference to the corresponding processing function in `src/processors/`. This structure allows for dynamic GUI generation.
- **`ImageRestorerGUI` class**: The main controller for the application.
  - **`init_ui`**: Initializes the layout and dynamically iterates over `FILTERS_CONFIG` to construct the sidebar with labeled sections and filter buttons.
  - **`_make_callback`**: A helper method that creates a proper closure for each filter button, ensuring the correct function is called when clicked, bypassing Python lambda scoping issues.
  - **`update_preview` / `_display_image`**: Manages the side-by-side display. `_display_image` is a reusable method to convert NumPy arrays to `QPixmap` and display them in a specified `QLabel`. `update_preview` calls this twice to update both the original and restored image displays.

## src/processors/
This module contains the logic for image restoration using `numpy` and `cv2`.
- **`ensure_gray` decorator**: A higher-order function that wraps image processing functions. It detects if an image is color (3 channels), converts it to grayscale, applies the function, and then converts the result back to BGR (if applicable), ensuring algorithms that only support grayscale work seamlessly on color images.
- **Filter Functions**:
  - **Point Processing**: Implements `negative`, `thresholding` (binary), `log_transformation`, `gamma_transformation`, `contrast_stretching` (piecewise linear), `gray_level_slicing`, and `bit_plane_slicing`.
  - **Spatial Filters**: Uses `cv2.blur` (`arithmetic_mean_filter`), `cv2.medianBlur` (`median_filter`), and custom implementations for `geometric_mean_filter`, `harmonic_mean_filter`, `contraharmonic_mean_filter` using NumPy vectorized operations for performance.
  - **Sharpening**: Implements `laplacian_sharpening`, `sobel_sharpening`, `prewitt_sharpening`, and `roberts_sharpening` using `cv2.filter2D` or specialized OpenCV functions like `cv2.Laplacian` and `cv2.Sobel`, combined with `cv2.convertScaleAbs` for correct output format.
  - **Frequency Domain**: `butterworth_highpass_filter` uses `np.fft.fft2` to convert the image to the frequency domain, applies a Butterworth mask, and converts it back using `np.fft.ifft2`.
