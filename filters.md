### 1. Point Processing & Intensity Transformations
These are the simplest operations applied to individual pixels (often the very first step in enhancement) to adjust contrast or brightness.
*   **Negative Transformation:** Inverts the image (e.g., turning white to black) to enhance white/grey details embedded in dark regions.
*   **Identity Transformation:** A linear transformation that leaves the image unchanged.
*   **Logarithmic Transformation:** Stretches apart dark pixels while compressing bright pixels to reveal details in low-contrast areas. 
*   **Inverse Log Transformation:** Performs the exact opposite of the log transform.
*   **Power Law (Gamma) Transformations:** Includes **nth power** and **nth root** transformations. They map a narrow range of dark values into a wider range of outputs (or vice versa), and are heavily used to fix monitor display distortions (Gamma Correction).
*   **Contrast Stretching (Piecewise Linear Transformation):** An arbitrary, user-defined linear transform used to stretch the contrast of a poor-quality image.
*   **Thresholding:** Converts an image to binary (black and white) by setting pixels above a certain value to 1.0 and the rest to 0.0, which is highly useful for isolating an object from its background.
*   **Grey Level Slicing:** Highlights a specific range of grey levels while preserving or suppressing others.
*   **Bit Plane Slicing:** Separates an image into binary planes based on bits (e.g., extracting the Most Significant Bits to see general shape, or Least Significant Bits to hide data/find noise).

### 2. Histogram Processing
Techniques used to redistribute the grey levels across the image.
*   **Histogram Equalization:** Spreads out pixel frequencies to improve dark or washed-out images, making dark areas more visible.
*   **CLAHE:** Contrast Limited Adaptive Histogram Equalization.

### 3. Spatial Smoothing Filters (For Noise Removal)
These filters average out a neighborhood of pixels to blur the image and reduce noise.
*   **Arithmetic Mean Filter (Simple Averaging Filter):** Averages all pixels in a neighborhood.
*   **Geometric Mean Filter:** Darker pixels have a stronger influence. It smooths similarly to the arithmetic mean but loses less image detail.
*   **Harmonic Mean Filter:** Another variant of the mean filter used for restoration.
*   **Contraharmonic Mean Filter:** A highly sensitive filter where choosing the wrong "Q" value can cause drastic, unwanted results.

### 4. Order Statistics Filters
Filters based on sorting/ranking the pixel values in a specific neighborhood.
*   **Median Filter:** Replaces the center pixel with the median value. Excellent for removing "salt and pepper" noise without the heavy blurring caused by averaging filters.
*   **Min Filter:** Sets the pixel to the lowest value in the neighborhood.
*   **Max Filter:** Sets the pixel to the highest value in the neighborhood.
*   **Midpoint Filter:** Another order-based spatial filter used for noise removal.
*   **Alpha-Trimmed Mean Filter:** Trims extreme high and low values before averaging.

### 5. Advanced Denoisers
More complex noise-handling techniques briefly mentioned in the text.
*   **Gaussian Filter:** Used for general noise smoothing.
*   **Bilateral Filter:** An advanced filter for handling noise.
*   **Non-Local Means**.
*   **Wavelet Thresholding**.
*   **Deep Learning-based Denoisers**.

### 6. Spatial Sharpening & Discontinuity Detectors
Used to highlight fine details, lines, points, and edges (often leading into object recognition).
*   **1st Derivative Filters:** Used to calculate gradients for edge detection.
*   **2nd Derivative Filters:** Provide a stronger response to fine details than 1st derivative filters.
*   **The Laplacian Filter:** A 2nd derivative filter that perfectly highlights edges and discontinuities. (The original image is usually subtracted from the Laplacian result to yield a final sharpened image).
*   **Composite Laplacian Masks:** Variations of the standard Laplacian that combine the original image and the Laplacian into a single filtering step.
*   **Point Detection Mask:** A specific mask configured with an "8" in the center and "-1" around the edges to find isolated points.
*   **Roberts Masks:** A simple 2x2 edge detection gradient operator.
*   **Prewitt Masks:** A 3x3 edge detection gradient operator.
*   **Sobel Operators (Masks):** A 3x3 edge detection filter (combining horizontal and vertical gradient components) that heavily emphasizes edges.

### 7. Frequency Domain Filters
Filters applied after transforming an image into its frequency components (using a Fast Fourier Transform) to handle large images faster.
*   **Butterworth Highpass Filter:** Used to sharpen an image by passing high frequencies.
*   **High-Frequency Emphasis Filter:** Enhances high frequencies (edges) while retaining some low-frequency background.
*   **Butterworth Bandreject Filter:** Specifically designed to remove repeating, periodic noise (like sinusoidal electrical interference) from an image.

### 8. Morphological Processing
Used later in the pipeline to alter the structural shape of features in the image (like thickening lines or removing small specs).
*   **Erosion:** Shrinks or thins objects in a binary image.
*   **Dilation:** Grows or thickens objects in a binary image.
*   **Opening:** An erosion followed by a dilation (useful for removing small noise spots).
*   **Closing:** A dilation followed by an erosion (useful for closing small gaps or holes in features).
