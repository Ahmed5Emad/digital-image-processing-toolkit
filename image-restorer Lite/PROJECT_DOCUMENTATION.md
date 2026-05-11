# Comprehensive Technical Documentation: Image Restorer Lite

## 1. Project Structure
```text
image-restorer-Lite/
├── restorer_gui.py         # Main GUI application logic (PyQt6)
└── src/
    └── processors/         # Core image processing logic
        ├── intensity.py    # Pixel-wise intensity transformations
        ├── frequency.py    # Frequency domain filtering (FFT)
        ├── utils.py        # Shared decorators and helper functions
        └── spatial/        # Spatial domain filtering (Kernels)
            ├── sharpening.py
            └── smoothing.py
```

---

## 2. Project Overview
The **Image Restorer Lite** is a desktop application built with Python and **PyQt6** for digital image processing. It provides a modern GUI to perform various intensity-based, spatial, and frequency-domain filtering techniques on images.

---

## 3. Architecture & Workflow

### Application Flow
1.  **Configuration Driven UI**: The application is driven by a master configuration dictionary (`FILTERS_CONFIG`) located in `restorer_gui.py`. This structure dynamically generates the sidebar buttons and parameter adjustment panels.
2.  **Event Handling**: When a filter is selected, `restorer_gui.py` initiates an "adjustment mode," hiding the main UI elements and showing parameter controls (sliders/spinboxes) for that specific function.
3.  **Processing Pipeline**:
    *   The `ensure_gray` decorator in `src/processors/utils.py` acts as a middleware to ensure compatibility for algorithms requiring grayscale inputs.
    *   All processing functions take `image` (NumPy array) as the first argument, followed by `**kwargs` for parameter tuning.
4.  **Live Preview**: A `QTimer` is used to debounced filter application, ensuring the GUI doesn't freeze when adjusting parameters for computationally expensive operations (especially Frequency domain).

---

## 4. Detailed Component Breakdown

### A. The GUI Controller (`restorer_gui.py`)

#### `FILTERS_CONFIG`
This dictionary defines the entire UI structure. Each entry is structured as:
`"CATEGORY": [("Display Name", function_reference, [metadata_list])]`

*   **Metadata Schema**:
    *   `arg`: The keyword argument name the filter function expects.
    *   `type`: 'int', 'float', 'odd', or 'choice' (affects UI generation).
    *   `min`, `max`, `default`: Used to configure sliders and spinboxes.

#### `ParameterWidget` class
This is the GUI generator.
*   **Logic**: It inspects the `type` field in the metadata to decide which PyQt6 widget to instantiate (`QSlider` for range, `QSpinBox` for precision, `QComboBox` for choices).
*   **Signaling**: It emits a `valueChanged` signal that triggers the `live_preview` method in the main window.

#### `ImageRestorerGUI(QMainWindow)`
The main application controller.
*   **Key Methods**:
    *   `enter_adjustment_mode`: Switches UI from sidebar to top-bar parameter adjustment.
    *   `live_preview`: Triggers a delayed update for frequency filters or immediate update for others.
    *   `_run_live_preview`: Core method that copies the snapshot, applies the active filter with current parameters, and updates the view.
    *   `update_preview`: Calls `_display_image` for both original and processed image labels.

---

### B. Core Processors (`src/processors/`)

#### 1. Utilities (`utils.py`)
*   **`ensure_gray(func)` (Decorator)**: Ensures input images are grayscale for processing and restores them to BGR if output is grayscale.
*   **`apply_blend(image, edges, blend_mode)`**: Blends original image with edge maps based on `Edges Only`, `Add (+)`, or `Subtract (-)`.

#### 2. Intensity Processing (`intensity.py`)
Pixel-wise transformations that do not depend on neighboring pixel values.

*   **`negative(image)`**: Inverts pixel values (`255 - pixel`).
*   **`thresholding(image, threshold_value, max_value)`**: Applies binary threshold.
*   **`log_transformation(image)`**: Applies logarithmic transform for dynamic range compression.
*   **`gamma_transformation(image, gamma)`**: Applies power-law gamma correction.
*   **`gray_level_slicing(image, r1, r2, ...)`**: Highlights pixels in a specific intensity range.
*   **`bit_plane_slicing(image, plane)`**: Extracts a specific bit plane of the image.
*   **`histogram_equalization(image)`**: Enhances contrast via `cv2.equalizeHist`.

#### 3. Frequency Domain (`frequency.py`)
These filters work in the Fourier domain.
*   **`_apply_filter(image, mask)`**: Core function: `FFT -> Shift -> Mask -> Inverse Shift -> Inverse FFT`.
*   **`ideal_filter(image, cutoff, type)`**: Wrapper for Ideal Low/Highpass filters.
*   **`butterworth_filter(image, cutoff, n, type)`**: Wrapper for Butterworth Low/Highpass filters.
*   **`gaussian_filter(image, cutoff, type)`**: Wrapper for Gaussian Low/Highpass filters.

#### 4. Spatial Domain (`spatial/`)
*   **`smoothing.py`**:
    *   **`arithmetic_mean_filter(image, kernel_size)`**: Blurs using `cv2.blur`.
    *   **`median_filter(image, kernel_size)`**: Removes salt-and-pepper noise using `cv2.medianBlur`.
*   **`sharpening.py`**:
    *   **`laplacian_sharpening(image, blend_mode)`**: Edge detection using `cv2.Laplacian`.
    *   **`sobel_sharpening(image, ksize, blend_mode)`**: Edge detection using `cv2.Sobel`.

---

## 5. In-Depth Code Examples

### Frequency Masking Implementation (`frequency.py`)
This snippet shows how the Butterworth mask is dynamically created.
```python
def butterworth_highpass_filter(image, cutoff=30, n=2, **kwargs):
    rows, cols = image.shape
    # Get distance from center of frequency spectrum
    D = _get_distance_matrix(rows, cols)
    # Butterworth formula: 1 / (1 + (cutoff/D)^(2n))
    # 1e-6 prevents division by zero
    mask = 1 / (1 + (cutoff / (D + 1e-6))**(2 * n))
    return _apply_filter(image, mask)
```

### Grayscale Enforcement Logic (`utils.py`)
This decorator wraps any processor function to handle color image conversion transparently.
```python
def ensure_gray(func):
    @wraps(func)
    def wrapper(image, *args, **kwargs):
        # Check if color image
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            result = func(gray, *args, **kwargs)
            # Re-convert to BGR if processing produced grayscale output
            if len(result.shape) == 2:
                return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            return result
        # Already grayscale, proceed
        return func(image, *args, **kwargs)
    return wrapper
```
