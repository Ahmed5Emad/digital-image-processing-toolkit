# Image Destroyer - Code Documentation

This document explains the codebase for the Image Destroyer tool.

## gui.py
- **`ModernButton` class**: A subclass of `QPushButton` that standardizes appearance. Sets a fixed minimum height and changes the mouse cursor to a pointing hand on hover.
- **`ImageDestroyerGUI` class**: The main controller for the application.
  - **`__init__`**: Initializes state variables for `original_image` and `current_image`.
  - **`init_ui`**: Constructs the application layout. Uses `QHBoxLayout` to split the window into a left-side `sidebar` (control panel) and a right-side `preview_container`.
  - **`load_image` / `save_image`**: Uses `QFileDialog` to handle file system interactions. Images are loaded as NumPy arrays using `cv2.imread`.
  - **`apply_effect`**: A higher-order function that takes a processing function as an argument, applies it to `self.current_image`, and calls `update_preview`.
  - **`update_preview`**: Converts OpenCV images (BGR format) to `QImage` (compatible with PyQt6). It handles both color and grayscale images, scaling the `QPixmap` to fit within the `QScrollArea`.

## processor.py
This module contains the logic for image corruption using `numpy` and `cv2`.
- **`to_grayscale`**: Checks the shape of the image array to ensure it is in grayscale before converting.
- **`add_gaussian_noise` / `add_speckle_noise`**: Generates a noise array matching the input image shape using `np.random` (normal or randn), adds it to the original image, and uses `np.clip` to keep values between 0 and 255.
- **`add_salt_and_pepper_noise`**: Calculates a number of salt (255) and pepper (0) pixels based on the `amount` parameter and uses random coordinate indices to directly modify the image array.
- **`add_periodic_noise`**: Uses `np.meshgrid` to generate a sinusoidal signal that is added to the image to simulate wave-like interference.
- **`add_uniform_noise` / `add_rayleigh_noise` / `add_exponential_noise`**: Uses specific NumPy probability distribution functions (`uniform`, `rayleigh`, `exponential`) to generate the noise array.
