# Image Processing Filters & Techniques

## Intensity Transformations & Point Processing
These operations apply a transformation function to individual pixels to change their intensity.

- **Negative Images (Image Inversion)**: Inverts the intensity values of an image using formulas like `s = 1.0 - r` or `s = intensity_max - r`.
    - **Use Case**: Enhancing white or grey detail embedded in dark regions, such as making tissue clearer in medical mammograms.
- **Thresholding**: Converts an image into a binary format (e.g., values below a threshold become 0.0, and above become 1.0).
    - **Use Case**: Image segmentation, specifically for isolating an object of interest from a background.
- **Logarithmic Transformations (Log / Inverse Log)**: Expands the values of dark pixels while compressing higher-level brightness values.
    - **Use Case**: Correcting non-linear display responses, such as performing Gamma correction so a monitor displays an image's true brightness without distorting dark or light tones.
- **Power-Law (Gamma) Transformations (`s = c * r^γ`)**: Maps a narrow range of input values into a wider range of output values based on the variable `γ`.
    - **Use Case**: Gamma correction for display devices, and significantly improving the contrast of dark medical images, such as fractured human spine MRI scans.
- **Contrast Stretching (Piecewise Linear Transformation)**: Stretches the range of intensity values to span the full dynamic range.
    - **Use Case**: Fixing low-contrast or washed-out images by spreading out the frequencies to make details pop.
- **Gray Level Slicing**: Highlights a specific band or range of gray levels while suppressing or preserving the rest.
    - **Use Case**: Identifying specific features in an image, such as highlighting water or bridge structures in satellite imagery.
- **Bit Plane Slicing**: Decomposes an 8-bit image into 8 separate binary images representing each bit. Higher bits contain general shapes, while lower bits contain minor details or noise.
    - **Use Case**: Image analysis (compression and encryption), image enhancement (discarding lower bit planes to remove noise), and steganography (hiding secret messages or watermarks inside invisible least-significant bit planes).
- **Histogram Equalization**: Spreads out the intensity frequencies to equalize an image.
    - **Use Case**: A simple and effective way to make dark areas more visible and improve washed-out images.

---

## Spatial Filtering (Neighborhood Operations)
These techniques operate on a local neighborhood of pixels (often a 3x3 mask) using operations like correlation and convolution.

### Smoothing Filters (Noise Removal & Blurring)
- **Averaging Filter (Arithmetic Mean)**: Averages all the pixel values within a neighborhood.
    - **Use Case**: Removing general noise from images, highlighting gross details, and blurring out fine, irrelevant details.
- **Median Filter (Order Statistic)**: Replaces the central pixel with the median value of its neighborhood.
    - **Use Case**: Excellent for noise removal without causing the aggressive smoothing/blurring associated with mean filters. Highly effective at removing salt-and-pepper (impulse) noise.

### Sharpening Filters (Edge & Detail Highlighting)
- **Laplacian Filter (2nd Derivative)**: Uses spatial differentiation to highlight fine details and sudden intensity changes.
    - **Use Case**: Removing blurring, highlighting edges, and drastically sharpening images like scanning electron microscope pictures or nuclear bone scans.
- **Gradient / 1st Derivative Filters (Sobel, Roberts, Prewitt)**: Masks that measure the directional rate of change in an image.
    - **Use Case**: Detecting and highlighting directional edges (e.g., horizontal or vertical gradient components) in structural images like buildings.

---

## Advanced Noise Removal & Image Restoration
These filters target specific kinds of noise profiles to restore corrupted images.

- **Geometric Mean Filter**: Computes the geometric mean of a window, allowing darker pixels to have a stronger influence.
    - **Use Case**: Reduces multiplicative noise and bright spikes (impulse noise) while preserving edge sharpness better than a standard arithmetic mean filter.
- **Harmonic Mean Filter**: Operates using the reciprocal sum of neighborhood pixels.
    - **Use Case**: An alternative mean filter used for specific noise profiles where arithmetic mean fails.
- **Contraharmonic Mean Filter**: Uses a parameter Q to adjust the filtering behavior.
    - **Use Case**: Using a positive Q eliminates "pepper" (black) noise, while a negative Q eliminates "salt" (white) noise.
- **Max Filter**: Replaces the pixel with the maximum value in the neighborhood.
    - **Use Case**: Excellent for specifically eliminating pepper noise.
- **Min Filter**: Replaces the pixel with the minimum value in the neighborhood.
    - **Use Case**: Excellent for specifically eliminating salt noise.
- **Midpoint Filter**: Averages the maximum and minimum values in a neighborhood.
    - **Use Case**: Good for fixing random Gaussian and uniform noise.
- **Alpha-Trimmed Mean Filter**: Deletes a specific number of the lowest and highest gray levels before averaging the rest.
    - **Use Case**: A hybrid filter that fixes images suffering from a combination of Gaussian noise and salt-and-pepper noise simultaneously.
- **Adaptive Median Filter**: A filter whose window size dynamically changes depending on the local characteristics of the image.
    - **Use Case**: Removing highly dense impulse noise that standard median filters can't handle, providing smoothing for non-impulse noise, and reducing overall distortion.
- **Bilateral Filter, Non-Local Means, Wavelet Thresholding, Deep Learning Denoisers**: Advanced algorithms.
    - **Use Case**: State-of-the-art denoising and structural preservation beyond standard masks.

---

## Frequency Domain Filtering
These filters use the Fourier transform to modify the frequency spectrum of an image before converting it back.

- **Ideal Low Pass Filter (ILPF)**: Cuts off high frequencies abruptly at a hard radius.
    - **Use Case**: Smoothing an image, though it leaves severe "ringing" artifacts around edges.
- **Butterworth Low Pass Filter**: Cuts off high frequencies with a mathematically smooth transition.
    - **Use Case**: Smoothing and blurring images effectively with much less ringing than the ideal filter.
- **Gaussian Low Pass Filter**: Uses a Gaussian bell curve to attenuate high frequencies.
    - **Use Case**: Seamlessly blurring images with absolutely zero ringing artifacts. Perfect for connecting broken text characters in poor-resolution documents and removing blemishes in human photographs.
- **Ideal, Butterworth, and Gaussian High Pass Filters**: Attenuates low frequencies to let high frequencies pass.
    - **Use Case**: Extracting edges and sharpening images.
- **Laplacian in the Frequency Domain**: The frequency-equivalent of the 2nd derivative mask.
    - **Use Case**: Highlighting structural details and edges mathematically via the frequency spectrum.
- **Band Reject Filters (Ideal, Butterworth, Gaussian)**: Removes a specific band (ring) of frequencies.
    - **Use Case**: Eliminating regular, periodic noise patterns caused by electrical or electromagnetic interference, such as sinusoidal noise obscuring a satellite image.

---

## Image Segmentation Filters
Algorithms aimed at finding highly specific geometrical features.

- **Point Detection Mask**: A mask containing -1s surrounding a central 8.
    - **Use Case**: Detecting isolated points or tiny anomalies, such as identifying a microscopic porosity defect in an X-ray of an industrial turbine blade.
- **Line Detection Masks**: Directional masks explicitly tuned to horizontal, vertical, +45°, and -45° angles.
    - **Use Case**: Extracting lines that are exactly one pixel thick running in specific directions, such as inspecting the traces on a binary wire-bond mask.
