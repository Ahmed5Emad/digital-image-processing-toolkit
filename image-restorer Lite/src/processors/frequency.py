import numpy as np
from .utils import apply_blend


def _get_distance_matrix(rows, cols):
    crow, ccol = rows // 2, cols // 2
    x = np.linspace(-ccol, ccol, cols)
    y = np.linspace(-crow, crow, rows)
    X, Y = np.meshgrid(x, y)
    return np.sqrt(X**2 + Y**2)


def _apply_filter(image, mask):
    dft = np.fft.fft2(image)
    dft_shift = np.fft.fftshift(dft)
    filtered_dft = dft_shift * mask
    dft_ishift = np.fft.ifftshift(filtered_dft)
    img_back = np.fft.ifft2(dft_ishift)
    img_back = np.abs(img_back)
    return np.clip(img_back, 0, 255).astype(np.uint8)


def ideal_lowpass_filter(image, cutoff=30, **kwargs):
    rows, cols = image.shape
    D = _get_distance_matrix(rows, cols)
    mask = np.zeros((rows, cols))
    mask[D <= cutoff] = 1
    return _apply_filter(image, mask)


def butterworth_lowpass_filter(image, cutoff=30, n=2, **kwargs):
    rows, cols = image.shape
    D = _get_distance_matrix(rows, cols)
    mask = 1 / (1 + (D / (cutoff + 1e-6))**(2 * n))
    return _apply_filter(image, mask)


def gaussian_lowpass_filter(image, cutoff=30, **kwargs):
    rows, cols = image.shape
    D = _get_distance_matrix(rows, cols)
    mask = np.exp(-(D**2) / (2 * (cutoff**2) + 1e-6))
    return _apply_filter(image, mask)
